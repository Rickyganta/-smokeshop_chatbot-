from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from openai import OpenAIError  # ✅ Correct OpenAI error handling

# ✅ Load API Key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ ERROR: OpenAI API Key is missing!")

openai.api_key = OPENAI_API_KEY

# ✅ Create Flask app instance
app = Flask(__name__)
CORS(app)

# ✅ Health check route
@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running! 🚀"

# ✅ Chatbot API Route with Corrected Error Handling
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        # ✅ Validate user message
        if not user_message:
            return jsonify({"error": "Message is empty"}), 400

        # ✅ Ensure OpenAI API Key is set
        if not OPENAI_API_KEY:
            return jsonify({"error": "Missing OpenAI API Key"}), 500

        # ✅ Send request to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        # ✅ Ensure response exists
        if "choices" in response and len(response["choices"]) > 0:
            bot_reply = response["choices"][0]["message"]["content"]
        else:
            bot_reply = "⚠️ No valid response from OpenAI."

        return jsonify({"response": bot_reply})
    
    except OpenAIError as e:  # ✅ Catch OpenAI-specific errors
        return jsonify({"error": f"OpenAI API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

# ✅ Ensure Flask runs on the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

