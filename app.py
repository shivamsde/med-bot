from flask import Flask, request
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("pharma_bot")
ACCESS_TOKEN = os.environ.get("1247109830793145|Ui00En9DX7E2j2QA8SXOs20uzOk")
PHONE_NUMBER_ID = os.environ.get("747806788420880")

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
        print("Webhook event:", data)  # log everything

        try:
            change = data["entry"][0]["changes"][0]["value"]

            # Only process if "messages" exists
            if "messages" in change:
                message = change["messages"][0]
                sender = message["from"]
                text = message["text"]["body"]

                print(f"📩 Message from {sender}: {text}")
                reply(sender, f"You said: {text}")
            else:
                print("⚠️ Webhook event without 'messages' (probably status update). Ignored.")

        except Exception as e:
            print("❌ Error handling webhook:", str(e))

        return "EVENT_RECEIVED", 200

def reply(to, text):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Reply response:", response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
