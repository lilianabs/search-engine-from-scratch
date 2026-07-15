from search_engine.base import BaseSearchEngine, SearchResult


class BM25SearchEngine(BaseSearchEngine):
    """BM25 probabilistic ranking function for search."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        """Initialize BM25 search engine.

        Args:
            k1: Controls non-linear term frequency normalization (saturation point).
            b: Controls how much effect document length has on relevance.
        """
        super().__init__()
        self.k1 = k1
        self.b = b
        self.avg_doc_length: float = 0.0
        self.doc_lengths: dict[str, int] = {}

    def create_inverted_index(self, documents: dict[str, str]) -> None:
        """Build an inverted index with document statistics for BM25.

        Args:
            documents: Dictionary mapping doc_id to document content.
        """
        pass

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using BM25 ranking.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects sorted by BM25 score (descending).
        """
        pass
