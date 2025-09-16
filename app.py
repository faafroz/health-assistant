import streamlit as st
import sqlite3
from translator import translate_text, LANG_CODES
import langid  # ✅ better language detection
from gtts import gTTS  # ✅ TTS
import os

# --- Streamlit UI ---
st.set_page_config(page_title="Local Language Health Info Assistant 🌍", page_icon="🌍")

st.title("Local Language Health Info Assistant 🌍")
st.caption(
    "Phase 1 languages: Spanish, Arabic, Vietnamese, Somali, Haitian Creole, Hindi, Bengali, Urdu, Chinese, Russian"
)

# --- Helper: detect language ---
def detect_language(text):
    try:
        lang, _ = langid.classify(text)
        return lang
    except:
        return "unknown"

# --- TTS helper ---
def generate_tts(text, lang_code="en"):
    try:
        tts = gTTS(text=text, lang=lang_code)
        file_path = "response.mp3"
        tts.save(file_path)
        return file_path
    except Exception as e:
        st.error(f"TTS error: {e}")
        return None

# --- UI: user input ---
user_question = st.text_input("Enter your health question:")

# Auto-detect language (if user typed something)
detected_lang = detect_language(user_question) if user_question else "en"

# Map langid codes to your dropdown labels
lang_map = {
    "en": "English",
    "es": "Spanish",
    "ar": "Arabic",
    "vi": "Vietnamese",
    "so": "Somali",
    "ht": "Haitian Creole",
    "hi": "Hindi",
    "bn": "Bengali",
    "ur": "Urdu",
    "zh": "Chinese",
    "ru": "Russian",
}

detected_lang_name = lang_map.get(detected_lang, "English")

# Input language dropdown (pre-filled with detected language, user can override)
input_lang = st.selectbox(
    "Input language:", list(LANG_CODES.keys()),
    index=list(LANG_CODES.keys()).index(detected_lang_name)
)
output_lang = st.selectbox("Response language:", list(LANG_CODES.keys()))

# --- Connect to SQLite DB ---
conn = sqlite3.connect("data/health_responses.db")
c = conn.cursor()

# --- Keyword/phrase matching with normalization ---
def normalize(text):
    text = text.lower().strip()
    if text.endswith("ing"):
        text = text[:-3]
    elif text.endswith("es"):
        text = text[:-2]
    elif text.endswith("s"):
        text = text[:-1]
    return text

def match_intents(user_input_en):
    matched_responses = []
    user_input_lower = normalize(user_input_en)

    c.execute("SELECT intent, keywords, answer, disclaimer FROM responses")
    for intent, keywords, answer, disclaimer in c.fetchall():
        if keywords:
            keyword_list = [normalize(k.strip()) for k in keywords.split(",")]
            for kw in keyword_list:
                if kw in user_input_lower:
                    matched_responses.append({
                        "intent": intent,
                        "answer": answer,
                        "disclaimer": disclaimer
                    })
                    break

    # ✅ Fallback if nothing matched
    if not matched_responses:
        matched_responses.append({
            "intent": "general",
            "answer": "Drink fluids, rest, and monitor your symptoms. If your condition worsens, seek medical attention.",
            "disclaimer": "This is general advice. Consult a healthcare professional for personal guidance."
        })
    return matched_responses

# --- Main app logic ---
if user_question:
    st.info(f"🌐 Detected input language: {detected_lang_name}")

    # Step 1: Translate input → English for intent matching
    user_input_en = translate_text(user_question, "en", src_code=LANG_CODES[input_lang])

    # Step 2: Match with responses
    matched_responses = match_intents(user_input_en)

    # Step 3: Show results
    for r in matched_responses:
        answer_out = translate_text(r["answer"], LANG_CODES[output_lang], src_code="en")
        disclaimer_out = translate_text(r["disclaimer"], LANG_CODES[output_lang], src_code="en")

        # ✅ Generate TTS for the translated answer
        audio_file = generate_tts(answer_out, lang_code=LANG_CODES[output_lang])

        # Advice card with TTS
        st.markdown(f"""
        <div style="border:1px solid #ddd; padding:20px; border-radius:10px; background:#f9f9f9;">
            <h3 style="color:black;">Advice for: {r['intent'].replace('_',' ').title()}</h3>
            <p style="color:black; font-size:1.1em;">{answer_out}</p>
            <p style="color:gray; font-size:0.9em;">{disclaimer_out}</p>
        </div>
        """, unsafe_allow_html=True)

        # 🎵 Play audio button
        if audio_file:
            st.audio(audio_file, format="audio/mp3")

# --- Close DB connection ---
conn.close()
