import streamlit as st
import requests
import json
import os

# Set the base URL for the API
# BASE_URL = "http://127.0.0.1:5000"  # Local development
BASE_URL = "https://lab7-97641147142.me-central1.run.app"  # Cloud deployment

st.set_page_config(
    page_title="Customer Support AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a feature:",
    ["Chat", "Query Categorization", "Medical Info Extraction", 
     "Mortgage Response", "Newsletter Analysis"]
)

# Function to call API endpoints
def call_api(endpoint, payload):
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error: {response.text}"
    except Exception as e:
        return None, f"Error: {str(e)}"

# Check if API is healthy
def check_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            st.sidebar.success("✅ API is online")
        else:
            st.sidebar.error("❌ API is offline")
    except:
        st.sidebar.error("❌ Cannot connect to API")

# Call health check
check_health()

# Chat page
if page == "Chat":
    st.title("💬 Customer Support Chat")
    st.write("Ask any customer support related question and get an AI-powered response.")
    
    # Input for user message
    user_message = st.text_area("Your question:", height=100)
    
    if st.button("Send", key="chat_send"):
        if user_message:
            with st.spinner("Getting response..."):
                payload = {"message": user_message}
                result, error = call_api("chat", payload)
                
                if error:
                    st.error(error)
                else:
                    st.subheader("Response:")
                    st.write(result["response"])
                    
                    # Display the raw JSON
                    with st.expander("View raw JSON"):
                        st.json(result)
        else:
            st.warning("Please enter a message.")

# Query Categorization page
elif page == "Query Categorization":
    st.title("🏦 Bank Query Categorization")
    st.write("Categorize customer inquiries for a bank's customer service team.")
    
    # Predefined categories for reference
    st.info("""
    **Available Categories:**
    - Account Management
    - Transaction Issues
    - Loan Services
    - Credit Cards
    - Online Banking
    - Fraud and Security
    - General Information
    - Other
    """)
    
    # Input options
    query_input_type = st.radio(
        "Input type:",
        ["Select from examples", "Enter custom query"]
    )
    
    if query_input_type == "Select from examples":
        example_queries = [
            "How do I open a new checking account?",
            "I noticed an unauthorized transaction on my account.",
            "What are the current interest rates for home loans?",
            "I want to apply for a credit card with rewards.",
            "I can't log into my online banking account.",
            "I think someone has stolen my debit card.",
            "What are your branch hours on weekends?"
        ]
        query = st.selectbox("Select an example query:", example_queries)
    else:
        query = st.text_area("Enter your query:", height=100)
    
    if st.button("Categorize", key="categorize_btn"):
        if query:
            with st.spinner("Categorizing..."):
                payload = {"query": query}
                result, error = call_api("categorize", payload)
                
                if error:
                    st.error(error)
                else:
                    st.subheader("Category:")
                    st.success(result["response"])
                    
                    # Display the raw JSON
                    with st.expander("View raw JSON"):
                        st.json(result)
        else:
            st.warning("Please enter or select a query.")

# Medical Info Extraction page
elif page == "Medical Info Extraction":
    st.title("🏥 Medical Information Extraction")
    st.write("Extract structured information from medical notes.")
    
    # Input options
    medical_input_type = st.radio(
        "Input type:",
        ["Use example", "Enter custom notes"]
    )
    
    if medical_input_type == "Use example":
        medical_notes = """
        A 60-year-old male patient, Mr. Johnson, presented with symptoms
        of increased thirst, frequent urination, fatigue, and unexplained
        weight loss. Upon evaluation, he was diagnosed with diabetes,
        confirmed by elevated blood sugar levels. Mr. Johnson's weight
        is 210 lbs. He has been prescribed Metformin to be taken twice daily
        with meals. It was noted during the consultation that the patient is
        a current smoker.
        """
    else:
        medical_notes = st.text_area("Enter medical notes:", height=200)
    
    # Display the notes
    st.subheader("Medical Notes:")
    st.write(medical_notes)
    
    if st.button("Extract Information", key="extract_btn"):
        if medical_notes:
            with st.spinner("Extracting information..."):
                payload = {"medical_notes": medical_notes}
                result, error = call_api("extract-medical", payload)
                
                if error:
                    st.error(error)
                else:
                    st.subheader("Extracted Information:")
                    
                    # Try to parse the JSON from the response
                    try:
                        extracted_data = json.loads(result["response"])
                        
                        # Create columns for displaying the data
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Age", extracted_data.get("age", "N/A"))
                            st.metric("Gender", extracted_data.get("gender", "N/A"))
                            st.metric("Diagnosis", extracted_data.get("diagnosis", "N/A"))
                        
                        with col2:
                            st.metric("Weight", f"{extracted_data.get('weight', 'N/A')} lbs" if extracted_data.get('weight') else "N/A")
                            st.metric("Smoking", extracted_data.get("smoking", "N/A"))
                    
                    except:
                        st.write(result["response"])
                    
                    # Display the raw JSON
                    with st.expander("View raw JSON"):
                        st.json(result)
        else:
            st.warning("Please enter medical notes.")

# Mortgage Response page
elif page == "Mortgage Response":
    st.title("🏠 Mortgage Inquiry Response")
    st.write("Generate personalized responses to mortgage-related inquiries.")
    
    # Display mortgage rates for reference
    with st.expander("View Current Mortgage Rates"):
        st.table({
            "Product": ["30-year fixed-rate", "20-year fixed-rate", "15-year fixed-rate", 
                       "10-year fixed-rate", "7-year ARM", "5-year ARM", "3-year ARM",
                       "30-year fixed-rate FHA", "30-year fixed-rate VA"],
            "Interest Rate": ["6.403%", "6.329%", "5.705%", "5.500%", "7.011%", 
                             "6.880%", "6.125%", "5.527%", "5.684%"],
            "APR": ["6.484%", "6.429%", "5.848%", "5.720%", "7.660%", 
                   "7.754%", "7.204%", "6.316%", "6.062%"]
        })
    
    # Input options
    email_input_type = st.radio(
        "Input type:",
        ["Select from examples", "Enter custom email"]
    )
    
    if email_input_type == "Select from examples":
        example_emails = [
            """
            Dear mortgage lender,
            
            What's your 30-year fixed-rate APR, and how does it compare to the 15-year
            fixed rate? I'm trying to decide which term would be better for me.
            
            Best regards,
            John
            """,
            """
            Hello,
            
            I'm interested in an FHA loan. Could you tell me what the current rates are
            and what the requirements are for qualification?
            
            Thanks,
            Sarah
            """,
            """
            To whom it may concern,
            
            I'm comparing different ARM options. Can you explain the differences between
            your 3-year, 5-year, and 7-year ARMs?
            
            Regards,
            Michael
            """
        ]
        email_index = st.selectbox("Select an example email:", range(len(example_emails)), 
                                 format_func=lambda i: f"Example {i+1}")
        email = example_emails[email_index]
    else:
        email = st.text_area("Enter customer email:", height=200)
    
    # Display the email
    st.subheader("Customer Email:")
    st.text(email)
    
    if st.button("Generate Response", key="mortgage_btn"):
        if email:
            with st.spinner("Generating response..."):
                payload = {"email": email}
                result, error = call_api("mortgage-response", payload)
                
                if error:
                    st.error(error)
                else:
                    st.subheader("Generated Response:")
                    st.write(result["response"])
                    
                    # Display the raw JSON
                    with st.expander("View raw JSON"):
                        st.json(result)
        else:
            st.warning("Please enter an email.")

# Newsletter Analysis page
elif page == "Newsletter Analysis":
    st.title("📰 Newsletter Analysis")
    st.write("Analyze a newsletter and generate a comprehensive report.")
    
    # Input options
    newsletter_input_type = st.radio(
        "Input type:",
        ["Use example", "Enter custom newsletter"]
    )
    
    if newsletter_input_type == "Use example":
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
    else:
        newsletter = st.text_area("Enter newsletter content:", height=300)
    
    # Display the newsletter
    st.subheader("Newsletter Content:")
    st.write(newsletter)
    
    if st.button("Analyze", key="newsletter_btn"):
        if newsletter:
            with st.spinner("Analyzing newsletter... This may take a minute."):
                payload = {"newsletter": newsletter}
                result, error = call_api("analyze-newsletter", payload)
                
                if error:
                    st.error(error)
                else:
                    st.subheader("Analysis Report:")
                    st.markdown(result["response"])
                    
                    # Display the raw JSON
                    with st.expander("View raw JSON"):
                        st.json(result)
        else:
            st.warning("Please enter newsletter content.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **About this app**
    
    This app demonstrates various AI capabilities using Mistral AI.
    
    Built with:
    - Flask (Backend)
    - Streamlit (Frontend)
    - Mistral AI (Language Model)
    """
) 