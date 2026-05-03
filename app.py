import streamlit as st
import google.generativeai as genai
import PIL.Image
import os

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Saravan's Metabolic Navigator", page_icon="🥗")

# Sidebar for Setup
try:
    api_key = st.secrets["GEMINI_KEY"]
except:
    st.error("API Key not found in secrets.toml!")
    st.stop()

# --- AGENT LOGIC ---
SYSTEM_INSTRUCTIONS = """
You are an empathetic, non-judgmental Metabolic Health Agent. 
Your goal is to reduce decision fatigue for a user managing a high BMI and joint pain.
1. Prioritize Low Impact: Never suggest high-impact exercises. 
2. Kitchen Efficiency: Suggest recipes with minimal standing time.
3. Tone: Be encouraging. Use 'we' instead of 'you'.
"""

def analyze_meal(uploaded_image, key):
    if not key:
        st.error("Please enter your API Key in the sidebar!")
        return None
    
    genai.configure(api_key=key)
    # Using the model name we found in your list earlier
    model = genai.GenerativeModel(
        model_name='models/gemini-3-flash-preview',
        system_instruction=SYSTEM_INSTRUCTIONS
    )
    
    img = PIL.Image.open(uploaded_image)
    prompt = "Identify this meal. Provide a 'Joint-Friendly' rating (1-10) and a tip for BMI management."
    
    with st.spinner('Agent is analyzing your meal...'):
        response = model.generate_content([prompt, img])
        return response.text

# --- USER INTERFACE ---
st.title("🥗 Saravan's Metabolic Navigator")
st.write("Take a photo of your meal for an instant health & joint-impact check.")

# Camera/Upload Widget
img_file = st.camera_input("Capture your meal") # This opens the camera on your phone!

if img_file is not None:
    # Display the analysis
    st.subheader("Agent's Analysis")
    result = analyze_meal(img_file, api_key)
    
    if result:
        st.markdown(result)
        
        # Proactive Step 4/5 Logic (Mocked for UI)
        st.divider()
        st.info("💡 **Proactive Tip:** It's humid outside today. If you feel ankle pressure, try 5 minutes of seated leg lifts after this meal.")
