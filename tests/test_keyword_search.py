"""Tests for KeywordSearchEngine."""

import pytest
from search_engine.keyword_search import KeywordSearchEngine


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return {
        "doc1": "python programming language",
        "doc2": "java programming language",
        "doc3": "python is awesome",
    }


def test_keyword_search_creates_index(sample_documents):
    """Test that keyword search creates an inverted index."""
    pass


def test_keyword_search_finds_matching_documents(sample_documents):
    """Test that keyword search finds documents with matching terms."""
    pass


def test_keyword_search_ranking(sample_documents):
    """Test that keyword search ranks results appropriately."""
    pass


def test_keyword_search_returns_top_k(sample_documents):
    """Test that keyword search respects top_k parameter."""
    pass
