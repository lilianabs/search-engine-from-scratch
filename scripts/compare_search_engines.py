from dataclasses import dataclass
from typing import Type
from search_engine.keyword_search import KeywordSearchEngine
from search_engine.bm25_search import BM25SearchEngine
from search_engine.base import BaseSearchEngine
from utils import read_documents, get_config_path, load_config, get_price_availability


@dataclass
class SearchEngineMetrics:
    """Store performance metrics for a search engine."""
    engine_name: str
    query: str
    results_count: int
    top_result_score: float


def init_search_engine(
    engine_class: Type[BaseSearchEngine],
    documents: dict[str, str],
    config_dict: dict,
    engine_name: str
) -> BaseSearchEngine:
    """Initialize and persist a search engine."""
    engine = engine_class()
    engine.add_documents(documents)
    index_path = config_dict["index"][f"{engine_name}_inverted_index_path"]
    engine.save(index_path)
    engine.load(index_path)
    return engine


def search_and_display(
    engine: BaseSearchEngine,
    engine_name: str,
    query: str,
    config_dict: dict,
    top_k: int = 10
) -> SearchEngineMetrics:
    """Run search and display results."""
    results = engine.search(query, top_k=top_k)
    print(f"\n{engine_name.upper()} Search Results for query '{query}':")
    print(f"Found {len(results)} results\n")

    for i, result in enumerate(results, 1):
        price, availability = get_price_availability(
            result.doc_id, config_dict["data"]["dataset_path"]
        )
        print(f"{i}. Doc ID: {result.doc_id}")
        print(f"   Score: {result.score:.4f}")
        print(f"   Content: {result.content[:100]}...")
        print(f"   Price: {price}, Availability: {availability}")
        print("-" * 80)

    return SearchEngineMetrics(
        engine_name=engine_name,
        query=query,
        results_count=len(results),
        top_result_score=results[0].score if results else 0.0
    )


def main():
    config_file_name = "conf.yaml"
    config_path = get_config_path(config_file_name)
    config_dict = load_config(config_path)

    columns = ["title"]
    documents = read_documents(config_dict["data"]["dataset_path"], columns)

    engines_config = [
        ("keyword", KeywordSearchEngine),
        ("bm25", BM25SearchEngine),
        # ("semantic", SemanticSearchEngine),
        # ("hybrid", HybridSearchEngine),
    ]

    engines = {}
    for engine_name, engine_class in engines_config:
        engines[engine_name] = init_search_engine(engine_class, documents, config_dict, engine_name)

    query = "steel toe work boots"
    metrics = []

    for engine_name, engine in engines.items():
        metric = search_and_display(engine, engine_name, query, config_dict, top_k=10)
        metrics.append(metric)

    print("\n" + "=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)
    for metric in metrics:
        print(
            f"{metric.engine_name}: {metric.results_count} results, "
            f"top score: {metric.top_result_score:.4f}"
        )


if __name__ == "__main__":
    main()