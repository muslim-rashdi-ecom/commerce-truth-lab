import csv
import io
from typing import List, Dict
from schemas.responses import UploadResponse

KNOWN_FIELDS = {
    "order_id": ["order id", "order", "id", "order_name", "name"],
    "created_at": ["created at", "date", "created", "timestamp"],
    "currency": ["currency", "ccy"],
    "total_amount": ["total", "amount", "total amount", "price"],
    "payment_method": ["payment", "payment method", "gateway"],
    "status": ["status", "state", "financial_status"],
    "customer_id": ["customer", "user id", "customer id", "email"]
}

def fuzzy_match(header: str, known: str) -> bool:
    h = header.lower().replace("_", " ").strip()
    return h in known or known in h

def suggest_mapping(header: str) -> str:
    for field, variations in KNOWN_FIELDS.items():
        for var in variations:
            if fuzzy_match(header, var):
                return field
    return ""

async def process_upload(file_name: str, contents: bytes) -> UploadResponse:
    decoded = contents.decode('utf-8-sig', errors='replace')
    reader = csv.reader(io.StringIO(decoded))
    
    headers = []
    preview = []
    try:
        headers = next(reader)
        for _ in range(5):
            try:
                preview.append(next(reader))
            except StopIteration:
                break
    except StopIteration:
        pass
    
    mappings = {}
    for h in headers:
        s = suggest_mapping(h)
        if s:
            mappings[h] = s

    return UploadResponse(
        file_name=file_name,
        detected_headers=headers,
        preview_rows=preview,
        suggested_mappings=mappings,
        warnings=[],
        errors=[]
    )
