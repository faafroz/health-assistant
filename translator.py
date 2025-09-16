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
    "Chinese": "zh-cn",   # Google Translate uses zh-cn
    "Russian": "ru"
}

def translate_text(text, dest_code, src_code=None):
    """
    Translate text into the target language code.
    Example: 'ur' for Urdu, 'es' for Spanish.
    If src_code is given, force translation from that language.
    """
    try:
        if dest_code == "en" and (src_code is None or src_code == "en"):
            return text
        translated = translator.translate(text, src=src_code, dest=dest_code)
        return translated.text
    except Exception:
        return text  # fallback if error
