import json


def load_ground_truth(path="src/ground_truth.json"):
    """
    Load the ground truth JSON file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_top1(retrieved_chunks, correct_chunk):
    """
    Check if the correct chunk is ranked first.
    """
    return int(retrieved_chunks[0]["chunk"] == correct_chunk)


def check_top3(retrieved_chunks, correct_chunk):
    """
    Check if the correct chunk is in the top 3.
    """
    top3 = [c["chunk"] for c in retrieved_chunks[:3]]
    return int(correct_chunk in top3)


def deterministic_mock_llm(
    retrieved_top1_chunk, query_type, ground_truth_item, correct_chunk
):
    """
    Simulate LLM output:
    - If the correct chunk is ranked #1, return the ground truth value from ground_truth.json.
    - Else, return a failure placeholder.
    """
    if retrieved_top1_chunk["chunk"] == correct_chunk:
        # Return the expected info from ground truth
        if query_type in ["start_date", "completion_date"]:
            return ground_truth_item[query_type]
        elif query_type == "materials":
            return ", ".join(ground_truth_item["materials"])
    else:
        return "[NOT FOUND]"


def evaluate_queries(queries, retrieved_results, correct_chunks, ground_truth):
    """
    Evaluate queries with Top-1, Top-3, and deterministic mock LLM info correctness.
    """
    top1_scores = []
    top3_scores = []
    info_scores = []

    print("=" * 60)

    for i, query in enumerate(queries):
        retrieved_top_k = retrieved_results[i]
        correct_chunk = correct_chunks[i]

        # Ground truth item by filename
        gt_item = next(item for item in ground_truth if item["file_name"] == correct_chunk["filename"])

        # Top-k checks
        top1 = check_top1(retrieved_top_k, correct_chunk)
        top3 = check_top3(retrieved_top_k, correct_chunk)

        # Mock LLM deterministic retrieval
        retrieved_info = deterministic_mock_llm(
            retrieved_top_k[0], query["query_type"], gt_item, correct_chunk
        )
        info_correct = int(retrieved_info != "[NOT FOUND]")

        top1_scores.append(top1)
        top3_scores.append(top3)
        info_scores.append(info_correct)

        # Detailed evaluation output
        print(f"Query {i + 1}: {query['query_text']}")
        print(f"Query type: {query['query_type']}")
        print(
            f"Top-1 chunk filename: {retrieved_top_k[0]['chunk']['filename']}, chunk index: {retrieved_top_k[0]['chunk']['chunk_index']}"
        )
        print(
            f"Expected info: {gt_item[query['query_type']] if query['query_type'] != 'materials' else ', '.join(gt_item['materials'])}"
        )
        print(f"Retrieved info: {retrieved_info}")
        print(f"Top-1 hit: {top1}, Top-3 hit: {top3}, LLM Response: {info_correct}")
        print("-" * 60)

    results = {
        "top1_accuracy": sum(top1_scores) / len(top1_scores),
        "top3_accuracy": sum(top3_scores) / len(top3_scores),
        "info_correctness": sum(info_scores) / len(info_scores),
    }

    return results
