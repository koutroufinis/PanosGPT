import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq

# Create Flask app
app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)

# Get API key from environment variable (Render.com) or from set.json (local)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# If not found in environment, try to load from set.json (for local development)
if not GROQ_API_KEY:
    try:
        with open("set.json", "r") as f:
            settings = json.load(f)
            GROQ_API_KEY = settings[0]["GROQ_API_KEY"]
        print("📁 Using API key from set.json")
    except FileNotFoundError:
        print("❌ Error: GROQ_API_KEY not found in environment and set.json is missing!")
        print("💡 Please set GROQ_API_KEY environment variable or create set.json")
        exit(1)

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

@app.route("/")
def serve_index():
    """Serve the main chat interface."""
    try:
        return send_from_directory(".", "index.html")
    except Exception as e:
        return f"Error loading index.html: {str(e)}", 404

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
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": user_message}],
        )
        answer = response.choices[0].message.content
        
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    """Health check endpoint for Render.com."""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 PanosGPT Server Starting...")
    print("=" * 50)
    print(f"📡 Server will run at: http://localhost:5000")
    print("🔑 API Key configured: Yes")
    print("💡 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Get port from environment variable for Render.com compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
