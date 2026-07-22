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
        self.keyword_engine.create_inverted_index(documents)
        self.semantic_engine.create_inverted_index(documents)

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using both engines and merge results.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects with merged scores (descending).
        """
        keyword_results = self.keyword_engine.search(query, top_k=top_k)
        semantic_results = self.semantic_engine.search(query, top_k=top_k)

        combined_scores = {}

        for result in keyword_results:
            score = result.score * self.keyword_weight
            if result.doc_id not in combined_scores:
                combined_scores[result.doc_id] = {"score": 0.0, "content": result.content}
            combined_scores[result.doc_id]["score"] += score

        for result in semantic_results:
            score = result.score * self.semantic_weight
            if result.doc_id not in combined_scores:
                combined_scores[result.doc_id] = {"score": 0.0, "content": result.content}
            combined_scores[result.doc_id]["score"] += score

        sorted_results = sorted(combined_scores.items(), key=lambda x: x[1]["score"], reverse=True)[:top_k]

        results = []
        for doc_id, data in sorted_results:
            results.append(SearchResult(
                doc_id=doc_id,
                score=data["score"],
                content=data["content"]
            ))

        return results
