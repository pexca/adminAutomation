import sys
import time
import requests

BOT_TOKEN = "insertTheToken"
CONFIG_FILE = "telegram_targets.txt"

# Make sure /bot is explicitly written out here before the curly braces:
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def load_chat_ids():
    """Reads raw IDs from a text file, ignoring empty lines and comments."""
    chat_ids = []
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comment lines starting with '#'
                if not line or line.startswith("#"):
                    continue
                # Split line if there's an inline comment, keep only the ID part
                raw_id = line.split("#")[0].strip()
                chat_ids.append(raw_id)
        return chat_ids
    except FileNotFoundError:
        print(f"❌ Error: Targets file '{CONFIG_FILE}' not found.")
        sys.exit(1)

def send_alert(alert_type, affected_method=""):
    chat_ids = load_chat_ids()
    
    if not chat_ids:
        print("⚠️ Warning: No Chat IDs found in the target list.")
        return

    # Build the message string
    if alert_type == "downtime":
        method_detail = f"**Method/Service:** `{affected_method}`" if affected_method else "Scheduled backend updates."
        message_text = (
            "⚠️ *SYSTEM DOWNTIME NOTICE*\n\n"
            "The environment is undergoing temporary maintenance.\n"
            f"{method_detail}\n\n"
            "🔴 Please save your work. Testing functionality is currently paused for this service."
        )
    elif alert_type == "recovery":
        message_text = (
            "✅ *SYSTEM RECOVERY NOTICE*\n\n"
            "Восстановлена функциональность сервиса."
        )
    else:
        print("❌ Invalid alert type. Use 'downtime' or 'recovery'.")
        return

    print(f"🚀 Dispatched {alert_type.upper()} broadcast to {len(chat_ids)} targets...")
    
    # Loop over the raw IDs directly
    for chat_id in chat_ids:
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        
        try:
            res = requests.post(BASE_URL, json=payload, timeout=10).json()
            if res.get("ok"):
                print(f"   ↳ Success -> {chat_id}")
            else:
                print(f"   ↳ ❌ Failed -> {chat_id}: {res.get('description')}")
        except Exception as e:
            print(f"   ↳ 💥 Network Error -> {chat_id}: {e}")
            
        time.sleep(1.0)  # Standard anti-flood pacing

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\n📝 Usage:")
        print("  python broadcast_alert.py downtime [name_of_failed_method]")
        print("  python broadcast_alert.py recovery\n")
        sys.exit(1)

    action = sys.argv[1].lower()
    method_or_service = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    send_alert(action, method_or_service)
