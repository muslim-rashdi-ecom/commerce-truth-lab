"""Strict canonical contract, not a Shopify/Stripe payload parser."""

from datetime import datetime, timezone
import re


class ValidationError(ValueError):
    """Input cannot safely be audited."""


KINDS = {
    "capture": "payments", "refund": "payments",
    "delivered": "fulfillment", "cod_collected": "cod",
    "cod_settled": "cod", "purchase_signal": "signals:",
}


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def fields(obj, required, optional=()):
    require(isinstance(obj, dict), "Expected an object")
    require(set(required) <= obj.keys(), "Missing required fields: " + str(sorted(set(required) - obj.keys())))
    require(obj.keys() <= set(required) | set(optional), "Unknown fields are not accepted; use the canonical contract")


def text(value):
    require(isinstance(value, str) and 0 < len(value) <= 160, "Expected a nonempty string of at most 160 characters")
    require(not any(ord(c) < 32 or ord(c) == 127 for c in value), "Control characters are not accepted")


def integer(value, maximum=10**15):
    require(type(value) is int and 0 <= value <= maximum, "Expected a bounded, nonnegative integer (not float/bool)")


def timestamp(value):
    require(isinstance(value, str), "Timestamp must be an ISO-8601 string with a timezone")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError("Invalid ISO-8601 timestamp") from exc
    require(parsed.tzinfo is not None, "Naive timestamps are not accepted")
    return parsed.astimezone(timezone.utc)


def destination(value):
    require(isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9_-]{0,39}", value), "Invalid destination label")


def stream_name(value):
    require(isinstance(value, str), "Invalid stream")
    if value.startswith("signals:"):
        destination(value[8:])
    else:
        require(value in {"payments", "cod", "fulfillment"}, "Unsupported stream")


def validate(data):
    fields(data, ("schema_version", "data_kind", "as_of", "currency_exponents", "policy", "coverage", "orders", "events"))
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "Unsupported schema version")
    require(isinstance(data["data_kind"], str) and data["data_kind"] in {"synthetic", "merchant_export"}, "Explicit data_kind is required")
    as_of = timestamp(data["as_of"])
    exponents = data["currency_exponents"]
    require(isinstance(exponents, dict) and 0 < len(exponents) <= 200, "Declare currency exponents")
    for code, exponent in exponents.items():
        require(re.fullmatch(r"[A-Z]{3}", code), "Use three-letter uppercase currency labels")
        integer(exponent, 4)
    fields(data["policy"], ("signal_grace_hours", "collection_grace_hours", "cod_settlement_grace_hours"))
    for value in data["policy"].values():
        integer(value, 87600)
    for key in ("orders", "events", "coverage"):
        require(isinstance(data[key], list) and len(data[key]) <= 100000, "Expected a bounded list")
    order_map = {}
    for order in data["orders"]:
        fields(order, ("store_id", "order_id", "created_at", "currency", "total_minor", "payment_method", "market", "locale", "signals"))
        for key in ("store_id", "order_id", "market", "locale"):
            text(order[key])
        require(isinstance(order["currency"], str) and order["currency"] in exponents, "Undeclared order currency")
        integer(order["total_minor"])
        require(isinstance(order["payment_method"], str) and order["payment_method"] in {"prepaid", "cod"}, "Only prepaid and COD supported in v0.1")
        require(timestamp(order["created_at"]) <= as_of, "Order created after as_of")
        key = (order["store_id"], order["order_id"])
        require(key not in order_map, "Duplicate order identity")
        order_map[key] = order
        require(isinstance(order["signals"], dict) and len(order["signals"]) <= 20, "signals must map destination labels to expectations")
        for channel, expectation in order["signals"].items():
            destination(channel)
            fields(expectation, ("permitted", "expected_value_minor"))
            require(type(expectation["permitted"]) is bool, "permitted must be a JSON boolean")
            integer(expectation["expected_value_minor"])
    stores = {key[0] for key in order_map}
    seen_coverage = set()
    for coverage in data["coverage"]:
        fields(coverage, ("store_id", "stream", "from", "through", "complete"))
        text(coverage["store_id"])
        require(coverage["store_id"] in stores, "Coverage references unknown store")
        stream_name(coverage["stream"])
        require(type(coverage["complete"]) is bool, "complete must be a JSON boolean")
        require(timestamp(coverage["from"]) <= timestamp(coverage["through"]), "Reversed coverage interval")
        key = (coverage["store_id"], coverage["stream"])
        require(key not in seen_coverage, "One coverage interval per store/stream required")
        seen_coverage.add(key)
    seen_events = {}
    for event in data["events"]:
        fields(event, ("id", "store_id", "order_id", "stream", "kind", "at"), ("currency", "amount_minor", "dedup_key"))
        for key in ("id", "store_id", "order_id"):
            text(event[key])
        order_key = (event["store_id"], event["order_id"])
        require(order_key in order_map, "Event references an unknown order; include its order snapshot")
        require(timestamp(event["at"]) >= timestamp(order_map[order_key]["created_at"]), "Event predates its order")
        stream_name(event["stream"])
        require(isinstance(event["kind"], str) and event["kind"] in KINDS, "Unsupported event kind")
        expected_stream = KINDS[event["kind"]]
        require(event["stream"].startswith(expected_stream) if expected_stream == "signals:" else event["stream"] == expected_stream, "Event kind/stream mismatch")
        if event["kind"] != "delivered":
            require("amount_minor" in event and "currency" in event, "Monetary event needs amount and currency")
            integer(event["amount_minor"])
            require(isinstance(event["currency"], str) and event["currency"] in exponents, "Undeclared event currency")
        else:
            require("amount_minor" not in event and "currency" not in event, "Delivery is not a cash transaction")
        if event["kind"] == "purchase_signal":
            require("dedup_key" in event, "Normalized platform-specific dedup_key is required")
            text(event["dedup_key"])
            require(event["stream"][8:] in order_map[order_key]["signals"], "Declare signal expectations for every observed destination")
        else:
            require("dedup_key" not in event, "dedup_key is only for purchase signals")
        if event["kind"].startswith("cod_"):
            require(order_map[order_key]["payment_method"] == "cod", "COD event on prepaid order")
        if event["kind"] in {"capture", "refund"}:
            require(order_map[order_key]["payment_method"] == "prepaid", "COD refunds/mixed tenders are unsupported; do not coerce")
        identity = (event["store_id"], event["stream"], event["id"])
        require(identity not in seen_events or seen_events[identity] == event, "Conflicting records share one source identity")
        seen_events[identity] = event
    return data
