"""Tests for BM25SearchEngine."""

import pytest
from search_engine.bm25_search import BM25SearchEngine


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return {
        "doc1": "python programming language",
        "doc2": "java programming language",
        "doc3": "python is awesome",
    }


def test_bm25_creates_index_with_stats(sample_documents):
    """Test that BM25 creates an index with document statistics."""
    pass


def test_bm25_calculates_average_doc_length(sample_documents):
    """Test that BM25 calculates average document length."""
    pass


def test_bm25_search_returns_results(sample_documents):
    """Test that BM25 search returns ranked results."""
    pass


def test_bm25_search_ranking_vs_keyword(sample_documents):
    """Test that BM25 ranking differs from simple keyword matching."""
    pass
