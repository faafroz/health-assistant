import streamlit as st
import sqlite3
import spacy
from translator import translate_text, LANG_CODES

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Connect to SQLite DB
conn = sqlite3.connect("data/health_responses.db")
c = conn.cursor()

st.title("Local Language Health Info Assistant 🌍")
st.caption("Phase 1 languages: Spanish, Arabic, Vietnamese, Somali, Haitian Creole, Hindi, Bengali, Urdu, Chinese, Russian")

# User input
user_question = st.text_input("Enter your health question:")

# Language selection
language = st.selectbox("Select language:", list(LANG_CODES.keys()))

def match_intents(user_input):
    """
    Smarter keyword matching using spaCy
    """
    matched_responses = []
    doc = nlp(user_input.lower())
    c.execute("SELECT intent, answer, disclaimer FROM responses")
    for intent, answer, disclaimer in c.fetchall():
        intent_tokens = nlp(intent.replace("_", " ").lower())
        if any(token.text in [t.text for t in doc] for token in intent_tokens):
            matched_responses.append({"intent": intent, "answer": answer, "disclaimer": disclaimer})
    return matched_responses

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

# Close DB connection
conn.close()
