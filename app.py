import streamlit as st
import os
import requests

# Load OpenRouter API key from environment or paste here directly
API_KEY = st.secrets["OPENROUTER_API_KEY"]# Replace with your key if not using .env

# Streamlit page setup
st.set_page_config(page_title="OpenRouter Myth Generator", layout="centered")
st.title("🧚‍♂️ Myth Generator using OpenRouter API")

# User input
country = st.text_input("🌍 Enter a country or region (e.g., India, Japan):")
theme = st.text_input("🎭 Optional: Enter a theme (e.g., wisdom, fire, forest):")
generate = st.button("✨ Generate Myth")

# When button is clicked
if generate and country:
    with st.spinner("Crafting your myth..."):

        prompt = f"""
You are a folk tale expert. Generate a rich, traditional myth or folk tale from {country}.
Include characters, a setting, a cultural theme like {theme if theme else "a traditional motif"}, and a moral lesson.
The story should be 300–500 words long and feel authentic to the region.
        """

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "HTTP-Referer": "http://localhost:8501",  # optional but polite
                    "X-Title": "MiniMyth Streamlit App"
                },
                json={
                    "model": "mistralai/mistral-small-3.2-24b-instruct:free",  # You can try other models like 'openai/gpt-3.5-turbo' or 'meta-llama/llama-3-70b-instruct'
                    "messages": [
                        {"role": "system", "content": "You are a cultural expert and mythological storyteller."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.9,
                    "max_tokens": 1000
                }
            )

            data = response.json()

            if "choices" in data:
                story = data["choices"][0]["message"]["content"]
                st.markdown("### 📖 Generated Folk Tale")
                st.write(story)
            else:
                st.error(" No story returned. Check your API key or model availability.")
                st.json(data)

        except Exception as e:
            st.error(f" Error: {e}")

elif generate:
    st.warning("⚠️ Please enter a country or region.")
