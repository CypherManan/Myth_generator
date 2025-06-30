import streamlit as st
import requests

API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Myth Generator", layout="centered")

# ---------- START CONTAINER with Scoped Styling ----------
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #505081 !important;
        color: #ffffff !important;
    }

    .main-container {
        padding: 2rem;
    }

    /* Main heading style */
    .title {
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        color: #f1f1f1;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #d3d3e3;
        margin-bottom: 30px;
    }

    .story-box {
        background-color: #8686AC;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        line-height: 1.6;
        overflow-y: auto;
        max-height: 500px;
        white-space: pre-wrap;
        color: #ffffff;
        font-size: 16px;
    }

    .footer {
        text-align: center;
        font-size: 14px;
        color: #cccccc;
        margin-top: 40px;
    }
   
    button[kind="primary"] {
        background-color: #6c63ff !important;
        color: white !important;
        border-radius: 8px;
    }
    </style>

    <div class="main-container">
""", unsafe_allow_html=True)

# ---------- CONTENT ----------
st.markdown('<div class="title">📚 Myth Generator using OpenRouter AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Craft rich, cultural folk tales with the help of powerful AI ✨</div>', unsafe_allow_html=True)

country = st.text_input("🌍 Enter a country or region", placeholder="e.g., Egypt, India, Greece")
theme = st.text_input("🎭 Optional: Enter a theme", placeholder="e.g., desert, river, tiger")
generate = st.button("🔮 Generate Myth")

if generate and country:
    with st.spinner("Summoning ancient stories..."):
        prompt = f"""
        Generate a culturally grounded folk tale from {country}.
        Theme: {theme if theme else 'a traditional cultural motif'}.
        Include a title, characters, setting, conflict, resolution, and moral.
        300–500 words, authentic tone.
        """

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "HTTP-Referer": "https://your-deployment-url",  # optional
                    "X-Title": "Myth Generator"
                },
                json={
                    "model": "mistralai/mixtral-8x7b-instruct",
                    "messages": [
                        {"role": "system", "content": "You are a cultural myth expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.9,
                    "max_tokens": 1000
                }
            )

            data = response.json()
            if "choices" in data:
                story = data["choices"][0]["message"]["content"]
                st.markdown("### 📖 Generated Myth")
                st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)
            else:
                st.error("No story returned. Try again.")
                st.json(data)

        except Exception as e:
            st.error(f"API Error: {e}")

elif generate:
    st.warning("Please enter a country or region.")

# ---------- FOOTER & CLOSE DIV ----------
st.markdown('<div class="footer">🔧 Built by Manan · Powered by OpenRouter + Streamlit</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
