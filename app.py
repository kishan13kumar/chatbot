import streamlit as st
import os
import google.generativeai as ai
from PIL import Image

# Configure the Google Generative AI API with the provided API key
api_key = "AIzaSyB2iS8tkkefGvFPjF-d2r36dnehRX_LJ_4"
ai.configure(api_key=api_key)

# Initialize the generative model
model = ai.GenerativeModel("text")

def gemini_response(query, image_path):
    if query:
        response = model.generate_content([query, image_path])
    else:
        response = model.generate_content([image_path])
    return response

st.set_page_config(page_title="Content Generation")

st.header("Content Creation Bot")

upload_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "gif", "bmp"])

image = None

if upload_file is not None:
    image = Image.open(upload_file)
    st.image(image, caption="Uploaded image", use_column_width=True)
    # Save the uploaded image to a temporary path
    image_path = "temp_image." + upload_file.name.split('.')[-1]
    image.save(image_path)
else:
    image_path = None

input_query = st.text_input("Input", key="input")

submit = st.button("Generate Content")

if submit and image_path:
    with st.spinner('Generating content...'):
        try:
            response = gemini_response(input_query, image_path)
            st.success("Content generated successfully!")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    if submit:
        st.warning("Please upload an image to proceed.")
