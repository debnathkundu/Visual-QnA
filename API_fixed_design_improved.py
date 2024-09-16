import streamlit as st
from PIL import Image, UnidentifiedImageError
import google.generativeai as genai
import time

# Set page config with a wide layout
st.set_page_config(page_title="Image Q&A with Gemini", layout="wide")

st.markdown("""
## Image Q&A with Google's Gemini Pro

This app allows you to upload an image, ask a question about it, and get insights using Google's Gemini Pro AI model or another model.

### How It Works

1. **Upload Your Image**: Upload any image you want to ask questions about.
2. **Ask a Question**: Ask a question related to the image, and the AI will provide an answer.
""")

# Pre-set the API key for Google Generative AI (not visible in frontend)
API_KEY = "AIzaSyBLtzFFE5L5vGA" + "Kq0F2iI3sRzcivJlrjPE"

# Set the API key for Google Generative AI
genai.configure(api_key=API_KEY)

# Function for Gemini Pro
def get_gemini_response(img_file, question):
    # Open the image using PIL
    image = Image.open(img_file)

    # Choose a Gemini API model.
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content([image, "Prompt: "+question])
    
    return response

# Function for another model (Dummy logic for now)
def get_another_model_response(img_file, question):
    # Simulating a different model's logic
    # For example, this could be a local model or a REST API call to another service
    # In this example, we return a simple placeholder answer
    time.sleep(2)  # Simulate a processing delay
    return f"Another model's answer to the question: '{question}' based on the image."

# Retry logic for Gemini
def get_gemini_response_with_retry(img_file, question, retries=3, delay=2):
    for i in range(retries):
        try:
            return get_gemini_response(img_file, question)
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e

# Main logic for the app
def main():
    # Header for the main content
    st.header("Ask Questions about Your Image 💁")

    # Sidebar for inputs
    with st.sidebar:
        st.title("Upload and Question")
        
        # Selectbox to choose model type
        model_choice = st.selectbox('Select AI Model', ['Google Gemini Pro', 'Another Model'])

        # File uploader for image
        image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"], key="image_uploader")

        # Text input for the question
        user_question = st.text_input("Ask a Question about the Image", key="user_question")

    # Only process the image and question if both are provided
    if image_file and user_question:
        try:
            # Try to open the image file and display it
            image = Image.open(image_file)
            # Display image with reduced size
            st.image(image, caption="Uploaded Image", width=400)

            with st.spinner("Processing..."):
                if model_choice == 'Google Gemini Pro':
                    # Call the Gemini API with the image and question
                    response = get_gemini_response_with_retry(image_file, user_question)
                    st.write("Reply: ", response.text)
                
                elif model_choice == 'Another Model':
                    # Call the other model logic
                    response = get_another_model_response(image_file, user_question)
                    st.write("Reply: ", response)

        except UnidentifiedImageError:
            st.error("Error: The uploaded file is not a valid image. Please upload a JPG, JPEG, or PNG file.")

if __name__ == "__main__":
    main()
