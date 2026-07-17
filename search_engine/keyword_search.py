from search_engine.base import BaseSearchEngine, SearchResult
from search_engine.tokenizer import preprocess, tokenize


class KeywordSearchEngine(BaseSearchEngine):
    """Simple keyword-based search using term matching."""
    def create_inverted_index(self, documents: dict[str, str]) -> None:
        """Build an inverted index mapping terms to documents.

        Args:
            documents: Dictionary mapping doc_id to document content.
        """
        for doc_id, content in documents.items():
            preprocessed_content = preprocess(content)
            tokens = tokenize(preprocessed_content)
            for token in tokens:
                if token not in self.inverted_index:
                    self.inverted_index[token] = {}
                self.inverted_index[token][doc_id] = self.inverted_index[token].get(doc_id, 0) + 1

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using simple keyword matching.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects sorted by relevance score (descending).
        """
        preprocessed_query = preprocess(query)
        query_tokens = tokenize(preprocessed_query)

        doc_scores = {}  # doc_id -> score

        for token in query_tokens:
            if token in self.inverted_index:
                for doc_id, freq in self.inverted_index[token].items():
                    doc_scores[doc_id] = doc_scores.get(doc_id, 0) + freq

        # Sort by score descending
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Convert to SearchResult objects
        results = []
        for doc_id, score in sorted_docs:
            results.append(SearchResult(
                doc_id=doc_id,
                score=score,
                content=self.documents[doc_id]
            ))
        return results

