from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

st.set_page_config(page_title="Multilanguage Invoice Extractor", page_icon=":robot:")
st.header("Multilanguage Invoice Extractor")
input = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the Invoice...",type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """ 
You are an expert in understanding invoices. We will upload a image as invoice and you
will have to answer any questions based on the uploaded invoice image
"""
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is ")
    st.write(response)

