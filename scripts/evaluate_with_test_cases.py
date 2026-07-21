import json
from typing import Dict, List
from dataclasses import dataclass
from search_engine.semantic_search import SemanticSearchEngine
from search_engine.keyword_search import KeywordSearchEngine
from search_engine.bm25_search import BM25SearchEngine
from utils import read_documents, get_config_path, load_config


@dataclass
class EvaluationResult:
    """Store evaluation metrics for a single test case."""
    query: str
    engine_name: str
    search_type: str
    relevant_docs: List[str]
    retrieved_docs: List[str]
    precision: float
    recall: float
    ndcg: float


def load_test_cases(test_cases_path: str) -> List[Dict]:
    """Load test cases from JSON file."""
    with open(test_cases_path, 'r') as f:
        return json.load(f)


def get_relevant_titles(test_case: Dict) -> set[str]:
    """Extract relevant document titles from test case."""
    return {result["title"] for result in test_case["expected_results"]}


def calculate_precision(retrieved: List[str], relevant: set[str]) -> float:
    """Calculate precision: fraction of retrieved docs that are relevant."""
    if not retrieved:
        return 0.0
    relevant_retrieved = sum(1 for doc in retrieved if doc in relevant)
    return relevant_retrieved / len(retrieved)


def calculate_recall(retrieved: List[str], relevant: set[str]) -> float:
    """Calculate recall: fraction of relevant docs that were retrieved."""
    if not relevant:
        return 0.0
    relevant_retrieved = sum(1 for doc in retrieved if doc in relevant)
    return relevant_retrieved / len(relevant)


def calculate_ndcg(retrieved: List[str], relevant: set[str], test_case: Dict, k: int = 10) -> float:
    """Calculate Normalized Discounted Cumulative Gain."""
    # Build relevance score map from test case
    relevance_map = {result["title"]: result["relevance"] for result in test_case["expected_results"]}

    # Calculate DCG
    dcg = 0.0
    for i, doc in enumerate(retrieved[:k], 1):
        relevance = relevance_map.get(doc, 0)
        dcg += relevance / (i ** 0.5)

    # Calculate IDCG (ideal DCG)
    ideal_relevances = sorted([result["relevance"] for result in test_case["expected_results"]], reverse=True)[:k]
    idcg = 0.0
    for i, relevance in enumerate(ideal_relevances, 1):
        idcg += relevance / (i ** 0.5)

    if idcg == 0:
        return 0.0
    return dcg / idcg


def evaluate_engine(engine, query: str, test_case: Dict, engine_name: str, top_k: int = 10) -> EvaluationResult:
    """Evaluate a search engine against a test case."""
    results = engine.search(query, top_k=top_k)
    retrieved_titles = [result.content.strip() if isinstance(result.content, str) else "" for result in results]
    relevant_titles = get_relevant_titles(test_case)

    precision = calculate_precision(retrieved_titles, relevant_titles)
    recall = calculate_recall(retrieved_titles, relevant_titles)
    ndcg = calculate_ndcg(retrieved_titles, relevant_titles, test_case, k=top_k)

    return EvaluationResult(
        query=query,
        engine_name=engine_name,
        search_type=test_case["search_type"],
        relevant_docs=list(relevant_titles),
        retrieved_docs=retrieved_titles,
        precision=precision,
        recall=recall,
        ndcg=ndcg
    )


def print_evaluation_report(results: List[EvaluationResult]):
    """Print evaluation results in a formatted table."""
    print("\n" + "=" * 100)
    print("EVALUATION REPORT")
    print("=" * 100)

    for result in results:
        print(f"\nQuery: '{result.query}'")
        print(f"Engine: {result.engine_name} | Search Type: {result.search_type}")
        print(f"Precision: {result.precision:.4f} | Recall: {result.recall:.4f} | nDCG: {result.ndcg:.4f}")
        print(f"Retrieved: {len(result.retrieved_docs)} docs | Relevant: {len(result.relevant_docs)} docs")
        print("-" * 100)


def main():
    config_file_name = "conf.yaml"
    config_path = get_config_path(config_file_name)
    config_dict = load_config(config_path)

    columns = ["title"]
    documents = read_documents(config_dict["data"]["dataset_path"], columns)

    # Load test cases
    test_cases_path = config_dict["data"]["test_cases_path"]
    test_cases = load_test_cases(test_cases_path)

    # Initialize search engines
    engines = {
        "keyword": KeywordSearchEngine(),
        "bm25": BM25SearchEngine(),
        "semantic": SemanticSearchEngine(model_name=config_dict.get("semantic_search", {}).get("model_name")),
    }

    for engine_name, engine in engines.items():
        engine.add_documents(documents)

    # Evaluate each test case
    all_results = []

    for test_case in test_cases:
        query = test_case["keyword"]
        search_type = test_case["search_type"]

        for engine_name, engine in engines.items():
            result = evaluate_engine(engine, query, test_case, engine_name, top_k=10)
            all_results.append(result)

            print(f"\n{'=' * 100}")
            print(f"Query: '{query}' | Engine: {engine_name.upper()}")
            print(f"{'=' * 100}")
            print(f"Precision: {result.precision:.4f}")
            print(f"Recall: {result.recall:.4f}")
            print(f"nDCG: {result.ndcg:.4f}")
            print(f"\nRetrieved {len(result.retrieved_docs)} relevant documents out of {len(result.relevant_docs)}")

    print_evaluation_report(all_results)

    # Summary statistics
    print("\n" + "=" * 100)
    print("SUMMARY STATISTICS")
    print("=" * 100)
    engines_summary = {}
    for engine_name in engines.keys():
        engine_results = [r for r in all_results if r.engine_name == engine_name]
        avg_precision = sum(r.precision for r in engine_results) / len(engine_results)
        avg_recall = sum(r.recall for r in engine_results) / len(engine_results)
        avg_ndcg = sum(r.ndcg for r in engine_results) / len(engine_results)
        engines_summary[engine_name] = {
            "avg_precision": avg_precision,
            "avg_recall": avg_recall,
            "avg_ndcg": avg_ndcg
        }

    for engine_name, metrics in engines_summary.items():
        print(f"\n{engine_name.upper()}:")
        print(f"  Average Precision: {metrics['avg_precision']:.4f}")
        print(f"  Average Recall: {metrics['avg_recall']:.4f}")
        print(f"  Average nDCG: {metrics['avg_ndcg']:.4f}")


if __name__ == "__main__":
    main()
