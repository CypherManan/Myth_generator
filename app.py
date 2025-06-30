import streamlit as st
import requests

# Load API key from Streamlit secrets
API_KEY = st.secrets["OPENROUTER_API_KEY"]

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Myth Generator", layout="centered")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #f0f2f6 !important;
        font-family: 'Segoe UI', sans-serif;
        color: #2c3e50;
    }
    .main-title {
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #6c757d;
        margin-bottom: 30px;
    }
    .story-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        line-height: 1.6;
        overflow-y: auto;
        max-height: 500px;
        white-space: pre-wrap;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #6c757d;
        margin-top: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">📚 Myth Generator using OpenRouter AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Craft rich folk tales from cultures around the world ✨</div>', unsafe_allow_html=True)

# ---------- INPUT FIELDS ----------
country = st.text_input("🌍 Enter a country or region", placeholder="e.g., India, Japan, Greece")
theme = st.text_input("🎭 Optional: Enter a theme", placeholder="e.g., forest, wisdom, dragons")
generate = st.button("🔮 Generate Myth")

# ---------- STORY GENERATION ----------
if generate and country:
    with st.spinner("Summoning ancient legends..."):
        prompt = f"""
        Generate a culturally grounded folk tale from {country}.
        Theme: {theme if theme else "a traditional motif"}.
        Include:
        - A title
        - Named characters
        - Cultural setting
        - A conflict and resolution
        - A moral at the end

        Length: 300-500 words.
        """

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "HTTP-Referer": "https://yourusername-myth-generator.streamlit.app",  # Replace with your deployed URL if you want
                    "X-Title": "MiniMyth Generator"
                },
                json={
                    "model": "mistralai/mixtral-8x7b-instruct",
                    "messages": [
                        {"role": "system", "content": "You are a cultural storyteller."},
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
                st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)
            else:
                st.error("⚠️ No story generated. Try again later.")
                st.json(data)

        except Exception as e:
            st.error(f"API Error: {e}")

elif generate:
    st.warning("⚠️ Please enter a country or region first.")

# ---------- FOOTER ----------
st.markdown('<div class="footer">🔧 Built by Manan · Powered by OpenRouter + Streamlit</div>', unsafe_allow_html=True)
