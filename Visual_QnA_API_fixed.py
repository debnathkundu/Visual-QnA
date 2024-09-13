import streamlit as st
from PIL import Image, UnidentifiedImageError
import google.generativeai as genai
import os
import io
import time

st.set_page_config(page_title="Image Q&A with Gemini", layout="wide")

st.markdown("""
## Image Q&A with Google's Gemini Pro

This app allows you to upload an image, ask a question about it, and get insights using Google's Gemini Pro AI model.

### How It Works

1. **Upload Your Image**: Upload any image you want to ask questions about.
2. **Ask a Question**: Ask a question related to the image, and the AI will provide an answer.
""")

# Pre-set the API key for Google Generative AI (not visible in frontend)
API_KEY = "AIzaSyBLtzFFE5L5vGA" + "Kq0F2iI3sRzcivJlrjPE"

# Set the API key for Google Generative AI
genai.configure(api_key=API_KEY)

def get_gemini_response(img_file, question):
    # Open the image using PIL
    image = Image.open(img_file)

    # Choose a Gemini API model.
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content([image, "Prompt: "+question])
    
    return response

def get_gemini_response_with_retry(img_file, question, retries=3, delay=2):
    for i in range(retries):
        try:
            return get_gemini_response(img_file, question)
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e

def main():
    st.header("Ask Questions about Your Image 💁")

    # File uploader for image
    image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"], key="image_uploader")

    # Text input for the question
    user_question = st.text_input("Ask a Question about the Image", key="user_question")

    if image_file and user_question:
        try:
            # Try to open the image file and display it
            image = Image.open(image_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            with st.spinner("Processing..."):
                # Call the Gemini API with the image and question
                # response = get_gemini_response(image_file, user_question)

                response = get_gemini_response_with_retry(image_file, user_question)

                st.write("Reply: ", response.text)
        
        except UnidentifiedImageError:
            st.error("Error: The uploaded file is not a valid image. Please upload a JPG, JPEG, or PNG file.")

if __name__ == "__main__":
    main()







