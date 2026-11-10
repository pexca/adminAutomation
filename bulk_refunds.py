import csv
import json
import time
import requests

# --- CONFIGURATION ---
URL = "https://api.sandbox.fusionpayments.io/api/v1/merchant/refunds"
TOKEN = "insertTheToken"
INPUT_FILE = "payments.csv"
OUTPUT_FILE = "responses.jsonl"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def process_refunds():
    try:
        # Open CSV and Output file simultaneously as memory-efficient streams
        with open(INPUT_FILE, "r", encoding="utf-8") as f_in, open(
            OUTPUT_FILE, "a", encoding="utf-8"
        ) as f_out:

            # DictReader automatically maps columns using the first row as keys
            reader = csv.DictReader(f_in)

            for row in reader:
                payment_id = row.get("paymentId", "").strip()
                amount_value = row.get("amount", "").strip()

                # Skip row if crucial data is missing
                if not payment_id or not amount_value:
                    print(f"[-] Skipping invalid row: {row}")
                    continue

                # Construct dynamic payload
                payload = {
                    "amount": {"currency": "AED", "value": amount_value},
                    "paymentId": payment_id,
                }

                print(
                    f"[...] Sending refund for ID: {payment_id} | Amount: {amount_value} RUB"
                )

                try:
                    response = requests.post(URL, json=payload, headers=HEADERS)

                    try:
                        resp_data = response.json()
                    except ValueError:
                        resp_data = {"error": "Non-JSON response", "raw": response.text}

                    # Package the data for logging
                    log_entry = {
                        "paymentId": payment_id,
                        "requested_amount": amount_value,
                        "status_code": response.status_code,
                        "response": resp_data,
                    }

                    # Live updates in console
                    print(
                        f"[+] Status: {response.status_code} | Resp: {json.dumps(resp_data)}"
                    )

                    # Commit to disk immediately
                    f_out.write(json.dumps(log_entry) + "\n")
                    f_out.flush()

                except requests.exceptions.RequestException as e:
                    print(f"[-] Network error for {payment_id}: {e}")

                # Rate-limiting delay to breathe (500ms)
                time.sleep(0.5)

    except FileNotFoundError:
        print(f"[-] Error: Base input file '{INPUT_FILE}' not found.")


if __name__ == "__main__":
    process_refunds()
