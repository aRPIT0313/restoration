import os
import google.generativeai as genai
from PIL import Image
import json
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)
def analyze_damage(image_path):
    model = genai.GenerativeModel("gemini-3-flash-preview")
    image = Image.open(image_path)

    prompt = """
    Analyze this image of a broken murti (Hindu idol/statue).
    Identify and return a JSON with:
    {
      "damaged_regions": ["list of broken parts"],
      "missing_parts": ["parts that appear missing"],
      "damage_severity": "low/medium/high",
      "murti_type": "your best guess e.g. Ganesh, Shiva, etc.",
      "pose_description": "brief description of pose",
      "reconstruction_priority": ["ordered list of what to fix first"]
    }
    Return only valid JSON, no extra text.
    """

    response = model.generate_content([prompt, image])
    
    # clean and parse JSON
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)