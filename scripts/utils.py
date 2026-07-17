import os
from typing import Tuple
import pandas as pd
import yaml


def read_documents(file_path: str, columns: list[str]) -> dict[str, str]:
    """Read documents from a csv file

    Args:
        file_path: Path to the file containing documents.
        columns: List of column names to include in the document content.

    Returns:
        Dictionary mapping document ID to document content.
    """
    documents = pd.read_csv(file_path)
    doc_dict = {}
    for _, row in documents.iterrows():
        doc_id = str(row["index"])
        content = " ".join(str(row[col]) for col in columns)
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
    
def get_price_availability(id: str, csv_path: str) -> Tuple[str, str]:
    """Extract price and availability information from a CSV file.

    Args:
        id: Document ID to look up.
        csv_path: Path to the CSV file containing price and availability data.

    Returns:
        Tuple of (price, availability) for the given document ID.
    """
    df = pd.read_csv(csv_path)
    row = df[df["index"] == int(id)].iloc[0]
    return str(row["price"]), str(row["availability"])
