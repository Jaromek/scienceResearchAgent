from sentence_transformers import SentenceTransformer

class EmbeddingArticle:
    def __init__(self, model_name='all-MiniLM-L6-v2', text=None):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.text = text

    def embed(self, text=None):
        text_to_embed = text if text is not None else self.text
        if not isinstance(text_to_embed, str):
            raise ValueError("Input text must be a string.")
        embedding = self.model.encode(text_to_embed, convert_to_tensor=True)
        return embedding

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

    sample_text = "This is a sample text for embedding."

    from textPreprocessing import textPreprocessing

    preprocessing_instance = textPreprocessing.TextPreprocessor(text=sample_text)
    processed_text = preprocessing_instance.preprocess()    
    print(f"Processed Text: {processed_text}")
    
    embedding_instance = EmbeddingArticle(text=processed_text)
    embedding = embedding_instance.embed()
    print(embedding.shape)
