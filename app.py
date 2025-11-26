import os
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
AUTH_TOKEN = os.getenv("CLOUDFLARE_AUTH_TOKEN")
ACCOUNT_ID = os.getenv("ACCOUNT_ID")
CLOUDFLARE_MODEL_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-8b-instruct-fast"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = requests.post(
        CLOUDFLARE_MODEL_URL,
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
            "messages": [
                {"role": "system", "content": "You are a helpful career guidance assistant and you need to support mongolian language not caused by human language."},
                {"role": "user", "content": user_message}
            ]
        }
    )
    print("Status code:", response.status_code)
    print("Response text:", response.text)

    result = response.json()
    output_text = result.get("result", {}).get("response", "No response from AI")

    return jsonify({"reply": output_text})

if __name__ == "__main__":
    app.run(debug=True)
