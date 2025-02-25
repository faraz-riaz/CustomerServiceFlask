import requests
import json

def test_chat_endpoint():
    # API endpoint URL
    url = "http://localhost:5000/chat"
    
    # Test cases with different messages
    test_messages = [
        "How do I reset my password?",
        "What are your business hours?",
        "I need help with my order"
    ]
    
    print("Testing Chat API Endpoint...")
    print("-" * 50)
    
    for message in test_messages:
        # Prepare the request payload
        payload = {
            "message": message
        }
        
        try:
            # Make POST request to the chat endpoint
            response = requests.post(url, json=payload)
            
            # Print request and response details
            print(f"\nRequest Message: {message}")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"AI Response: {response_data['response']}")
            else:
                print(f"Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to {url}. Make sure the Flask server is running.")
        except Exception as e:
            print(f"Error: {str(e)}")
            
        print("-" * 50)

def test_health_endpoint():
    # Health check endpoint URL
    url = "http://localhost:5000/health"
    
    print("\nTesting Health Check Endpoint...")
    print("-" * 50)
    
    try:
        # Make GET request to the health endpoint
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {url}. Make sure the Flask server is running.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # First test the health endpoint
    test_health_endpoint()
    
    # Then test the chat endpoint
    test_chat_endpoint() 