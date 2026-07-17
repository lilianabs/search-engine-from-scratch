import os
from typing import Tuple
import pandas as pd
import yaml


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
        content = f"{row['title']} {row['description']} {row['price']} {row['availability']}"
        doc_dict[doc_id] = content
    return doc_dict


def get_config_path(config_file_name: str) -> str:
    """Get the path to the config.yaml file located in the project root directory."""
    # Get the project root directory (parent of scripts directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, config_file_name)


def load_config(config_path: str) -> dict:
    """Load configuration from config.yaml file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    
def get_price_availability(id: str, documents: dict[str, str]) -> Tuple[str, str]:
    """Extract price and availability information from documents.

    Args:
        documents: Dictionary mapping document ID to document content.
    """
    price = documents[id].split()[-2]  # Assuming price is the second last word
    availability = documents[id].split()[-1]  # Assuming availability is the last word
    
    return price, availability
