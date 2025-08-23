from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ✅ Environment variables (set these in Render)
VERIFY_TOKEN = os.environ.get("pharma_bot")  # your webhook verify token
ACCESS_TOKEN = os.environ.get("EAARuPWJ117kBPYzrJSx7NOurezrFOWOZBPwPZBLeDTS3ENItxNabMc8DL0VuQGxGZBUdEW8tNQ4kxVodEzxenYhkW5ayibZBK8YQ1F2Xgi3PcwxoPHsTO2WTZBzneVWi7MsSkhGQDPj4E5Pn2l2IyZA7W9gmoLMZCJZAg2iqXRu8qJo1Jskld2h3hN5upAD2fZBZAgrMimyvNNZAWKu8QB89gPB1cc3LZCQA5ZBIHdPwi")      # your permanent token
PHONE_NUMBER_ID = os.environ.get("747806788420880") # your WhatsApp Business number ID

# Webhook endpoint
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Meta webhook verification
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Verification failed", 403

    elif request.method == "POST":
        # Incoming message handling
        data = request.get_json()
        print("Webhook event:", data)

        try:
            change = data["entry"][0]["changes"][0]["value"]

            # Only process if "messages" exists
            if "messages" in change:
                message = change["messages"][0]
                sender = message["from"]
                text = message.get("text", {}).get("body", "")

                print(f"📩 Message from {sender}: {text}")

                # Auto-reply with text
                reply_text(sender, f"You said: {text}")

                # Optional: send template message
                # reply_template(sender, "hello_world")  # uncomment if template is needed

            else:
                print("⚠️ Webhook event without 'messages'. Ignored.")

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
