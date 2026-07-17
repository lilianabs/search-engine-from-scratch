import os
import pandas as pd
import yaml
from search_engine.keyword_search import KeywordSearchEngine


def read_documents(file_path: str) -> dict[str, str]:
    """Read documents from a csv file

    Args:
        file_path: Path to the file containing documents.

    Returns:
        Dictionary mapping document ID to document content (title + description).
    """
    documents = pd.read_csv(file_path)
    doc_dict = {}
    for _, row in documents.iterrows():
        doc_id = str(row["index"])
        # Combine title and description as the document content
        content = f"{row['title']} {row['description']}"
        doc_dict[doc_id] = content
    return doc_dict


def get_config_path() -> str:
    """Get the path to the config.yaml file located in the project root directory."""
    # Get the project root directory (parent of scripts directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, "conf.yaml")


def load_config(config_path: str) -> dict:
    """Load configuration from config.yaml file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    # Get the project root directory (parent of scripts directory)
    config_path = get_config_path()
    config_dict = load_config(config_path)
    documents = read_documents(config_dict["data"]["dataset_path"])

    keyword_search_engine = KeywordSearchEngine()
    # Use add_documents which sets self.documents and calls create_inverted_index
    keyword_search_engine.add_documents(documents)
    
    query = "steel toe work boots"
    keyword_results = keyword_search_engine.search(query, top_k=10)
    print(f"Keyword Search Results for query '{query}':")
    for result in keyword_results:
        print(f"Doc ID: {result.doc_id}, Score: {result.score}, Content: {result.content}")


if __name__ == "__main__":
    main()