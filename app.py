import streamlit as st
import requests

API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="Myth Generator", layout="centered")

# ---------- STYLING ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;800&display=swap');

    html, body, .stApp {
        background-color: #272757 !important;
        color: #505081 !important;
        font-family: 'Raleway', sans-serif;
    }

    .main-container {
        padding: 2rem;
    }

    .title {
        font-size: 32px;
        font-weight: 800;
        text-align: center;
        color: #5c5c99;
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
        color: #272757;
        font-size: 16px;
    }

    .footer {
        text-align: center;
        font-size: 14px;
        color: #d3d3e3;
        margin-top: 40px;
    }

    .badge {
        text-align: center;
        margin-top: 30px;
    }

    .badge span {
        background-color: #8686ac;
        color: #272757;
        padding: 6px 16px;
        border-radius: 12px;
        font-size: 14px;
    }

    button[kind="primary"] {
        background-color: #8686ac !important;
        color: #0f0e47 !important;
        border-radius: 8px;
    }
    </style>
    <div class="main-container">
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">📚 Myth Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Craft rich, cultural folk tales with the help of powerful AI ✨</div>', unsafe_allow_html=True)

# ---------- INPUT FIELDS ----------
author = st.text_input("🖋️ Your name (optional)", placeholder="e.g., Arjun, Fatima")
country = st.text_input("🌍 Enter a country or region", placeholder="e.g., Egypt, India, Greece")
theme = st.text_input("🎭 Optional: Enter a theme", placeholder="e.g., desert, river, tiger")
generate = st.button("🔮 Generate Myth")

# ---------- GENERATE MYTH ----------
if generate and country:
    with st.spinner("Summoning ancient stories from the mists of time..."):
        prompt = f"""
        You are a skilled cultural storyteller and historian. Craft a vivid, authentic folk tale from the region of {country}.
        If possible, subtly weave in real cultural, geographic, or mythological elements from that place.

        Theme: {theme if theme else "a timeless traditional motif"}.

        The story should:
        - Feel like it's passed down orally through generations.
        - Include a meaningful title.
        - Feature named characters rooted in the region's traditions.
        - Describe a setting that evokes the local environment or time period.
        - Contain a conflict, a gentle arc, and a memorable resolution.
        - End with a short moral, wisdom, or proverb-like reflection.

        Style: Smooth, immersive, poetic in tone but easy to understand — like a tale heard under moonlight.
        Length: 350–500 words.
        """

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "HTTP-Referer": "https://your-deployment-url",
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

                story_text = story
                if author:
                    story_text += f"\n\n~ Written for you by {author}"

                st.download_button(
                    label="📥 Download as .txt",
                    data=story_text,
                    file_name=f"{country.lower().replace(' ', '_')}_myth.txt",
                    mime="text/plain"
                )
            else:
                st.error("No story returned. Try again.")
                st.json(data)

        except Exception as e:
            st.error(f"API Error: {e}")

elif generate:
    st.warning("Please enter a country or region.")

# ---------- BADGE ----------
st.markdown("""
    <div class="badge">
        <span>🌓 Inspired by cultural fantasy</span>
    </div>
""", unsafe_allow_html=True)

# ---------- FOOTER & CLOSE ----------
st.markdown('<div class="footer">🔧 Built by Manan · Powered by OpenRouter + Streamlit</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
