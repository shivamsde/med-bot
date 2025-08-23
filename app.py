from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ✅ Environment variables (set these in Render)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")  # your webhook verify token
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")      # your permanent token
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID") # your WhatsApp Business number ID

# Webhook endpoint
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Verification failed", 403

    elif request.method == 'POST':
        data = request.get_json()
        print("🔔 Webhook event received")

        try:
            change = data["entry"][0]["changes"][0]["value"]

            # ✅ Incoming messages
            if "messages" in change:
                message = change["messages"][0]
                sender = message["from"]
                text = message.get("text", {}).get("body", "")

                print(f"📩 Incoming message from {sender}: {text}")
                reply(sender, f"You said: {text}")

            # ✅ Status updates (delivered, read, etc.)
            elif "statuses" in change:
                status = change["statuses"][0]
                msg_id = status.get("id")
                msg_status = status.get("status")
                recipient = status.get("recipient_id")

                print(f"📬 Status update: message {msg_id} → {msg_status} for {recipient}")

            else:
                print("⚠️ Unknown webhook event type:", change)

        except Exception as e:
            print("❌ Error handling webhook:", str(e))

        return "EVENT_RECEIVED", 200

# Function to reply with text message
def reply_text(to, text):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Reply response:", response.json())

# Function to reply with a template message
def reply_template(to, template_name):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": "en_US"}
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Template reply response:", response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
