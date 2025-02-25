from flask import Flask, request, jsonify
from flask_cors import CORS
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from config import Config

app = Flask(__name__)
CORS(app)

# Initialize Mistral client
mistral_client = MistralClient(api_key=Config.MISTRAL_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Create system message for customer support context
        system_message = """You are a helpful customer support assistant. 
        Provide clear, concise, and friendly responses to customer inquiries. 
        If you're unsure about something, be honest and suggest escalating to a human agent."""

        # Create chat messages
        messages = [
            ChatMessage(role="system", content=system_message),
            ChatMessage(role="user", content=user_message)
        ]

        # Get response from Mistral AI
        response = mistral_client.chat(
            model=Config.CHAT_MODEL,
            messages=messages
        )

        # Access the response content correctly
        return jsonify({
            'response': response.choices[0].message.content,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True) 