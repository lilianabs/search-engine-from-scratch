from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a single search result."""
    doc_id: str
    score: float
    content: str = ""


class BaseSearchEngine(ABC):
    """Abstract base class for all search engine implementations."""

    def __init__(self):
        self.documents: dict[str, str] = {}
        self.inverted_index: dict = {}

    def add_documents(self, documents: dict[str, str]) -> None:
        """Add documents to the engine and build the inverted index."""
        self.documents = documents
        self.create_inverted_index(documents)

    @abstractmethod
    def create_inverted_index(self, documents: dict[str, str]) -> None:
        """Build the inverted index from documents.

        Args:
            documents: Dictionary mapping doc_id to document content.
        """
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Search for documents matching the query.

        Args:
            query: The search query string.
            top_k: Maximum number of results to return.

        Returns:
            List of SearchResult objects sorted by relevance score (descending).
        """
        pass

    def save(self, path: str) -> None:
        """Save the index to disk.

        Args:
            path: File path to save the index to.
        """
        from search_engine import storage
        storage.save_index(self, path)

    def load(self, path: str) -> None:
        """Load a previously saved index from disk.

        Args:
            path: File path to load the index from.
        """
        from search_engine import storage
        storage.load_index(self, path)
