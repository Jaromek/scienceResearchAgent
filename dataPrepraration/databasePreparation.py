from extraction.keywordsExtraction import KeywordsExtractor
from apiIntegration.arxiveAPI import ArxivAPI
from embedding.embeddingArticle import EmbeddingArticle
from pdfToText.pdfToText import PDFToText


class DatabasePreparation:
    def __init__(self, user_query: str = "", max_results: int = 10, download_directory: str = './archive'):
        self.user_query = user_query
        self.max_results = max_results
        self.download_directory = download_directory

    def prepare_database(self):
        # Step 1: Extract keywords from the provided text
        extractor = KeywordsExtractor(self.user_query)
        keyword_list = extractor.get_keywords()

        # Step 2: Search and download papers from arXiv
        arxiv_api = ArxivAPI(keyword_list=keyword_list, max_results=self.max_results, download_directory=self.download_directory)
        papers = arxiv_api.search()

        # Step 3: Convert downloaded PDFs to text
        pdf_to_text = PDFToText(pdf_path=self.download_directory)
        texts = pdf_to_text.convert_to_text()

        # Step 4: Embed articles and add them to the vectorstore
        embedding_article = EmbeddingArticle(articles=texts)
        embedding_article.embed_articles()