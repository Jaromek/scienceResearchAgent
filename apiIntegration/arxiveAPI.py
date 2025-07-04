import arxiv

class ArxivAPI:
    def __init__(self, keyword_list: list[str], max_results: int = 10):
        self.keyword_list = keyword_list
        self.max_results = max_results

    def search(self) -> list[str]:
        """
        Search for papers on arXiv based on the keyword_list.

        Args:
            keyword_list (str): The search keyword_list.
            max_results (int): Maximum number of results to return.

        Returns:
            list: A list of dictionaries containing paper information.
        """
        # Połącz słowa kluczowe w jeden query string
        query_string = " OR ".join(self.keyword_list)
        
        search = arxiv.Search(
            query=query_string,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for result in search.results():
            results.append({
                'title': result.title,
                'summary': result.summary,
                'authors': [author.name for author in result.authors],
                'published': result.published,
                'arxiv_id': result.entry_id
            })
        
        return results