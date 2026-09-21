import sqlite3
import json

def init_db():
    conn = sqlite3.connect("data/synthetic/demo.db")
    cur = conn.cursor()
    # In a real app we would use SQLAlchemy models to create tables.
    # For now, just create some basic tables matching our models.
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, store_id TEXT, created_at TEXT, currency TEXT, total_amount_minor INTEGER, payment_method TEXT, status TEXT, customer_id TEXT, tags TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS payments (id TEXT PRIMARY KEY, order_id TEXT, captured_at TEXT, currency TEXT, amount_minor INTEGER, method TEXT, gateway TEXT, status TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS settlements (id TEXT PRIMARY KEY, order_id TEXT, courier_name TEXT, delivered_at TEXT, collected_amount_minor INTEGER, settled_amount_minor INTEGER, collection_currency TEXT, settlement_status TEXT, grace_days INTEGER)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS refunds (id TEXT PRIMARY KEY, order_id TEXT, refunded_at TEXT, currency TEXT, amount_minor INTEGER, reason TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS signals (id TEXT PRIMARY KEY, order_id TEXT, signal_type TEXT, platform TEXT, event_name TEXT, event_id TEXT, reported_at TEXT, currency TEXT, value_minor INTEGER, consent_granted BOOLEAN, pixel_id TEXT)''')

    with open("data/synthetic/dataset.json", "r") as f:
        data = json.load(f)

    for o in data["orders"]:
        cur.execute("INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (o["id"], o["store_id"], o["created_at"], o["currency"], o["total_amount_minor"], o["payment_method"], o["status"], o["customer_id"], json.dumps(o["tags"])))
    
    for p in data["payments"]:
        cur.execute("INSERT OR REPLACE INTO payments VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (p["id"], p["order_id"], p.get("captured_at"), p["currency"], p["amount_minor"], p["method"], p["gateway"], p["status"]))

    for s in data["settlements"]:
        cur.execute("INSERT OR REPLACE INTO settlements VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (s["id"], s["order_id"], s["courier_name"], s.get("delivered_at"), s.get("collected_amount_minor"), s.get("settled_amount_minor"), s["collection_currency"], s["settlement_status"], s["grace_days"]))

    for r in data["refunds"]:
        cur.execute("INSERT OR REPLACE INTO refunds VALUES (?, ?, ?, ?, ?, ?)", (r["id"], r["order_id"], r["refunded_at"], r["currency"], r["amount_minor"], r.get("reason")))

    for s in data["signals"]:
        cur.execute("INSERT OR REPLACE INTO signals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (s["id"], s["order_id"], s["signal_type"], s["platform"], s["event_name"], s.get("event_id"), s["reported_at"], s["currency"], s["value_minor"], s.get("consent_granted"), s.get("pixel_id")))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
