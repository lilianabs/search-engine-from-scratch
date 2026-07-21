from typing import Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from search_engine.base import BaseSearchEngine, SearchResult


class SemanticSearchEngine(BaseSearchEngine):
    """Semantic search using embeddings and cosine similarity."""

    def __init__(self, model_name: Optional[str] = None):
        """Initialize semantic search engine.

        Args:
            model_name: Name of the SentenceTransformer model to use.
                       Defaults to "all-MiniLM-L6-v2" if not provided.
        """
        super().__init__()
        if model_name is None:
            model_name = "all-MiniLM-L6-v2"
        self.model = SentenceTransformer(model_name)
        self.document_embeddings = None
        self.doc_id_list = []
        self.knn_index = None

    def create_inverted_index(self, documents: dict[str, str]) -> None:
        """Build an index of document embeddings using NearestNeighbors.

        Args:
            documents: Dictionary mapping doc_id to document content.
        """
        if not documents:
            self.document_embeddings = np.array([])
            self.doc_id_list = []
            return

        self.doc_id_list = list(documents.keys())
        doc_contents = [documents[doc_id] for doc_id in self.doc_id_list]

        self.document_embeddings = self.model.encode(doc_contents, show_progress_bar=True)

        self.knn_index = NearestNeighbors(n_neighbors=min(len(documents), 5), metric="cosine")
        self.knn_index.fit(self.document_embeddings)

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search using semantic similarity.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects sorted by similarity score (descending).
        """
        if self.knn_index is None or len(self.doc_id_list) == 0:
            return []

        query_embedding = self.model.encode([query])

        n_neighbors = min(top_k, len(self.doc_id_list))
        distances, indices = self.knn_index.kneighbors(query_embedding, n_neighbors=n_neighbors)

        results = []
        for distance, idx in zip(distances[0], indices[0]):
            doc_id = self.doc_id_list[idx]
            similarity_score = 1 - distance
            results.append(SearchResult(
                doc_id=doc_id,
                score=similarity_score,
                content=self.documents[doc_id]
            ))

        return results
