from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ ERROR: Missing OpenAI API Key!")

openai.api_key = OPENAI_API_KEY

# ✅ Create Flask app instance
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# ✅ Health Check Route
@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running! 🚀"

# ✅ Chatbot API Route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # ✅ Simple product database
    PRODUCTS = {
        "vape": "Vapes are electronic devices that simulate smoking.",
        "cbd": "CBD is a natural compound found in cannabis with relaxing properties.",
    }

    # ✅ Check if user is asking about a product
    for product, details in PRODUCTS.items():
        if product in user_message.lower():
            return jsonify({"response": details})

    # ✅ Generate AI response using OpenAI API
    ai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    return jsonify({"response": ai_response["choices"][0]["message"]["content"]})

# ✅ Ensure Flask runs on the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render-assigned PORT
    app.run(host="0.0.0.0", port=port, debug=True)

