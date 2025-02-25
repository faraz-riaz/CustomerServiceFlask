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

@app.route('/categorize', methods=['POST'])
def categorize_query():
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        prompt = f"""
        You are an AI assistant trained to support a bank's customer service team. Your task is to categorize customer inquiries into one of the 
        following predefined categories:

        Account Management: Questions related to opening, closing, or managing bank accounts.
        Transaction Issues: Inquiries about unauthorized charges, failed transactions, or disputes.
        Loan Services: Requests for information on personal, home, or auto loans.
        Credit Cards: Queries about credit card applications, benefits, or billing.
        Online Banking: Issues related to internet banking, mobile app access, or technical support.
        Fraud and Security: Reports of suspicious activity or questions about account security.
        General Information: Requests for branch locations, operating hours, or bank policies.

        Given the customer inquiry below, determine the most appropriate category from the list above. If the inquiry doesn't fit any category, 
        classify it as 'Other'

        Query: {query}
        """

        messages = [ChatMessage(role="user", content=prompt)]
        response = mistral_client.chat(
            model=Config.CHAT_MODEL,
            messages=messages
        )

        return jsonify({
            'response': response.choices[0].message.content,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/extract-medical', methods=['POST'])
def extract_medical_info():
    try:
        data = request.json
        medical_notes = data.get('medical_notes')
        
        if not medical_notes:
            return jsonify({'error': 'No medical notes provided'}), 400

        prompt = f"""
        Extract information from the following medical notes:
        {medical_notes}
        Return json format with the following JSON schema:
        {{
        "age": {{
        "type": "integer"
        }},
        "gender": {{
        "type": "string",
        "enum": ["male", "female", "other"]
        }},
        "diagnosis": {{
        "type": "string",
        "enum": ["migraine", "diabetes", "arthritis", "acne"]
        }},
        "weight": {{
        "type": "integer"
        }},
        "smoking": {{
        "type": "string",
        "enum": ["yes", "no"]
        }}
        }}
        """

        messages = [ChatMessage(role="user", content=prompt)]
        response = mistral_client.chat(
            model=Config.CHAT_MODEL,
            messages=messages
        )

        return jsonify({
            'response': response.choices[0].message.content,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/mortgage-response', methods=['POST'])
def mortgage_response():
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'No email provided'}), 400

        prompt = f"""
        You are a mortgage lender customer service bot, and your task is to
        create personalized email responses to address customer questions.
        Answer the customer's inquiry using the provided facts below. Ensure
        that your response is clear, concise, and directly addresses the
        customer's question. Address the customer in a friendly and
        professional manner. Sign the email with "Lender Customer Support."

        # Facts
        30-year fixed-rate: interest rate 6.403%, APR 6.484%
        20-year fixed-rate: interest rate 6.329%, APR 6.429%
        15-year fixed-rate: interest rate 5.705%, APR 5.848%
        10-year fixed-rate: interest rate 5.500%, APR 5.720%
        7-year ARM: interest rate 7.011%, APR 7.660%
        5-year ARM: interest rate 6.880%, APR 7.754%
        3-year ARM: interest rate 6.125%, APR 7.204%
        30-year fixed-rate FHA: interest rate 5.527%, APR 6.316%
        30-year fixed-rate VA: interest rate 5.684%, APR 6.062%

        # Email
        {email}
        """

        messages = [ChatMessage(role="user", content=prompt)]
        response = mistral_client.chat(
            model=Config.CHAT_MODEL,
            messages=messages
        )

        return jsonify({
            'response': response.choices[0].message.content,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/analyze-newsletter', methods=['POST'])
def analyze_newsletter():
    try:
        data = request.json
        newsletter = data.get('newsletter')
        
        if not newsletter:
            return jsonify({'error': 'No newsletter provided'}), 400

        prompt = f"""
        You are a commentator. Your task is to write a report on a newsletter.
        When presented with the newsletter, come up with interesting questions to ask,
        and answer each question.
        Afterward, combine all the information and write a report in the markdown
        format.

        # Newsletter:
        {newsletter}

        # Instructions:
        ## Summarize:
        In clear and concise language, summarize the key points and themes
        presented in the newsletter.
        ## Interesting Questions:
        Generate three distinct and thought-provoking questions that can be
        asked about the content of the newsletter. For each question:
        - After "Q: ", describe the problem
        - After "A: ", provide a detailed explanation of the problem addressed
        in the question.
        - Enclose the ultimate answer in <>.
        ## Write a analysis report
        Using the summary and the answers to the interesting questions,
        create a comprehensive report in Markdown format.
        """

        messages = [ChatMessage(role="user", content=prompt)]
        response = mistral_client.chat(
            model=Config.CHAT_MODEL,
            messages=messages
        )

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