# This code is part of a Streamlit application that uses Google Generative AI to analyze invoices.
# It allows users to upload an invoice image and ask questions about it, receiving answers based on the image content.
# Make sure to set the GOOGLE_API_KEY in your environment variables before running this app.
from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Initialize the Google Generative AI client with the API key
# Ensure you have set the GOOGLE_API_KEY in your environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get response from Gemini Pro Vision model
def get_gemini_response(input_text, image_parts, prompt):
    response = model.generate_content([
        {"text": input_text},
        image_parts[0],     
        {"text": prompt}
    ])
    return response.text

# Function to handle image input and convert it to the required format
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No image file uploaded.")

# Streamlit app configuration
st.set_page_config(page_title="Multi Language Invoice Analysis", page_icon=":robot_face:", layout="wide")
st.title("Multi Language Invoice Analysis")
st.header("Upload your invoice image")

# Input fields for user query and image upload
input_text = st.text_input("Enter your query about the invoice")
upload_image = st.file_uploader("Upload an image of the invoice", type=["jpg", "jpeg", "png"])

# Display the uploaded image if available
if upload_image is not None:
    pil_image = Image.open(upload_image)
    st.image(pil_image, caption="Uploaded Invoice Image", use_column_width=True)

submit_button = st.button("Tell me about the invoice")

input_prompt = (
    "You are a helpful AI assistant and expert in understanding invoices. "
    "We will provide you an image of an invoice and a query about the invoice. "
    "You need to answer the query based on the invoice image. Here is the query: "
    + input_text
)

if submit_button and upload_image is not None and input_text:
    image_data = input_image_details(upload_image)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("Response from Gemini Pro Vision:")
    st.write(response)
