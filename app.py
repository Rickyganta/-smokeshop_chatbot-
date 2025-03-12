from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this

import openai
import os
from dotenv import load_dotenv

# Load API Key securely
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running! 🚀"

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample product database
PRODUCTS = {
    "vape": "We offer a variety of vapes including disposable vapes, pod systems, and mods.",
    "e-liquid": "Our e-liquids come in different nicotine levels and flavors.",
    "kratom": "We have high-quality kratom in powder and capsule forms.",
    "cbd": "Our CBD products include tinctures, gummies, and vapes."
}

# Function to get AI response
def get_chatbot_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant for a smoke shop."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message", "")

    # Check if user is asking about a product
    for product, details in PRODUCTS.items():
        if product in user_input.lower():
            return jsonify({"response": details})

    # Get AI-generated response
    ai_response = get_chatbot_response(user_input)
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=True)

