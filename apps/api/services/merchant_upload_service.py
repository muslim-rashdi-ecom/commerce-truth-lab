import csv
import io
import re
import secrets
import datetime
from typing import Dict, List, Tuple, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import (
    UploadMetadata, DataSource, Order, Payment, CourierSettlement, 
    Refund, PurchaseSignal, AuditLog
)
from security import pseudonymize_identifier

def sanitize_csv_value(val: Any) -> str:
    """
    Sanitizes CSV cell values to neutralize CSV Formula Injection (CWE-1236).
    If a string starts with formula trigger characters (=, +, -, @, \\t, \\r),
    prepend a single quote (') to prevent spreadsheet calculation upon viewing or export,
    unless it is a purely numerical signed number (e.g. -42.50).
    """
    if val is None:
        return ""
    s = str(val)
    if not s:
        return ""
    trimmed = s.strip()
    if re.match(r'^[+-]?\d+(\.\d+)?$', trimmed):
        return trimmed
    if s[0] in ('=', '+', '-', '@', '\t', '\r'):
        return f"'{s}"
    if trimmed and trimmed[0] in ('=', '+', '-', '@'):
        return f"'{trimmed}"
    return trimmed

STREAM_DEFINITIONS = {
    "shopify_orders": {
        "required": ["order_id", "total_amount", "currency"],
        "known_fields": {
            "order_id": ["order_id", "order id", "name", "order", "id"],
            "created_at": ["created_at", "created at", "date", "created", "processed_at"],
            "total_amount": ["total_amount", "total", "amount", "total price", "subtotal"],
            "currency": ["currency", "presentment_currency", "ccy"],
            "payment_method": ["payment_method", "payment", "gateway", "financial_status"],
            "status": ["status", "fulfillment_status", "state"],
            "customer_id": ["customer_id", "customer", "email", "customer email", "user_id"]
        },
        "pii_fields": ["customer_id", "email", "customer email", "phone", "address", "shipping_address", "billing_address", "customer_name", "name"]
    },
    "payments": {
        "required": ["order_id", "amount", "currency"],
        "known_fields": {
            "id": ["payment_id", "transaction_id", "id", "charge_id"],
            "order_id": ["order_id", "order", "order id", "reference"],
            "captured_at": ["captured_at", "date", "created", "timestamp"],
            "amount": ["amount", "captured_amount", "net", "gross"],
            "currency": ["currency", "ccy"],
            "gateway": ["gateway", "processor", "provider", "method"],
            "status": ["status", "state"]
        },
        "pii_fields": ["cardholder_name", "email", "customer_email"]
    },
    "courier_settlements": {
        "required": ["order_id", "collected_amount", "courier_name"],
        "known_fields": {
            "id": ["settlement_id", "id", "waybill", "airway_bill", "tracking_number"],
            "order_id": ["order_id", "order", "order id", "merchant_reference"],
            "courier_name": ["courier_name", "courier", "carrier", "delivery_partner"],
            "delivered_at": ["delivered_at", "delivery_date", "pod_date", "date"],
            "collected_amount": ["collected_amount", "collected", "cod_amount", "amount_collected"],
            "settled_amount": ["settled_amount", "remitted_amount", "deposited_amount", "net_settled"],
            "collection_currency": ["collection_currency", "currency", "ccy"],
            "settlement_status": ["settlement_status", "status", "remittance_status"]
        },
        "pii_fields": ["recipient_name", "phone", "address", "receiver_phone"]
    },
    "refunds": {
        "required": ["order_id", "amount", "currency"],
        "known_fields": {
            "id": ["refund_id", "id", "transaction_id"],
            "order_id": ["order_id", "order", "order id"],
            "refunded_at": ["refunded_at", "date", "created", "timestamp"],
            "amount": ["amount", "refund_amount", "total"],
            "currency": ["currency", "ccy"],
            "reason": ["reason", "notes", "note", "comment"]
        },
        "pii_fields": ["customer_email", "name"]
    },
    "purchase_signals": {
        "required": ["order_id", "platform", "value", "currency"],
        "known_fields": {
            "id": ["signal_id", "id", "event_id_unique"],
            "order_id": ["order_id", "order", "order id", "content_id"],
            "platform": ["platform", "source", "ad_channel", "pixel_type"],
            "event_name": ["event_name", "event", "action"],
            "event_id": ["event_id", "dedup_id", "transaction_id"],
            "reported_at": ["reported_at", "date", "timestamp", "event_time"],
            "currency": ["currency", "ccy"],
            "value": ["value", "amount", "revenue", "price"],
            "signal_type": ["signal_type", "type", "channel"]
        },
        "pii_fields": ["email", "external_id", "phone", "fbp", "fbc", "ip_address"]
    }
}

def normalize_string(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

def fuzzy_match_header(header: str, variations: List[str]) -> bool:
    norm_h = normalize_string(header)
    for v in variations:
        norm_v = normalize_string(v)
        if norm_h == norm_v or norm_v in norm_h or norm_h in norm_v:
            return True
    return False

def suggest_field_mappings(headers: List[str], source_type: str) -> Tuple[Dict[str, str], List[str]]:
    definition = STREAM_DEFINITIONS.get(source_type, STREAM_DEFINITIONS["shopify_orders"])
    known_fields = definition["known_fields"]
    pii_fields = definition["pii_fields"]
    
    suggested = {}
    pseudonymized = []
    
    for h in headers:
        # Check for PII headers
        for pii in pii_fields:
            if normalize_string(pii) in normalize_string(h):
                if h not in pseudonymized:
                    pseudonymized.append(h)
                    
        # Check known target field matches
        for target, variations in known_fields.items():
            if target not in suggested.values() and fuzzy_match_header(h, variations):
                suggested[h] = target
                break
                
    return suggested, pseudonymized

def parse_monetary_minor(val: Any, currency: str = "USD") -> int:
    """Parse string/float monetary value into integer minor units (e.g. cents)."""
    if val is None or val == "":
        return 0
    clean = re.sub(r'[^\d.-]', '', str(val))
    if not clean:
        return 0
    f = float(clean)
    curr = currency.upper()
    if curr in ["JPY", "KRW", "VND", "CLP"]:
        return int(round(f))
    elif curr in ["KWD", "BHD", "OMR"]:
        return int(round(f * 1000))
    else:
        return int(round(f * 100))

async def stage_csv_upload(
    workspace_id: str,
    source_type: str,
    file_name: str,
    contents: bytes,
    db: AsyncSession
) -> Dict[str, Any]:
    # 1. File size check (Max 25MB)
    if len(contents) > 25 * 1024 * 1024:
        raise ValueError("File size exceeds 25MB limit. Please upload smaller monthly batches.")
    
    if not file_name.lower().endswith(".csv"):
        raise ValueError("Invalid file format. Only .csv files are supported.")
        
    # 2. Decode CSV
    decoded = None
    for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
        try:
            decoded = contents.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if not decoded:
        raise ValueError("Failed to decode file encoding. Please ensure the CSV is encoded in UTF-8.")
        
    reader = csv.DictReader(io.StringIO(decoded))
    if not reader.fieldnames:
        raise ValueError("CSV contains no valid header row.")
        
    headers = [h.strip() for h in reader.fieldnames if h]
    
    # 3. Suggest mappings & identify PII columns to pseudonymize
    mappings, pii_cols = suggest_field_mappings(headers, source_type)
    
    # 4. Preview first 5 rows
    preview = []
    total_rows = 0
    warnings = []
    errors = []
    
    stream_def = STREAM_DEFINITIONS.get(source_type, STREAM_DEFINITIONS["shopify_orders"])
    for req_field in stream_def["required"]:
        if req_field not in mappings.values():
            warnings.append(f"Required field '{req_field}' was not automatically detected. Please map it manually.")
            
    for i, row in enumerate(reader):
        total_rows += 1
        if i < 5:
            # Mask PII in preview and sanitize formula injections
            safe_row = {}
            for k, v in row.items():
                if not k:
                    continue
                clean_k = sanitize_csv_value(k)
                if k in pii_cols:
                    safe_row[clean_k] = f"[PSEUDONYMIZED: {pseudonymize_identifier(v)}]"
                else:
                    safe_row[clean_k] = sanitize_csv_value(v)
            preview.append(safe_row)
            
    if total_rows == 0:
        errors.append("CSV file contains headers but zero data rows.")
        
    upload_id = f"upl_{secrets.token_hex(8)}"
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    upload_record = UploadMetadata(
        id=upload_id,
        workspace_id=workspace_id,
        source_type=source_type,
        file_name=file_name,
        file_size_bytes=len(contents),
        row_count=total_rows,
        mapped_columns=mappings,
        warnings=warnings,
        status="staged",
        created_at=now_iso
    )
    db.add(upload_record)
    await db.commit()
    
    return {
        "upload_id": upload_id,
        "file_name": file_name,
        "source_type": source_type,
        "detected_headers": headers,
        "suggested_mappings": mappings,
        "preview_rows": preview,
        "row_count": total_rows,
        "warnings": warnings,
        "errors": errors,
        "pseudonymized_fields": pii_cols
    }

async def commit_csv_import(
    workspace_id: str,
    upload_id: str,
    contents: bytes,
    confirmed_mappings: Dict[str, str],
    user_id: str,
    db: AsyncSession
) -> Dict[str, Any]:
    upload = (await db.execute(
        select(UploadMetadata).where(UploadMetadata.id == upload_id, UploadMetadata.workspace_id == workspace_id)
    )).scalars().first()
    if not upload:
        raise ValueError("Staged upload session not found or expired.")
        
    decoded = contents.decode('utf-8-sig', errors='replace')
    reader = csv.DictReader(io.StringIO(decoded))
    
    source_type = upload.source_type
    imported_count = 0
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Invert mapping: target_field -> csv_header
    inv = {v: k for k, v in confirmed_mappings.items()}
    
    if source_type == "shopify_orders":
        for row in reader:
            raw_oid = str(row.get(inv.get("order_id", ""), "")).strip()
            if not raw_oid:
                continue
            oid = sanitize_csv_value(raw_oid)
            curr = str(row.get(inv.get("currency", ""), "USD")).strip().upper()
            raw_amt = row.get(inv.get("total_amount", ""), "0")
            amt_minor = parse_monetary_minor(raw_amt, curr)
            raw_cust = row.get(inv.get("customer_id", ""), "")
            cust_hash = pseudonymize_identifier(raw_cust)
            created = str(row.get(inv.get("created_at", ""), now_iso)).strip()
            status = sanitize_csv_value(row.get(inv.get("status", ""), "paid"))
            method = sanitize_csv_value(row.get(inv.get("payment_method", ""), "prepaid"))
            
            # Upsert Order
            order = (await db.execute(
                select(Order).where(Order.workspace_id == workspace_id, Order.id == oid)
            )).scalars().first()
            if not order:
                order = Order(
                    id=oid,
                    workspace_id=workspace_id,
                    store_id="merchant_store",
                    created_at=created,
                    currency=curr,
                    total_amount_minor=amt_minor,
                    payment_method=method,
                    status=status,
                    customer_id=cust_hash,
                    is_synthetic=False
                )
                db.add(order)
            else:
                order.total_amount_minor = amt_minor
                order.currency = curr
                order.status = status
                order.customer_id = cust_hash
            imported_count += 1
            
    elif source_type == "payments":
        for row in reader:
            raw_pid = str(row.get(inv.get("id", ""), "")).strip()
            pid = sanitize_csv_value(raw_pid) if raw_pid else f"pay_{secrets.token_hex(6)}"
            raw_oid = str(row.get(inv.get("order_id", ""), "")).strip()
            if not raw_oid: continue
            oid = sanitize_csv_value(raw_oid)
            curr = str(row.get(inv.get("currency", ""), "USD")).strip().upper()
            amt = parse_monetary_minor(row.get(inv.get("amount", ""), "0"), curr)
            db.add(Payment(
                id=pid,
                workspace_id=workspace_id,
                order_id=oid,
                captured_at=str(row.get(inv.get("captured_at", ""), now_iso)).strip(),
                currency=curr,
                amount_minor=amt,
                gateway=sanitize_csv_value(row.get(inv.get("gateway", ""), "gateway")),
                status=sanitize_csv_value(row.get(inv.get("status", ""), "captured"))
            ))
            imported_count += 1
            
    elif source_type == "courier_settlements":
        for row in reader:
            raw_sid = str(row.get(inv.get("id", ""), "")).strip()
            sid = sanitize_csv_value(raw_sid) if raw_sid else f"set_{secrets.token_hex(6)}"
            raw_oid = str(row.get(inv.get("order_id", ""), "")).strip()
            if not raw_oid: continue
            oid = sanitize_csv_value(raw_oid)
            curr = str(row.get(inv.get("collection_currency", ""), "AED")).strip().upper()
            col = parse_monetary_minor(row.get(inv.get("collected_amount", ""), "0"), curr)
            raw_set = row.get(inv.get("settled_amount", ""), "")
            settled = parse_monetary_minor(raw_set, curr) if raw_set != "" else None
            db.add(CourierSettlement(
                id=sid,
                workspace_id=workspace_id,
                order_id=oid,
                courier_name=sanitize_csv_value(row.get(inv.get("courier_name", ""), "Courier")),
                delivered_at=str(row.get(inv.get("delivered_at", ""), now_iso)).strip(),
                collected_amount_minor=col,
                settled_amount_minor=settled,
                collection_currency=curr,
                settlement_status=sanitize_csv_value(row.get(inv.get("settlement_status", ""), "settled" if settled else "pending")),
                grace_days=7
            ))
            imported_count += 1
            
    elif source_type == "refunds":
        for row in reader:
            raw_rid = str(row.get(inv.get("id", ""), "")).strip()
            rid = sanitize_csv_value(raw_rid) if raw_rid else f"ref_{secrets.token_hex(6)}"
            raw_oid = str(row.get(inv.get("order_id", ""), "")).strip()
            if not raw_oid: continue
            oid = sanitize_csv_value(raw_oid)
            curr = str(row.get(inv.get("currency", ""), "USD")).strip().upper()
            amt = parse_monetary_minor(row.get(inv.get("amount", ""), "0"), curr)
            db.add(Refund(
                id=rid,
                workspace_id=workspace_id,
                order_id=oid,
                refunded_at=str(row.get(inv.get("refunded_at", ""), now_iso)).strip(),
                currency=curr,
                amount_minor=amt,
                reason=sanitize_csv_value(row.get(inv.get("reason", ""), "Customer return"))
            ))
            imported_count += 1
            
    elif source_type == "purchase_signals":
        for row in reader:
            raw_sig_id = str(row.get(inv.get("id", ""), "")).strip()
            sig_id = sanitize_csv_value(raw_sig_id) if raw_sig_id else f"sig_{secrets.token_hex(6)}"
            raw_oid = str(row.get(inv.get("order_id", ""), "")).strip()
            if not raw_oid: continue
            oid = sanitize_csv_value(raw_oid)
            curr = str(row.get(inv.get("currency", ""), "USD")).strip().upper()
            val = parse_monetary_minor(row.get(inv.get("value", ""), "0"), curr)
            db.add(PurchaseSignal(
                id=sig_id,
                workspace_id=workspace_id,
                order_id=oid,
                platform=sanitize_csv_value(row.get(inv.get("platform", ""), "meta")),
                event_name=sanitize_csv_value(row.get(inv.get("event_name", ""), "Purchase")),
                event_id=sanitize_csv_value(row.get(inv.get("event_id", ""), f"evt_{secrets.token_hex(4)}")),
                reported_at=str(row.get(inv.get("reported_at", ""), now_iso)).strip(),
                currency=curr,
                value_minor=val,
                signal_type=sanitize_csv_value(row.get(inv.get("signal_type", ""), "browser")),
                consent_granted=True,
                pixel_id="P1"
            ))
            imported_count += 1
            
    # Update or create DataSource record
    ds = (await db.execute(
        select(DataSource).where(DataSource.workspace_id == workspace_id, DataSource.source_type == source_type)
    )).scalars().first()
    if not ds:
        ds = DataSource(
            id=f"ds_{secrets.token_hex(6)}",
            workspace_id=workspace_id,
            name=f"{source_type}_import",
            source_type=source_type,
            coverage_status="full",
            completeness_status="good",
            last_processed=now_iso,
            record_count=imported_count
        )
        db.add(ds)
    else:
        ds.record_count += imported_count
        ds.last_processed = now_iso
        
    upload.status = "committed"
    upload.mapped_columns = confirmed_mappings
    
    # Audit log
    db.add(AuditLog(
        id=f"log_{secrets.token_hex(8)}",
        workspace_id=workspace_id,
        user_id=user_id,
        action="csv_committed",
        details={"source_type": source_type, "imported_rows": imported_count, "file_name": upload.file_name},
        timestamp=now_iso
    ))
    
    await db.commit()
    
    return {
        "success": True,
        "source_type": source_type,
        "imported_rows": imported_count,
        "message": f"Successfully imported {imported_count} verified records into {source_type}."
    }
