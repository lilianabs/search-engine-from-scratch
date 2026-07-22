# Search engine from scratch

This project contains the implementation of the following search engines from scratch in Python:

- Keyword
- BM25
- Semantic
- Hybrid

## Table of Contents

- [search-engine-from-scratch](#search-engine-from-scratch)
  - [Table of Contents](#table-of-contents)
  - [Data](#data)
  - [Search Engine Evaluation Results](#search-engine-evaluation-results)
    - [Overall Performance Summary](#overall-performance-summary)
    - [Query-by-Query Performance](#query-by-query-performance)
      - [1. "steel toe work boots" (Keyword Query)](#1-steel-toe-work-boots-keyword-query)
      - [2. "waterproof jacket for cold weather" (Semantic Query) ⭐](#2-waterproof-jacket-for-cold-weather-semantic-query-)
      - [3. "blue paint for bedroom walls" (Hybrid Query)](#3-blue-paint-for-bedroom-walls-hybrid-query)
      - [4. "bathroom vanity mirror" (Keyword Query)](#4-bathroom-vanity-mirror-keyword-query)
      - [5. "something to keep my dog from escaping the yard" (Semantic Query) ⭐](#5-something-to-keep-my-dog-from-escaping-the-yard-semantic-query-)
    - [Key Findings](#key-findings)
  - [Evaluation Metrics](#evaluation-metrics)
    - [Precision](#precision)
    - [Recall](#recall)
    - [nDCG (Normalized Discounted Cumulative Gain)](#ndcg-normalized-discounted-cumulative-gain)
  - [Running the project](#running-the-project)
    - [Using the venv in VS CODE](#using-the-venv-in-vs-code)
    - [Running the search engine](#running-the-search-engine)

## Data
To test the search engines, we use the [Home Depot dataset](https://www.kaggle.com/datasets/thedevastator/the-home-depot-products-dataset) from Kaggle, which contains 2,551 product records from Home Depot. Each product includes metadata such as title, description, brand, price, SKU, and availability. This dataset serves as the foundation for developing and testing keyword, semantic, and hybrid search capabilities across ecommerce product catalogs.

**Note:** The query examples were generated with Claude Code.

## Search Engine Evaluation Results

### Overall Performance Summary

The semantic search engine outperforms keyword-based approaches, especially on semantic queries:

| Engine | Precision | Recall | nDCG |
|--------|-----------|--------|------|
| **Semantic** | **64.0%** | **58.6%** | **0.712** |
| Keyword | 44.0% | 28.3% | 0.425 |
| Hybrid | 46.0% | 31.0% | 0.439 |
| BM25 | 42.0% | 27.7% | 0.412 |

### Query-by-Query Performance

#### 1. "steel toe work boots" (Keyword Query)
- **Best Engine**: Keyword/BM25/Hybrid (tied)
- All engines: 100% Precision, 90.91% Recall, ~0.96 nDCG
- All engines perform well on explicit keyword matches
- Hybrid: 100% Precision, 90.91% Recall, 0.9693 nDCG (matches BM25)

#### 2. "waterproof jacket for cold weather" (Semantic Query) ⭐
- **Best Engine**: Semantic Search
- Semantic: 40% Precision, **100% Recall**, 0.9758 nDCG
- Keyword/BM25/Hybrid: 0% (unable to understand semantic intent)
- **Finding**: Semantic search excels at understanding natural language intent that keyword engines miss
- **Hybrid Limitation**: Equal-weight averaging dilutes semantic advantage when keyword engine fails completely

#### 3. "blue paint for bedroom walls" (Hybrid Query)
- Limited by title-only indexing (waterproof claims exist only in descriptions)
- All engines: ~30% Precision, ~9.4% Recall
- Hybrid: 30% Precision, 9.38% Recall, 0.1732 nDCG (comparable to individual engines)

#### 4. "bathroom vanity mirror" (Keyword Query)
- **Best Engine**: Semantic Search
- Semantic: **90% Precision**, 42.86% Recall, 0.9261 nDCG
- Hybrid: 80% Precision, 38.1% Recall, 0.9050 nDCG (slightly lower than semantic)
- Hybrid pulls semantic down by averaging with BM25

#### 5. "something to keep my dog from escaping the yard" (Semantic Query) ⭐
- **Best Engine**: Semantic Search
- Semantic: **60% Precision**, **50% Recall**, 0.5150 nDCG
- Keyword/BM25: 0% (fail to understand containment concept)
- Hybrid: 20% Precision, 16.67% Recall, 0.1461 nDCG (significantly underperforms)
- **Hybrid Limitation**: Equal-weight averaging dilutes semantic advantage when keyword engine has zero performance

### Key Findings

1. **Semantic Search Strengths** (nDCG: 0.712):
   - Excels at understanding semantic intent and natural language queries
   - Captures meaning beyond exact keyword matching
   - Better at synonyms and conceptual relationships
   - Consistently outperforms on semantic queries (4/5 test cases)

2. **Keyword/BM25 Strengths** (nDCG: 0.425/0.412):
   - Better for explicit keyword queries with exact matches
   - Lower computational overhead (no embedding models)
   - Predictable behavior for straightforward keyword matching

3. **Hybrid Search Performance** (nDCG: 0.439):
   - Moderate performance with 50/50 weighting
   - Achieves parity with keyword engines on explicit keyword queries
   - Significantly underperforms on semantic queries due to equal-weight averaging
   - When one engine fails completely (0% recall), averaging prevents the winning engine from dominating
   - **Limitation**: Current equal-weight scheme doesn't adapt to query type

4. **Recommendation**:
   - **For natural language queries**: Use semantic search directly (0.712 nDCG)
   - **For explicit keyword queries**: Use BM25 (0.412 nDCG is competitive)
   - **For hybrid approach**: Consider adaptive weighting (e.g., higher semantic weight for natural language queries)
   - Semantic search provides ~50% better overall performance with zero computational penalty for keyword-heavy indexing

## Evaluation Metrics

### Precision
Measures the fraction of retrieved documents that are relevant:

```
Precision = (# of relevant retrieved docs) / (# of retrieved docs)
```

**Example**: If you retrieve 10 documents and 4 are relevant, precision = 40%

### Recall
Measures the fraction of relevant documents that were successfully retrieved:

```
Recall = (# of relevant retrieved docs) / (# of total relevant docs)
```

**Example**: If there are 20 relevant documents total and you retrieve 8 of them, recall = 40%

### nDCG (Normalized Discounted Cumulative Gain)
Measures ranking quality by considering both relevance and position. Documents ranked higher contribute more to the score.

```
DCG = Σ(relevance_i / log₂(position_i + 1))
nDCG = DCG / IDCG (Ideal DCG with perfect ranking)
```

**How it works**:
- Relevance scores: Grade 2 = highly relevant, Grade 1 = somewhat relevant, Grade 0 = not relevant
- Position matters: A relevant document at position 1 is worth much more than at position 10
- Normalized: nDCG ranges from 0 to 1, where 1 = perfect ranking

**Example**:
- Retrieved order: [Grade 2, Grade 0, Grade 1, Grade 2, ...]
- Position 1 (Grade 2): 2 / log₂(2) = 2.0
- Position 2 (Grade 0): 0 / log₂(3) = 0
- Position 3 (Grade 1): 1 / log₂(4) = 0.5
- Position 4 (Grade 2): 2 / log₂(5) = 0.86
- DCG = 2.0 + 0 + 0.5 + 0.86 = 3.36

**Why nDCG is important**: It rewards good ranking order while penalizing relevant documents that appear late in results.


## Running the project
Before installing the project locally, make sure you have **Python 3.13+** and [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

To install the project, follow these steps:

1. Create a new virtual environment:

   ```
   uv venv venv --python 3.13
   ```

1. Activate the Python environment:

   ```
   source venv/bin/activate
   ```

1. Install the project dependencies:

   ```
   uv sync
   ```

1. Install the project locally:

   ```
   uv pip install -e .
   ```

### Using the venv in VS CODE

If you are modifying the project using VS CODE then create the file `.vscode/settings.json` with the following lines:

   ```
  {
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
  }
   ```

### Running the search engine

To run the comparison of all search engines:

```bash
uv run python scripts/compare_search_engines.py
```

To evaluate search engines against test cases:

```bash
uv run python scripts/evaluate_with_test_cases.py
```
