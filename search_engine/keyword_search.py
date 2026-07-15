from search_engine.base import BaseSearchEngine, SearchResult


class KeywordSearchEngine(BaseSearchEngine):
    """Simple keyword-based search using term matching."""

    def create_inverted_index(self, documents: dict[str, str]) -> None:
        """Build an inverted index mapping terms to documents.

        Args:
            documents: Dictionary mapping doc_id to document content.
        """
        pass

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using simple keyword matching.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects sorted by relevance score (descending).
        """
        pass
