from search_engine.keyword_search import KeywordSearchEngine
from search_engine.bm25_search import BM25SearchEngine
from utils import read_documents, get_config_path, load_config, get_price_availability


def init_keyword_search_engine(documents, config_dict) -> KeywordSearchEngine:
    keyword_search_engine = KeywordSearchEngine()
    # Use add_documents which sets self.documents and calls create_inverted_index
    keyword_search_engine.add_documents(documents)
    keyword_search_engine.save(config_dict["index"]["keyword_inverted_index_path"])
    keyword_search_engine.load(config_dict["index"]["keyword_inverted_index_path"])
    return keyword_search_engine

def init_bm25_search_engine(documents, config_dict) -> BM25SearchEngine:
    bm25_search_engine = BM25SearchEngine()
    bm25_search_engine.add_documents(documents)
    bm25_search_engine.save(config_dict["index"]["bm25_inverted_index_path"])
    bm25_search_engine.load(config_dict["index"]["bm25_inverted_index_path"])
    return bm25_search_engine
    

def main():
    # Get the project root directory (parent of scripts directory)
    config_file_name = "conf.yaml"
    config_path = get_config_path(config_file_name)
    config_dict = load_config(config_path)
    
    columns = ["title"]
    documents = read_documents(config_dict["data"]["dataset_path"], columns)

    keyword_search_engine = init_keyword_search_engine(documents, config_dict)
    bm25_search_engine = init_bm25_search_engine(documents, config_dict)
    
    query = "steel toe work boots"
    
    keyword_results = keyword_search_engine.search(query, top_k=10)
    print(f"Keyword Search Results for query '{query}':")
    for result in keyword_results:
        price, availability = get_price_availability(result.doc_id, config_dict["data"]["dataset_path"])
        print(f"Doc ID: {result.doc_id}, \nScore: {result.score}, \nContent: {result.content}")
        print(f"Price: {price}, \nAvailability: {availability}")
        print("-" * 80)
        
    bm25_results = bm25_search_engine.search(query, top_k=10)
    print(f"BM25 Search Results for query '{query}':")
    for result in bm25_results:
        price, availability = get_price_availability(result.doc_id, config_dict["data"]["dataset_path"])
        print(f"Doc ID: {result.doc_id}, \nScore: {result.score}, \nContent: {result.content}")
        print(f"Price: {price}, \nAvailability: {availability}")
        print("-" * 80)


if __name__ == "__main__":
    main()