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

    def get_keywords(self, num_keywords: int = 5) -> tuple:
        """
        Extract keywords from the text provided in constructor.

        Uses the translated text to extract keywords.

        Args:
            num_keywords (int): Number of keywords to extract (default: 5).

        Returns:
            list: A list of tuple containing keywords extracted from the text.
        """
        keywords = self.model.extract_keywords(
            self.translated_text, 
            keyphrase_ngram_range=(1, 1), 
            stop_words='english', 
            top_n=num_keywords
        )

        return tuple(kw[0] for kw in keywords)
    
if __name__ == "__main__":
    sample_text = """
        Black holes are among the most fascinating and mysterious objects in the universe. 
        They are regions in space where gravity is so intense that nothing—not even light—can escape. 
        Black holes form when massive stars collapse under their own gravity after exhausting their nuclear fuel.

        There are several types of black holes. Stellar black holes form from collapsing stars and usually have a 
        mass up to 20 times that of the Sun. Supermassive black holes, found at the centers of galaxies, can have 
        masses millions or even billions of times greater than the Sun. Scientists believe that almost every galaxy, 
        including our Milky Way, contains a supermassive black hole at its center.

        Black holes can't be observed directly because no light escapes them. However, their presence is inferred 
        through their effects on nearby matter. For example, when a black hole pulls in nearby gas or stars, the 
        material heats up and emits X-rays, which telescopes can detect.

        In 2019, the Event Horizon Telescope captured the first-ever image of a black hole's shadow, marking a historic 
        milestone in astrophysics. Despite decades of research, black holes continue to challenge our understanding 
        of physics, space, and time, holding secrets yet to be revealed.
        """    
    
    extractor = KeywordsExtractor(sample_text)
    keywords = extractor.get_keywords()
    print(keywords)
    print("Original text:", extractor.original_text)
    print("Translated text:", extractor.translated_text)
    print("Extracted keywords:", keywords)