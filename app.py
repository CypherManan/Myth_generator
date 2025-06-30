import streamlit as st
import requests

# Load API key securely from Streamlit Secrets
API_KEY = st.secrets["OPENROUTER_API_KEY"]

# ---------- STYLING ----------
st.set_page_config(page_title="🌍 Myth Generator", layout="centered")
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: #f5f6fa;
            font-family: 'Segoe UI', sans-serif;
        }
        .big-font {
            font-size: 24px !important;
            font-weight: bold;
            color: #2f3542;
        }
        .story-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- APP TITLE ----------
st.markdown('<p class="big-font">🧙‍♂️ Myth Generator by Culture & Theme</p>', unsafe_allow_html=True)
st.caption("Generate culturally inspired folk tales using powerful language models.")

# ---------- INPUT ----------
country = st.text_input("🌐 Enter a country or region", placeholder="e.g., India, Greece, Japan")
theme = st.text_input("🎭 Optional: Enter a theme", placeholder="e.g., fire, wisdom, animals")
generate = st.button("✨ Generate Myth")

# ---------- API Call ----------
if generate and country:
    with st.spinner("Crafting a myth from ancient legends..."):
        prompt = f"""
        You are a folklore expert. Generate a culturally authentic folk tale from {country}, involving the theme '{theme if theme else 'a traditional motif'}'.
        Include:
        - A title
        - Named characters
        - A conflict and resolution
        - A meaningful moral
        Keep it 300-500 words.
        """

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "HTTP-Referer": "http://localhost:8501",
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
                st.markdown("### 📖 Your Generated Folk Tale")
                st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)
            else:
                st.error("❌ Failed to generate. Try changing the model or retry later.")
                st.json(data)

        except Exception as e:
            st.error(f"API Error: {e}")

elif generate:
    st.warning("Please enter at least a country or region.")

# ---------- Footer ----------
st.markdown("---")
st.caption("🛠️ Built by Manan • Powered by OpenRouter & Streamlit")
