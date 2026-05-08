import json, time, random
from datetime import datetime

try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False

BOOTSTRAP_SERVERS = ['localhost:19092']
TOPIC = 'payflow.transactions.live'

PAYMENT_METHODS = ['UPI', 'IMPS', 'NEFT', 'RTGS', 'NACH', 'CTS']
BANKS = ['SBI', 'HDFC', 'ICICI', 'Axis', 'Kotak', 'PNB', 'BOB', 'Canara']

def generate_transaction(offset):
    return {
        "transaction_id": f"TXN{random.randint(100000, 999999)}",
        "timestamp": datetime.utcnow().isoformat(),
        "payment_method": random.choice(PAYMENT_METHODS),
        "sender_bank": random.choice(BANKS),
        "receiver_bank": random.choice(BANKS),
        "amount_inr": round(random.uniform(10, 50000), 2),
        "status": random.choices(['SUCCESS', 'FAILED', 'PENDING'], weights=[85, 10, 5])[0],
        "offset": offset
    }

def run_producer():
    global KAFKA_AVAILABLE  # Fixes the UnboundLocalError
    print("🚀 Starting PayFlow Producer...")

    producer = None
    if KAFKA_AVAILABLE:
        try:
            producer = KafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8')
            )
            print(f"✅ Connected to Redpanda at {BOOTSTRAP_SERVERS[0]}")
        except Exception as e:
            print(f"⚠️ Redpanda not reachable, switching to Simulation Mode: {e}")
            KAFKA_AVAILABLE = False

    i = 0
    while True:
        txn = generate_transaction(i)
        if KAFKA_AVAILABLE and producer:
            producer.send(TOPIC, key=txn['payment_method'], value=txn)
            print(f"[LIVE] {txn['transaction_id']} | {txn['payment_method']} | ₹{txn['amount_inr']}")
        else:
            print(f"[SIMULATED] {txn['transaction_id']} | {txn['payment_method']} | ₹{txn['amount_inr']}")
        i += 1
        time.sleep(0.5)

if __name__ == "__main__":
    run_producer()