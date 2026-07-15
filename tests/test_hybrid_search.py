"""Tests for HybridSearchEngine."""

import pytest
from search_engine.keyword_search import KeywordSearchEngine
from search_engine.bm25_search import BM25SearchEngine
from search_engine.hybrid_search import HybridSearchEngine


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return {
        "doc1": "python programming language",
        "doc2": "java programming language",
        "doc3": "python is awesome",
    }


def test_hybrid_search_initialization(sample_documents):
    """Test HybridSearchEngine initialization with two engines."""
    pass


def test_hybrid_search_builds_both_indices(sample_documents):
    """Test that hybrid search builds indices in both underlying engines."""
    pass


def test_hybrid_search_combines_results(sample_documents):
    """Test that hybrid search combines results from both engines."""
    pass
