import requests
import json

BASE_URL = "https://lab7-97641147142.me-central1.run.app"

def try_endpoint(url, payload, endpoint_name=""):
    try:
        response = requests.post(url, json=payload)
        print(f"\nRequest to {endpoint_name}:")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response: {json.dumps(response_data, indent=2)}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {url}. Make sure the service is running.")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("-" * 50)

def test_chat_endpoint():
    url = f"{BASE_URL}/chat"
    test_messages = [
        "How do I reset my password?",
        "What are your business hours?",
        "I need help with my order"
    ]
    
    print("\nTesting Chat API Endpoint...")
    for message in test_messages:
        try_endpoint(url, {"message": message}, "Chat API")

def test_categorize_endpoint():
    url = f"{BASE_URL}/categorize"
    test_queries = [
        "How can I get a credit card?",
        "I want to open a new account",
        "My card was stolen"
    ]
    
    print("\nTesting Categorize API Endpoint...")
    for query in test_queries:
        try_endpoint(url, {"query": query}, "Categorize API")

def test_medical_endpoint():
    url = f"{BASE_URL}/extract-medical"
    medical_notes = """
    A 60-year-old male patient, Mr. Johnson, presented with symptoms
    of increased thirst, frequent urination, fatigue, and unexplained
    weight loss. Upon evaluation, he was diagnosed with diabetes,
    confirmed by elevated blood sugar levels. Mr. Johnson's weight
    is 210 lbs. He has been prescribed Metformin to be taken twice daily
    with meals. It was noted during the consultation that the patient is
    a current smoker.
    """
    
    print("\nTesting Medical Extraction API Endpoint...")
    try_endpoint(url, {"medical_notes": medical_notes}, "Medical API")

def test_mortgage_endpoint():
    url = f"{BASE_URL}/mortgage-response"
    email = """
    Dear mortgage lender,

    What's your 30-year fixed-rate APR, and how does it compare to the 15-year
    fixed rate? I'm trying to decide which term would be better for me.

    Best regards,
    John
    """
    
    print("\nTesting Mortgage Response API Endpoint...")
    try_endpoint(url, {"email": email}, "Mortgage API")

def test_newsletter_endpoint():
    url = f"{BASE_URL}/analyze-newsletter"
    newsletter = """
    Q3 2023 Market Update

    The third quarter saw significant developments in the tech sector, with AI 
    continuing to dominate headlines. Major companies announced new AI products,
    while concerns about AI safety led to increased calls for regulation.

    In financial markets, inflation showed signs of cooling, though central banks
    maintained their hawkish stance. The S&P 500 experienced volatility but
    ended the quarter with modest gains.

    The real estate market remained challenging due to high interest rates,
    with home sales declining in most regions. However, rental markets showed
    strength in urban areas.
    """
    
    print("\nTesting Newsletter Analysis API Endpoint...")
    try_endpoint(url, {"newsletter": newsletter}, "Newsletter API")

def test_health_endpoint():
    url = f"{BASE_URL}/health"
    
    print("\nTesting Health Check Endpoint...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {url}. Make sure the service is running.")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    print("-" * 50)

if __name__ == "__main__":
    # Test all endpoints
    test_health_endpoint()
    test_chat_endpoint()
    test_categorize_endpoint()
    test_medical_endpoint()
    test_mortgage_endpoint()
    test_newsletter_endpoint() 