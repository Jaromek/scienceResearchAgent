from keybert import KeyBERT
from deep_translator import GoogleTranslator

class KeywordsExtractor:
    def __init__(self, text: str):
        self.model = KeyBERT()
        self.translator = GoogleTranslator(source='auto', target='en')
        self.original_text = text
        self.translated_text = self._translate_text(text)

    def _translate_text(self, text: str) -> str:
        """
        Translate the given text to English.

        Takes the original text and translates it using Google Translator.

        Args:
            text (str): The original text to translate.

        Returns:
            text (str): The translated text.
            If the text is already in English, it will return the original text.
        """
        return self.translator.translate(text)

    def get_keywords(self, num_keywords: int = 5) -> list:
        """
        Extract keywords from the text provided in constructor.

        Uses the translated text to extract keywords.

        Args:
            num_keywords (int): Number of keywords to extract (default: 5).

        Returns:
            list: A list of tuples containing (keyword, score) extracted from the text.
        """
        return self.model.extract_keywords(
            self.translated_text, 
            keyphrase_ngram_range=(1, 1), 
            stop_words='english', 
            top_n=num_keywords
        )