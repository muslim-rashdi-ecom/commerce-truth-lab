"""Deterministic, entirely synthetic casebook; no Livora/client results."""

from copy import deepcopy


def demo_data():
    data = {
        "schema_version": 1, "data_kind": "synthetic", "as_of": "2026-09-19T12:00:00Z",
        "currency_exponents": {"AED": 2, "USD": 2, "PKR": 2, "JPY": 0, "KWD": 3},
        "policy": {"signal_grace_hours": 24, "collection_grace_hours": 48, "cod_settlement_grace_hours": 168},
        "coverage": [], "orders": [], "events": [],
    }
    for stream in ("payments", "cod", "fulfillment", "signals:meta", "signals:ga4"):
        data["coverage"].append({"store_id": "demo", "stream": stream, "from": "2026-09-01T00:00:00Z", "through": data["as_of"], "complete": True})

    def order(number, amount, currency="AED", method="prepaid", market="AE", locale="ar-AE", permitted=True):
        oid = f"DEMO-{number:03}"
        data["orders"].append({"store_id": "demo", "order_id": oid, "created_at": "2026-09-02T09:00:00Z", "currency": currency, "total_minor": amount, "payment_method": method, "market": market, "locale": locale, "signals": {"meta": {"permitted": permitted, "expected_value_minor": amount}}})
        return oid

    def event(oid, suffix, kind, amount=None, currency="AED", at="2026-09-02T09:05:00Z", key=None, channel="meta"):
        stream = {"capture": "payments", "refund": "payments", "delivered": "fulfillment", "cod_collected": "cod", "cod_settled": "cod", "purchase_signal": f"signals:{channel}"}[kind]
        row = {"id": f"{oid}-{suffix}", "store_id": "demo", "order_id": oid, "stream": stream, "kind": kind, "at": at}
        if amount is not None:
            row.update(amount_minor=amount, currency=currency)
        if kind == "purchase_signal":
            row["dedup_key"] = key or f"purchase-{oid}"
        data["events"].append(row)
        return row

    oid = order(1, 10000)
    event(oid, "capture", "capture", 10000)
    event(oid, "browser", "purchase_signal", 10000)
    event(oid, "server", "purchase_signal", 10000)  # matching key: not duplicate-purchase finding
    data["events"].append(deepcopy(data["events"][-1]))  # retry: not a second event

    oid = order(2, 14000)
    event(oid, "capture", "capture", 14000)
    event(oid, "browser", "purchase_signal", 14000, key="browser-002")
    event(oid, "server", "purchase_signal", 14000, key="server-002")

    oid = order(3, 25000, method="cod")
    event(oid, "signal", "purchase_signal", 25000)
    event(oid, "delivery", "delivered", at="2026-09-04T10:00:00Z")
    event(oid, "collected", "cod_collected", 25000, at="2026-09-04T10:00:00Z")
    event(oid, "settled", "cod_settled", 10000, at="2026-09-08T10:00:00Z")

    oid = order(4, 8000)
    event(oid, "signal", "purchase_signal", 8000)
    event(oid, "delivery", "delivered", at="2026-09-04T10:00:00Z")

    oid = order(5, 12000, "USD", market="US", locale="en-US")
    event(oid, "capture", "capture", 12000, "USD")
    event(oid, "signal", "purchase_signal", 12000, "USD")
    event(oid, "refund", "refund", 12000, "USD", at="2026-09-07T10:00:00Z")  # healthy full refund, not a leak

    oid = order(6, 5000, "JPY", market="JP", locale="ja-JP")
    event(oid, "capture", "capture", 5000, "JPY")
    event(oid, "signal", "purchase_signal", 500000, "JPY")  # erroneous decimal exponent

    oid = order(7, 15900, "KWD", market="KW", locale="ar-KW")
    event(oid, "capture", "capture", 15900, "KWD")
    event(oid, "signal", "purchase_signal", 15900, "KWD")  # 15.900 KWD, not 159.00

    oid = order(8, 200000, "PKR", method="cod", market="PK", locale="ur-PK")
    event(oid, "signal", "purchase_signal", 200000, "PKR")
    event(oid, "delivery", "delivered", at="2026-09-19T09:00:00Z")
    event(oid, "collected", "cod_collected", 200000, "PKR", at="2026-09-19T09:00:00Z")  # not overdue

    oid = order(9, 11000, permitted=False)
    event(oid, "capture", "capture", 11000)
    event(oid, "signal", "purchase_signal", 11000)  # configured-policy exception

    oid = order(10, 7500)
    event(oid, "capture", "capture", 7500)  # missing expected signal

    oid = order(11, 9900)
    event(oid, "capture", "capture", 9900)
    event(oid, "capture-2", "capture", 9900)
    event(oid, "signal", "purchase_signal", 9900)

    oid = order(12, 3000, "USD", market="US", locale="es-US")
    event(oid, "capture", "capture", 3000, "USD")
    event(oid, "signal", "purchase_signal", 3000, "AED")
    return data
