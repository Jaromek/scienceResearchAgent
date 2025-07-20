import arxiv
import os

class ArxivAPI:
    def __init__(self, keyword_list: tuple[str, ...], max_results: int = 10, download_directory: str = './archive'):
        self.keyword_list = keyword_list
        self.max_results = max_results
        self.download_directory = download_directory

    def _create_download_directory(self):
        """
        Create the download directory if it does not exist.
        """
        if not os.path.exists(self.download_directory):
            os.makedirs(self.download_directory)

    def search(self) -> list[str]:
        """
        Search for papers on arXiv based on the keyword_list.

        Args:
            keyword_list (str): The search keyword_list.
            max_results (int): Maximum number of results to return.

        Returns:
            list: A list of dictionaries containing paper information.
        """
        # Create download directory first
        self._create_download_directory()
        
        # Połącz słowa kluczowe w jeden query string
        query_string = " OR ".join(self.keyword_list)
        
        search = arxiv.Search(
            query=query_string,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for result in search.results():
            try:
                # Download PDF first, then add to results only if successful
                result.download_pdf(dirpath=self.download_directory, filename=f"{result.entry_id.split('/')[-1]}.pdf")
                
                results.append({
                    'title': result.title,
                    'summary': result.summary,
                    'authors': [author.name for author in result.authors],
                    'published': result.published,
                    'arxiv_id': result.entry_id
                })
                
            except Exception as e:
                print(f"Failed to download {result.entry_id}: {e}")
                continue
        
        return results
    
if __name__ == "__main__":
    # Example usage
    keywords = ("black holes", "space exploration", "artificial intelligence")
    arxiv_api = ArxivAPI(keyword_list=keywords, max_results=10, download_directory='./archive')
    papers = arxiv_api.search()