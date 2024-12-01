import streamlit as st
from PIL import Image
import pyttsx3
import os
import pytesseract  
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI
import logging
import streamlit as st

# Suppress Streamlit warnings
logging.getLogger("streamlit").setLevel(logging.ERROR)


# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Google Generative AI with API Key
GEMINI_API_KEY = "GEMINI_API_KEY"  # Replace with your valid API key
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Custom CSS and markdown for the app
st.markdown(
    """
    <style>
     .main-title {
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #003399;
        margin-top: -10px;
     }
    .subtitle {
        font-size: 18px;
        color: #444;
        text-align: center;
        margin-bottom: 25px;
    }
    .section-title {
        font-size: 24px;
        color: #222;
        font-weight: bold;
    }
    .icon-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .icon {
        font-size: 30px;
        text-align: center;
        color: #003399;
        cursor: pointer;
    }
    .icon:hover {
        color: #0066cc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title and Subtitle
st.markdown('<div class="main-title">AudibleVision 🔉👓</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle" style="color: white;">Enabling visually impaired individuals to navigate and understand their environment through AI-based scene interpretation, text extraction, and auditory assistance.</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="icon-container">
        <div class="icon" style="font-size: 18px;">AI-based scene interpretation🖼️</div>
        <div class="icon" style="font-size: 18px;">Extract Text📄</div>
        <div class="icon" style="font-size: 18px;">Auditory Assistance 🔉</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Sidebar with "About" section always displayed
st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
    """
    **Key Features**:
    - 🖼️ **Scene Insights**: Detailed descriptions of uploaded images.
    - 📄 **Text Extraction**: Extract written text from the image.
    - 🔉 **Voice Output**: Listen to the text content via audio.

    **Why This App?**:
    - Enhances accessibility for individuals with visual challenges.
    - Combines image analysis, OCR, and audio feedback seamlessly.

    **Technology Stack**:
    - Google Gemini for AI-based scene understanding.
    - Tesseract for Optical Character Recognition (OCR).
    - pyttsx3 for converting text to speech.
    """
)

# Core functions for processing
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Image upload section
st.markdown("<h3 class='section-title' style='color: #FF6347;'>📤 Upload Your Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose an image file (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Feature buttons
st.markdown("<h3 class='section-title'style='color: #FF5555;'>🛠️ Choose a Feature</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🔍 Analyze Scene\n And Provide Assistance ")
ocr_button = col2.button("📄 Extract Text from image")
tts_button = col3.button("🔉 Convert  Text to Speech")

# Input prompt for AI description
input_prompt = """
You are an AI assistant supporting visually impaired individuals. Describe the image by:
1. Listing detected items and their purposes.
2. Providing a brief overall description.
3. Suggesting precautions or assistance relevant to the content.
"""

# Handling user actions
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Analyzing the image..."):
            response = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='section-title'>🔍 Scene Analysis</h3>", unsafe_allow_html=True)
            st.write(response)

    if ocr_button:
        with st.spinner("Extracting text from the image..."):
            text = extract_text_from_image(image)
            st.markdown("<h3 class='section-title'>📄 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Text Content", text, height=150)

    if tts_button:
        with st.spinner("Converting text to audio..."):
            text = extract_text_from_image(image)
            if text.strip():
                text_to_speech(text)
                st.success("✅ Audio Conversion Complete!")
            else:
                st.warning("No text detected for audio conversion.")


st.markdown(
    """
    <style>
    /* Fixed Footer */
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 16px;
        color: #333;
        z-index: 1000;
        left: 0;
    }
    </style>
    <div class="footer">
        AudibleVision | Powered by GenAI | ©️ Sanket Darekar | Enhancing accessibility through innovation. 🚀
    </div>
    """,
    unsafe_allow_html=True
)
