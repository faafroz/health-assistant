import streamlit as st
import sqlite3
import re
from translator import translate_text, LANG_CODES

# -------------------------------
# UI
# -------------------------------
st.title("Local Language Health Info Assistant 🌍")
st.caption(
    "Phase 1 languages: Spanish, Arabic, Vietnamese, Somali, Haitian Creole, Hindi, Bengali, Urdu, Chinese, Russian"
)

user_question = st.text_input("Enter your health question:")
language = st.selectbox("Select language:", list(LANG_CODES.keys()))

# -------------------------------
# Database connection
# -------------------------------
conn = sqlite3.connect("data/health_responses.db")
c = conn.cursor()

# -------------------------------
# Keyword matching function
# -------------------------------
def match_intents(user_input):
    """
    Matches user input to intents based on keywords in the database.
    Uses regex word boundaries to avoid partial matches.
    """
    matched_responses = []
    user_input_lower = user_input.lower()
    c.execute("SELECT intent, keywords, answer, disclaimer FROM responses")
    for intent, keywords, answer, disclaimer in c.fetchall():
        if keywords:
            keyword_list = [k.strip().lower() for k in keywords.split(",")]
            for k in keyword_list:
                # Regex to match whole word or exact phrase
                pattern = r'\b' + re.escape(k) + r'\b'
                if re.search(pattern, user_input_lower):
                    matched_responses.append({
                        "intent": intent,
                        "answer": answer,
                        "disclaimer": disclaimer
                    })
                    break  # stop checking other keywords for this intent
    return matched_responses

# -------------------------------
# Main app logic
# -------------------------------
if user_question:
    matched_responses = match_intents(user_question)
    if matched_responses:
        for r in matched_responses:
            # Translate answer and disclaimer
            answer_translated = translate_text(r["answer"], language)
            disclaimer_translated = translate_text(r["disclaimer"], language)

            st.subheader(f"Advice for: {r['intent'].replace('_',' ').title()}")
            st.write(answer_translated)
            st.caption(disclaimer_translated)
    else:
        st.write("Sorry, I don't have advice for that question yet.")

# -------------------------------
# Close DB connection
# -------------------------------
conn.close()
