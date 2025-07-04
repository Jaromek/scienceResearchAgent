from sentence_transformers import SentenceTransformer

class EmbeddingArticle:
    def __init__(self, model_name='all-MiniLM-L6-v2', text=None):
        """
        Initializes the EmbeddingArticle with a specified SentenceTransformer model.

        :param model_name: The name of the SentenceTransformer model to use.
        :param text: The text to embed (optional).
        """
        
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.text = text

        
    def embed(self, text=None):
        """
        Embeds the given text using the SentenceTransformer model.

        :param text: The text to embed. If None, uses the text from constructor.
        :return: The embedding of the text as a numpy array.
        """
        # Use provided text or fall back to instance text
        text_to_embed = text if text is not None else self.text
        
        if not isinstance(text_to_embed, str):
            raise ValueError("Input text must be a string.")
        
        embedding = self.model.encode(text_to_embed, convert_to_tensor=True)
        return embedding
