from googletrans import Translator

# Initialize Google Translate
translator = Translator()

# Phase 1 language codes
LANG_CODES = {
    "English": "en",
    "Spanish": "es",
    "Arabic": "ar",
    "Vietnamese": "vi",
    "Somali": "so",
    "Haitian Creole": "ht",
    "Hindi": "hi",
    "Bengali": "bn",
    "Urdu": "ur",
    "Chinese": "zh-cn",
    "Russian": "ru"
}

def translate_text(text, dest_language):
    """
    Translate text to the target Phase 1 language using Google Translate.
    dest_language: full language name, e.g., 'Spanish', 'Hindi'
    """
    try:
        lang_code = LANG_CODES.get(dest_language, "en")
        translated = translator.translate(text, dest=lang_code)
        return translated.text
    except Exception as e:
        return f"Translation error: {e}"
