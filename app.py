import streamlit as st
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import langsmith

# Load environment variables
load_dotenv()

# LangSmith Tracking (if needed)
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# Define Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to user queries."),
        ("user", "Question: {question}")
    ]
)

# Define function to generate response
def generate_response(question, api_key, model_name, temperature, max_tokens):
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    # Initialize the Gemini model
    model = genai.GenerativeModel(model_name=model_name)

    # Generate response from Gemini
    response = model.generate_content(question, generation_config={"temperature": temperature, "max_output_tokens": max_tokens})
    
    # Extract and return the text response
    return response.text if response and hasattr(response, "text") else "No response generated."

# Streamlit App Title
st.title("Enhanced Q&A Chatbot with Gemini")

# Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

# Select the Gemini model
model_name = st.sidebar.selectbox("Select Gemini Model", ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro","gemini-2.0-pro-exp-02-05"])

# Adjust response parameters
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=600, value=150)

# User input section
st.write("Go ahead and ask any question:")
user_input = st.text_input("You:")

# Process user input
if user_input and api_key:
    response = generate_response(user_input, api_key, model_name, temperature, max_tokens)
    st.write("**Assistant:**", response)

elif user_input:
    st.warning("Please enter the Gemini API Key in the sidebar.")

custom_footer = """
    <style>
    .footer {
        position: scroll;
        bottom: 0;
        width: 100%;
        background-color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: white;
        border:2px solid white;
        border-radius:10px;
    }
    </style>
    <div class="footer">
        Developed by <b>Laavanjan</b> | © Faculty of IT B22
    </div>
"""
st.markdown(custom_footer, unsafe_allow_html=True)

else:
    st.write("Please provide a question.")

