from search_engine.base import BaseSearchEngine, SearchResult


class HybridSearchEngine(BaseSearchEngine):
    """Hybrid search combining multiple search engines."""

    def __init__(self, keyword_engine: BaseSearchEngine, semantic_engine: BaseSearchEngine,
                 keyword_weight: float = 0.5, semantic_weight: float = 0.5):
        """Initialize hybrid search engine.

        Args:
            keyword_engine: A keyword/BM25-based search engine.
            semantic_engine: A semantic search engine.
            keyword_weight: Weight for keyword search results (0-1).
            semantic_weight: Weight for semantic search results (0-1).
        """
        super().__init__()
        self.keyword_engine = keyword_engine
        self.semantic_engine = semantic_engine
        self.keyword_weight = keyword_weight
        self.semantic_weight = semantic_weight

    def create_inverted_index(self, documents: dict[str, str]) -> None:
        """Build indices in both underlying engines.

        Args:
            documents: Dictionary mapping doc_id to document content.
        """
        pass

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using both engines and merge results.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects with merged scores (descending).
        """
        pass
