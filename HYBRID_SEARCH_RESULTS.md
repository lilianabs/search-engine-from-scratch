# Hybrid Search Engine Evaluation Results

## Overview
This document contains the comprehensive evaluation results of the Hybrid Search Engine, which combines BM25 (keyword) and Semantic search with equal weighting (50/50).

## Summary Statistics

| Engine | Precision | Recall | nDCG |
|--------|-----------|--------|------|
| **Semantic** | **64.0%** | **58.6%** | **0.712** |
| Keyword | 44.0% | 28.3% | 0.425 |
| **Hybrid** | **46.0%** | **31.0%** | **0.439** |
| BM25 | 42.0% | 27.7% | 0.412 |

## Query-by-Query Results

### Query 1: "steel toe work boots" (Keyword Query)

| Engine | Precision | Recall | nDCG | Status |
|--------|-----------|--------|------|--------|
| Keyword | 100% | 90.91% | 1.0000 | ✅ Best |
| BM25 | 100% | 90.91% | 0.9693 | ✅ |
| Semantic | 100% | 90.91% | 0.9434 | ✅ |
| **Hybrid** | **100%** | **90.91%** | **0.9693** | ✅ **Matches BM25** |

**Analysis**: Hybrid engine performs excellently on explicit keyword queries, matching BM25's performance. This query benefits from equal weighting since both engines perform well.

---

### Query 2: "waterproof jacket for cold weather" (Semantic Query) ⭐

| Engine | Precision | Recall | nDCG | Status |
|--------|-----------|--------|------|--------|
| Keyword | 0% | 0% | 0.0000 | ❌ |
| BM25 | 0% | 0% | 0.0000 | ❌ |
| Semantic | 40% | **100%** | **0.9758** | ✅ **Best** |
| **Hybrid** | **0%** | **0%** | **0.0000** | ❌ **Failure** |

**Analysis**: Critical failure point for hybrid engine. When BM25 returns 0% recall (completely wrong results), averaging with semantic's 40% precision pulls the score down to 0%. The keyword engine's irrelevant results contaminate the hybrid results.

**Issue**: Equal-weight averaging assumes both engines contribute value. This assumption breaks when one engine completely fails.

---

### Query 3: "blue paint for bedroom walls" (Hybrid Query)

| Engine | Precision | Recall | nDCG | Status |
|--------|-----------|--------|------|--------|
| Keyword | 40% | 12.50% | 0.2592 | ⚠️ |
| BM25 | 30% | 9.38% | 0.1772 | ⚠️ |
| Semantic | 30% | 9.38% | 0.1998 | ⚠️ |
| **Hybrid** | **30%** | **9.38%** | **0.1732** | ⚠️ **Below semantic** |

**Analysis**: Limited by title-only indexing. Hybrid underperforms semantic slightly (0.1732 vs 0.1998 nDCG) because it averages with BM25's lower score.

---

### Query 4: "bathroom vanity mirror" (Keyword Query)

| Engine | Precision | Recall | nDCG | Status |
|--------|-----------|--------|------|--------|
| Keyword | 80% | 38.10% | 0.8671 | ✅ |
| BM25 | 80% | 38.10% | 0.9111 | ✅ |
| Semantic | **90%** | **42.86%** | **0.9261** | ✅ **Best** |
| **Hybrid** | **80%** | **38.10%** | **0.9050** | ✅ **Good** |

**Analysis**: Hybrid performs well but below semantic. Semantic's superior precision (90%) is diluted by BM25's lower score (80%) in the 50/50 average.

---

### Query 5: "something to keep my dog from escaping the yard" (Semantic Query) ⭐

| Engine | Precision | Recall | nDCG | Status |
|--------|-----------|--------|------|--------|
| Keyword | 0% | 0% | 0.0000 | ❌ |
| BM25 | 0% | 0% | 0.0000 | ❌ |
| Semantic | **60%** | **50%** | **0.5150** | ✅ **Best** |
| **Hybrid** | **20%** | **16.67%** | **0.1461** | ❌ **Significant Underperformance** |

**Analysis**: Another critical failure for hybrid. Semantic engine finds 60% precision and 50% recall, but averaging with BM25's 0% results in only 20% precision. This is the worst hybrid result (0.1461 vs 0.5150 nDCG).

---

## Key Insights

### When Hybrid Works Well
1. **Explicit keyword queries** (Query 1): Both engines perform well, averaging provides stable results
2. **Moderate semantic queries** (Query 4): Benefits from combining signals

### When Hybrid Fails
1. **Semantic queries where BM25 fails completely** (Queries 2 & 5):
   - BM25 returns 0% recall (irrelevant results)
   - Averaging a 40% precision with 0% precision yields 20% combined precision
   - Semantic alone would have achieved 40-60% precision

2. **The 50/50 weighting problem**:
   - Assumes both engines are equally reliable
   - Doesn't account for query type (keyword vs semantic)
   - Doesn't account for engine confidence or performance variance

### Recommendations

#### For Production Use
1. **Use Semantic Search directly** for best overall performance (0.712 nDCG)
   - Handles both keyword and semantic queries well
   - No computational overhead for BM25
   - Consistent high performance

2. **Use BM25 only for known keyword-heavy datasets**
   - More efficient computationally
   - Acceptable performance on explicit keyword queries

3. **Hybrid should use adaptive weighting**:
   - Higher semantic weight for natural language queries
   - Higher BM25 weight for technical/exact-match queries
   - Query classification layer to determine optimal weights
   - OR: Use semantic confidence scores to weight results

#### For Current Hybrid Engine
- Consider increasing semantic_weight to 0.7-0.8 (from 0.5)
- Implement query type detection
- Use relevance score normalization to prevent zero-score dominance

## Conclusion

The hybrid engine with equal weighting (50/50) achieves **0.439 nDCG**, which is:
- **Better than BM25 alone** (0.412)
- **Worse than Semantic alone** (0.712)
- **Same as Keyword** (0.425)

**Current hybrid implementation is not recommended** for production use. The semantic search engine alone provides superior and more stable performance across all query types.
