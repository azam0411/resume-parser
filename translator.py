from googletrans import Translator

translator = Translator()

def translate_content(content, lang):
    translated = translator.translate(content, dest=lang)
    return translated.text
