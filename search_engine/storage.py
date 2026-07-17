"""Index persistence utilities."""

import pickle
from pathlib import Path
from search_engine.base import BaseSearchEngine


def save_index(engine: BaseSearchEngine, path: str) -> None:
    """Save search engine index to disk using pickle.

    Args:
        engine: The search engine instance to save.
        path: File path to save the index to.
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump({
            'documents': engine.documents,
            'inverted_index': engine.inverted_index
        }, f)


def load_index(engine: BaseSearchEngine, path: str) -> None:
    """Load a previously saved index into a search engine instance.

    Args:
        engine: The search engine instance to load into.
        path: File path to load the index from.
    """
    with open(path, 'rb') as f:
        data = pickle.load(f)
        engine.documents = data['documents']
        engine.inverted_index = data['inverted_index']
