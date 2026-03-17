import google.generativeai as genai
from PIL import Image
import json
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
genai.configure(api_key=api_key)
def generate_guidance(damage_report, reference_image_paths, ref_meta=None):
    model = genai.GenerativeModel("gemini-3-flash-preview")

    # build source info string
    source_info = ""
    if ref_meta:
        source_info = "\nReference sources:\n" + "\n".join(
            [f"- {r['title']} ({r['source']})" for r in ref_meta]
        )

    prompt = f"""
    You are assisting a 3D artist in reconstructing a broken murti (Hindu idol/statue) in Blender.
    
    Damage report:
    {json.dumps(damage_report, indent=2)}
    {source_info}
    
    The attached images are similar intact murtis retrieved as references.
    
    Please provide:
    1. Step-by-step reconstruction guidance for Blender
    2. Which reference image looks most useful and why
    3. Approximate proportions or geometry hints for the missing parts
    4. Any symmetry or mirroring tips that apply
    5. Suggested Blender tools or modifiers to use (e.g. Mirror, Sculpt, Subdivide)
    
    Keep it practical and specific for a Blender 3D artist.
    Be concise but thorough.
    """

    # load reference images that exist
    content = [prompt]
    for path in reference_image_paths[:2]:  # max 2 to stay within free tier limits
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                content.append(img)
            except Exception as e:
                print(f"Could not load reference image {path}: {e}")

    response = model.generate_content(content)
    return response.text