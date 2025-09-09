import streamlit as st
import yaml
from translator import translate_text, LANG_CODES

# Load responses
with open("responses/health_responses.yaml", "r") as file:
    data = yaml.safe_load(file)
    responses = data["responses"]

st.title("Local Language Health Info Assistant 🌍")
st.caption("Phase 1: Spanish, Arabic, Vietnamese, Somali, Haitian Creole, Hindi, Bengali, Urdu, Chinese, Russian")

# User input
user_question = st.text_input("Enter your health question:")

# Language selection
language = st.selectbox("Select language:", list(LANG_CODES.keys()))

# Display response
if user_question:
    matched_responses = []
    for r in responses:
        if r["intent"].lower() in user_question.lower():
            matched_responses.append(r)

    if matched_responses:
        for matched in matched_responses:
            # Translate if needed
            if language != "English":
                answer = translate_text(matched["answer"], dest_language=language)
                disclaimer = translate_text(matched["disclaimer"], dest_language=language)
            else:
                answer = matched["answer"]
                disclaimer = matched["disclaimer"]

            st.subheader(f"Advice for: {matched['intent'].replace('_',' ').title()}")
            st.write(answer)
            st.caption(disclaimer)
    else:
        st.write("Sorry, I don't have advice for that question yet.")
