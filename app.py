import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# ✅ Load Together.AI API Key
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("⚠️ ERROR: Together.AI API Key is missing!")

# ✅ Create Flask app instance
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "LLaMA 3 Chatbot is running via Together.AI! 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is empty"}), 400

        # ✅ Use the correct LLaMA 3 model from Together.AI
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "togethercomputer/llama-3-8b-instruct",  # ✅ Correct Model
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 200
        }

        response = requests.post(
            "https://api.together.ai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        # ✅ Handle Response
        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
        else:
            bot_reply = f"⚠️ API Error: {response.json()}"

        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"error": f"⚠️ Server Error: {str(e)}"}), 500

# ✅ Run Flask on the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

