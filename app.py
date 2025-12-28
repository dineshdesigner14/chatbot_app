from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

SYSTEM_PROMPT = """
You are a friendly and helpful AI assistant named GroqBot. 
Keep your responses concise and engaging. Respond to the user's latest message based on the entire conversation history provided.
"""

app = Flask(__name__)

# --- Initialize the Groq Client ---
# Initialize 'client' to None outside the try block
client = None
try:
    # Attempt to create the client object
    client = OpenAI(
        api_key=os.environ.get("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1" 
    )
except Exception as e:
    # If initialization fails, 'client' remains None.
    print(f"Error initializing Groq client: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Check if the client was successfully initialized before use
        if client is None:
            return jsonify({"status": "error", "message": "API Client is not configured. Check the GROQ_API_KEY environment variable."}), 500
        
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({"status": "error", "message": "No conversation history provided"}), 400

        full_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        full_messages.extend(messages)

        # --- Groq API Call ---
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=full_messages,
            temperature=0.7 
        )

        llm_reply = response.choices[0].message.content.strip()

        return jsonify({
            "status": "success",
            "reply": llm_reply
        })

    except Exception as e:
        # Catches API errors (401, 429) if client is defined and running
        return jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}), 500



# ✅ THIS MUST BE THE LAST PART OF THE FILE
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
