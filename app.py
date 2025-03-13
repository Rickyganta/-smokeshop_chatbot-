from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

# ✅ Load Hugging Face API Key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HUGGINGFACE_API_KEY:
    raise ValueError("⚠️ ERROR: Hugging Face API Key is missing!")

# ✅ Create Flask app instance
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "LLaMA 3 Chatbot is running! 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is empty"}), 400

        # ✅ Send request to Hugging Face API (LLaMA 3)
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": user_message,
            "parameters": {"max_length": 200}
        }

        response = requests.post(
            "https://api-inference.huggingface.co/models/meta-llama/Llama-3-8B",
            headers=headers,
            json=payload
        )

        # ✅ Handle Response
        if response.status_code == 200:
            bot_reply = response.json()[0]["generated_text"]
        else:
            bot_reply = f"⚠️ API Error: {response.json()}"

        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"error": f"⚠️ Server Error: {str(e)}"}), 500

# ✅ Run Flask on the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

