import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
import io

st.set_page_config(page_title="Image Q&A with Gemini", layout="wide")

st.markdown("""
## Image Q&A with Google's Gemini Pro

This app allows you to upload an image, ask a question about it, and get insights using Google's Gemini Pro AI model.

### How It Works

1. **Enter Your API Key**: You'll need a Google API key to access Gemini Pro.
    You can get yours from here: https://aistudio.google.com/app/apikey
2. **Upload Your Image**: Upload any image you want to ask questions about.
3. **Ask a Question**: Ask a question related to the image, and the AI will provide an answer.
""")

# Input for API key
api_key = st.text_input("Enter your Google API Key:", type="password", key="api_key_input")

# Set the API key for Google Generative AI
genai.configure(api_key=api_key)

def get_gemini_response(img_file, question):
    # with open(image_path, "rb") as img_file:
    # image_data = img_file.read()

    image = Image.open(img_file)

    # Choose a Gemini API model.
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content([image, "Prompt: "+question])

    # # Make the request to the Gemini API
    # response = model.generate_content(
    #     prompt=f"Question: {question}",
    #     image=image  # Assuming the API can accept image data
    # )
    
    return response

def main():
    st.header("Ask Questions about Your Image 💁")

    # File uploader for image
    image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"], key="image_uploader")

    # Text input for the question
    user_question = st.text_input("Ask a Question about the Image", key="user_question")

    if image_file and user_question and api_key:
        # Display the uploaded image
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        with st.spinner("Processing..."):
            # Call the Gemini API with the image and question
            response = get_gemini_response(image_file, user_question)
            st.write("Reply: ", response.text)
            # st.write("Reply: ", response.get('output', 'No response received'))

if __name__ == "__main__":
    main()
