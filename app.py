import streamlit as st
import sqlite3
from translator import translate_text, LANG_CODES

# --- Streamlit UI ---
st.title("Local Language Health Info Assistant 🌍")
st.caption(
    "Phase 1 languages: Spanish, Arabic, Vietnamese, Somali, Haitian Creole, Hindi, Bengali, Urdu, Chinese, Russian"
)

user_question = st.text_input("Enter your health question:")
language = st.selectbox("Select language:", list(LANG_CODES.keys()))

# --- Connect to SQLite DB ---
conn = sqlite3.connect("data/health_responses.db")
c = conn.cursor()

# --- Keyword/phrase matching ---
def match_intents(user_input):
    """
    Returns a list of matched responses based on user input.
    Uses word-level and phrase-level matching.
    """
    matched_responses = []
    user_input_lower = user_input.lower().strip()
    
    c.execute("SELECT intent, keywords, answer, disclaimer FROM responses")
    for intent, keywords, answer, disclaimer in c.fetchall():
        if keywords:
            keyword_list = [k.strip().lower() for k in keywords.split(",")]
            for kw in keyword_list:
                # Exact match or phrase contained in user input
                if kw in user_input_lower or all(word in user_input_lower for word in kw.split()):
                    matched_responses.append({
                        "intent": intent,
                        "answer": answer,
                        "disclaimer": disclaimer
                    })
                    break
    return matched_responses

# --- Main app logic ---
if user_question:
    matched_responses = match_intents(user_question)
    if matched_responses:
        for r in matched_responses:
            answer = translate_text(r["answer"], language)
            disclaimer = translate_text(r["disclaimer"], language)
            st.subheader(f"Advice for: {r['intent'].replace('_',' ').title()}")
            st.write(answer)
            st.caption(disclaimer)
    else:
        st.write("Sorry, I don't have advice for that question yet.")

conn.close()
