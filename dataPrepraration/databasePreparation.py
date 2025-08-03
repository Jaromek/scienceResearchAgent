from dataPrepraration.extraction.keywordsExtraction import KeywordsExtractor
from dataPrepraration.apiIntegration.arxiveAPI import ArxivAPI
from dataPrepraration.embedding.embeddingArticle import EmbeddingArticle
from dataPrepraration.pdfToText.pdfToText import PDFToText


class DatabasePreparation:
    def __init__(self, user_query: str = "", max_results: int = 10, download_directory: str = 'archive'):
        self.user_query = user_query
        self.max_results = max_results
        self.download_directory = download_directory

    def prepare_database(self):
        # Step 1: Extract keywords from the provided text
        extractor = KeywordsExtractor(self.user_query)
        keyword_list = extractor.get_keywords()
        print(f"Extracted keywords: {keyword_list}")

        # Step 2: Search and download papers from arXiv
        arxiv_api = ArxivAPI(keyword_list=keyword_list, max_results=self.max_results, download_directory=self.download_directory)
        papers = arxiv_api.search()
        print(f"Successfully downloaded {len(papers)} papers")

        if not papers:
            print("No papers were downloaded. Cannot proceed with text extraction.")
            return

        # Step 3: Convert downloaded PDFs to text
        pdf_to_text = PDFToText(pdf_path=self.download_directory)
        texts = pdf_to_text.convert_to_text()
        
        if not texts:
            print("No texts were extracted from PDFs.")
            return

        # Step 4: Get PDF filenames for metadata
        pdf_paths = pdf_to_text._path_to_pdfs()
        
        # Create articles list with filenames as metadata
        articles_with_names = []
        for i, text in enumerate(texts):
            if i < len(pdf_paths):
                filename = pdf_paths[i].split('/')[-1].replace('.pdf', '')  # Get filename without path and extension
                articles_with_names.append({'text': text, 'filename': filename})
            else:
                articles_with_names.append({'text': text, 'filename': f'Document_{i+1}'})
        
        # Step 5: Embed articles and add them to the vectorstore
        texts_only = [article['text'] for article in articles_with_names]
        embedding_article = EmbeddingArticle(articles=texts_only)
        
        # Override the embed_articles method to use proper filenames
        for i, article_data in enumerate(articles_with_names):
            chunks = embedding_article._split_text(article_data['text'])
            if chunks:
                embedding_article._add_documents(chunks, article_data['filename'])
                print(f"Embedded article: {article_data['filename']} ({len(chunks)} chunks)")
        
        print("Database preparation completed successfully!")

if __name__ == "__main__":
    query = 'what machine learning methods are used in black hole research and why?'

    db_preparation = DatabasePreparation(user_query=query, max_results=10, download_directory='archive')
    try:
        db_preparation.prepare_database()
        print("Database preparation completed successfully.")
    except Exception as e:
        print(f"An error occurred during database preparation: {e}")
        print(f"Error: {e}")
    
