import math
from search_engine.base import BaseSearchEngine, SearchResult
from search_engine.tokenizer import preprocess, tokenize


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
        self.doc_lengths = {}
        total_length = 0

        for doc_id, content in documents.items():
            preprocessed_content = preprocess(content)
            tokens = tokenize(preprocessed_content)
            doc_length = len(tokens)
            self.doc_lengths[doc_id] = doc_length
            total_length += doc_length

            for token in tokens:
                if token not in self.inverted_index:
                    self.inverted_index[token] = {}
                self.inverted_index[token][doc_id] = self.inverted_index[token].get(doc_id, 0) + 1

        self.avg_doc_length = total_length / len(documents) if documents else 0.0

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using BM25 ranking.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects sorted by BM25 score (descending).
        """
        preprocessed_query = preprocess(query)
        query_tokens = tokenize(preprocessed_query)

        doc_scores = {}

        for token in query_tokens:
            if token in self.inverted_index:
                idf = self._calculate_idf(token)
                for doc_id, freq in self.inverted_index[token].items():
                    bm25_score = self._calculate_bm25_score(
                        freq, idf, self.doc_lengths[doc_id]
                    )
                    doc_scores[doc_id] = doc_scores.get(doc_id, 0) + bm25_score

        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for doc_id, score in sorted_docs:
            results.append(SearchResult(
                doc_id=doc_id,
                score=score,
                content=self.documents[doc_id]
            ))
        return results

    def _calculate_idf(self, token: str) -> float:
        """Calculate inverse document frequency for a token.

        Args:
            token: The token to calculate IDF for.

        Returns:
            IDF score for the token.
        """
        num_docs = len(self.documents)
        docs_with_token = len(self.inverted_index.get(token, {}))
        return math.log((num_docs - docs_with_token + 0.5) / (docs_with_token + 0.5) + 1.0)

    def _calculate_bm25_score(self, freq: int, idf: float, doc_length: int) -> float:
        """Calculate BM25 score for a term in a document.

        Args:
            freq: Term frequency in the document.
            idf: Inverse document frequency.
            doc_length: Length of the document.

        Returns:
            BM25 score.
        """
        numerator = freq * (self.k1 + 1)
        denominator = freq + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_length))
        return idf * (numerator / denominator)
