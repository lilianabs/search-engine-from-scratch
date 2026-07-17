from search_engine.keyword_search import KeywordSearchEngine
from utils import read_documents, get_config_path, load_config, get_price_availability


def main():
    # Get the project root directory (parent of scripts directory)
    config_file_name = "conf.yaml"
    config_path = get_config_path(config_file_name)
    config_dict = load_config(config_path)
    
    documents = read_documents(config_dict["data"]["dataset_path"])

    keyword_search_engine = KeywordSearchEngine()
    # Use add_documents which sets self.documents and calls create_inverted_index
    keyword_search_engine.add_documents(documents)
    keyword_search_engine.save(config_dict["index"]["keyword_inverted_index_path"])
    keyword_search_engine.load(config_dict["index"]["keyword_inverted_index_path"])
    
    query = "steel toe work boots"
    keyword_results = keyword_search_engine.search(query, top_k=10)
    print(f"Keyword Search Results for query '{query}':")
    for result in keyword_results:
        price, availability = get_price_availability(result.doc_id, documents)
        print(f"Doc ID: {result.doc_id}, \nScore: {result.score}, \nContent: {result.content}")
        print(f"Price: {price}, \nAvailability: {availability}")
        print("-" * 80)


if __name__ == "__main__":
    main()