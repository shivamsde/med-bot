from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "pharma_bot"
ACCESS_TOKEN = "EAARuPWJ117kBPMdwnIEWeGI6igYTWJQgp6GlN0JtZCCW29F7v6aVgQXXnycelazUZCr0HmePUpah0aWnFvPkhLuGrQpR7tawJlTIbC1n4DVgYnbeqHVdgIrzELQXq84ylutBKRaYzWSMWkKHhZC3GRb9ic9uXnHBUBCQKAS2e6cZB046IJXkrejKo0Rmtu63ZBPwGEvZCH9wPtYOFakNSMyUvKUCOFmRXD2gQM"
PHONE_NUMBER_ID = "747806788420880"

# Step 1: Webhook Verification
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

# Step 2: Receive Messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data['object'] == 'whatsapp_business_account':
        for entry in data['entry']:
            for change in entry['changes']:
                message = change['value']['messages'][0]
                sender = message['from']
                text = message['text']['body']

                if "order" in text.lower():
                    send_message(sender, "Please upload your prescription 📄")
                elif "hi" in text.lower():
                    send_message(sender, "Hello 👋 Welcome to PharmaCo! Type 'order' to place your order.")
                else:
                    send_message(sender, "Sorry, I didn’t understand. Type 'order' to start.")

    return jsonify(success=True)

# Step 3: Send Messages
def send_message(to, text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(port=5000)
