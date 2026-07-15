from search_engine.base import BaseSearchEngine, SearchResult


class SemanticSearchEngine(BaseSearchEngine):
    """Semantic search using embeddings (stub for now)."""

    def __init__(self, embedder=None):
        """Initialize semantic search engine.

        Args:
            embedder: Optional embedding function. Will be added later
                     when a concrete embedding model is integrated.
        """
        super().__init__()
        self.embedder = embedder

    def create_inverted_index(self, documents: dict[str, str]) -> None:
        """Build an index of document embeddings.

        Note: This is currently a stub. Will generate embeddings for documents
              once an embedder is provided.

        Args:
            documents: Dictionary mapping doc_id to document content.
        """
        pass

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using semantic similarity.

        Note: This is currently a stub. Will compute query embedding and
              find nearest document embeddings once embedder is available.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects sorted by similarity score (descending).
        """
        pass
