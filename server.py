import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq

# Load settings
with open("set.json", "r") as f:
    settings = json.load(f)
DEFAULT_API_KEY = settings[0]["GROQ_API_KEY"]

# Create Flask app
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Global client using default key
default_client = Groq(api_key=DEFAULT_API_KEY)

@app.route("/")
def serve_index():
    """Serve the main chat interface."""
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Accept a user message and returns the assistant's response.
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = default_client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": user_message}],
        )
        answer = response.choices[0].message.content
        
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 PanosGPT Server Starting...")
    print("=" * 50)
    print(f"📡 Server will run at: http://localhost:5000")
    print("🔑 Using API key from set.json")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Get port from environment variable for Render.com compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)