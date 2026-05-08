import json, time, random
from datetime import datetime

PAYMENT_METHODS = ['UPI', 'IMPS', 'NEFT', 'RTGS']
BANKS = ['SBI', 'HDFC', 'ICICI', 'Axis', 'Kotak', 'PNB']

def simulate_transaction_stream(num_transactions=50):
    print("🚀 PayFlow Kafka Stream Simulator")
    print("=" * 50)
    print("Topic: payflow.transactions.live")
    print("Broker: localhost:9092 (simulated)")
    print("=" * 50)

    for i in range(num_transactions):
        transaction = {
            "transaction_id": f"TXN{random.randint(100000, 999999)}",
            "timestamp": datetime.now().isoformat(),
            "payment_method": random.choice(PAYMENT_METHODS),
            "bank": random.choice(BANKS),
            "amount_inr": round(random.uniform(10, 50000), 2),
            "status": random.choices(['SUCCESS', 'FAILED', 'PENDING'], weights=[85, 10, 5])[0],
            "partition": random.randint(0, 2),
            "offset": i
        }
        print(f"[CONSUMER] Partition-{transaction['partition']} | "
              f"Offset-{transaction['offset']:04d} | "
              f"{transaction['payment_method']} | "
              f"₹{transaction['amount_inr']:,.2f} | "
              f"{transaction['status']}")
        time.sleep(0.2)

    print("\n✅ Stream simulation complete. 50 events processed.")

if __name__ == "__main__":
    simulate_transaction_stream()