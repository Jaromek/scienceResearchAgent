import re
import contractions
from num2words import num2words
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    def __init__(self, text=""):
        self.text = text

    def set_text(self, text):
        """Set the text to be preprocessed."""
        self.text = text

    def get_text(self):
        """Get the current text."""
        return self.text

    def remove_special_characters(self):
        """Remove special characters from the text."""
        self.text = re.sub(r'[^a-zA-Z0-9\s]', '', self.text)

    def remove_html_tags(self):
        """Remove HTML tags from the text."""
        self.text = re.sub(r'<.*?>', '', self.text)

    def normalize_case(self):
        """Convert text to lowercase."""
        self.text = self.text.lower()

    def expand_contractions(self):
        """Expand contractions in the text."""
        self.text = contractions.fix(self.text)

    def convert_numbers(self):
        """Convert numbers to words."""
        self.text = re.sub(r'\b\d+\b', lambda x: num2words(int(x.group())), self.text)
    
    def lemmatize(self):
        """Lemmatize the words in the text."""
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        lemmatizer = WordNetLemmatizer()
        tokens = self.text.split()
        self.text = ' '.join([lemmatizer.lemmatize(word) for word in tokens])

    def normalize_whitespace(self):
        """Normalize whitespace characters (multiple spaces → single space)."""
        self.text = re.sub(r'\s+', ' ', self.text).strip()

    def remove_stopwords(self, language='english'):
        """Remove stopwords from the text."""
        stop_words = set(stopwords.words(language))
        tokens = self.text.split()
        self.text = ' '.join([word for word in tokens if word not in stop_words])


    def preprocess(self):
        """Run all preprocessing steps."""
        self.remove_html_tags()
        self.remove_special_characters()
        self.normalize_case()
        self.expand_contractions()
        self.convert_numbers()
        self.normalize_whitespace()
        self.remove_stopwords()
        self.lemmatize()
        
        return self.text
    
if __name__ == "__main__":
    sample_text = "<p>This is a sample text with some numbers: 1, 2, and 3. It's a test!</p>"
    preprocessor = TextPreprocessor(sample_text)
    processed_text = preprocessor.preprocess()
    print(processed_text)
