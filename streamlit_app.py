import streamlit as st
import urllib.parse
from PIL import Image
import requests
from io import BytesIO

# --- App Configuration ---
st.set_page_config(page_title="Free AI Image Generator", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.title("🧠 AI Image Generator")
    st.markdown(
        """
        Generate AI art instantly using **Pollinations**, a free, open-source tool powered by public models.
        
        
        🔗 [Pollinations GitHub](https://github.com/pollinations/pollinations)

        👨‍💻 Built with [Streamlit](https://streamlit.io) 

        ---
        **Created by:** [Anushka](https://github.com/hive0372) 
        """
    )

# --- Initialize session state for history ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Main Layout ---
st.title("🖼️ Image Generator ")
st.write("Enter a creative prompt to generate stunning AI art using open-source models!")

# Example prompts
example_prompts = [
    "A futuristic city skyline at sunset, cyberpunk style",
    "A cat wearing sunglasses, surfing on a pizza",
    "Ancient forest temple overgrown with vines and glowing crystals"
]

# Show example prompt buttons
st.markdown("**Try an example prompt:**")
cols = st.columns(len(example_prompts))
for i, prompt in enumerate(example_prompts):
    if cols[i].button(prompt):
        st.session_state["prompt_input"] = prompt

# Prompt input
prompt = st.text_input("Enter your prompt:", value=st.session_state.get("prompt_input", ""), max_chars=200)
generate_button = st.button("🚀 Generate Image")

# Image generation logic
def generate_image(prompt_text):
    encoded_prompt = urllib.parse.quote(prompt_text)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img, url
        else:
            return None, "Error: Failed to fetch image from Pollinations."
    except Exception as e:
        return None, f"Error: {str(e)}"

# Display generated image
if generate_button and prompt.strip():
    with st.spinner("Generating your image..."):
        img, result = generate_image(prompt.strip())
        if img:
            st.image(img, caption=f"Prompt: {prompt}", use_container_width=True)
            # Save to history
            st.session_state.history.insert(0, {"prompt": prompt, "image": img})
        else:
            st.error(result)
elif generate_button and not prompt.strip():
    st.warning("Please enter a prompt before generating an image.")

# Show history gallery
if st.session_state.history:
    st.markdown("---")
    st.subheader("Prompt History")
    num_cols = 3
    cols = st.columns(num_cols)
    for i, entry in enumerate(st.session_state.history[:9]):  # Limit to last 9
        with cols[i % num_cols]:
            st.image(entry["image"], caption=entry["prompt"], use_container_width=True)

# Footer spacing
st.markdown(" ")
