import os
import json
from datetime import datetime

from ingestion_pipeline import ingest_documents
from hybrid_retrieval import hybrid_mock_retrieve
from evaluation import load_ground_truth, evaluate_queries

# Create output directory and define paths for logs and results
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = os.path.join(OUTPUT_DIR, f"run_{timestamp}.txt")
json_path = os.path.join(OUTPUT_DIR, f"run_{timestamp}.json")


def log(message, file):
    print(message)
    file.write(message + "\n")


chunks = ingest_documents()  # All chunks from your .txt files
ground_truth = load_ground_truth()  # Ground truth data for evaluation


# Define queries and their corresponding query types for evaluation (Query type is used to generate mock llm responses)
queries = [
    {
        "query_text": "When did the construction begin for the Harbor Residential Complex Project?",
        "query_type": "start_date",
    },
    {
        "query_text": "What materials are used in Central City Hospital Upgrade?",
        "query_type": "materials",
    },
    {
        "query_text": "When is the expected completion date for the Riverside Complex?",
        "query_type": "completion_date",
    },
    {
        "query_text": "What is the start date of the Solar Plant Delta project?",
        "query_type": "start_date",
    },
    {
        "query_text": "What are the materials used in Skyline Tower project?",
        "query_type": "materials",
    },
]

# For demo purposes, assume we know the indices of correct chunks, which we accept as ground truth chunks for evaluation.
correct_chunks = [
    next(c for c in chunks if c["filename"] == "project_residential.txt" and c["chunk_index"] == 0),
    next(c for c in chunks if c["filename"] == "project_hospital.txt" and c["chunk_index"] == 2),
    next(c for c in chunks if c["filename"] == "project_riverside.txt" and c["chunk_index"] == 0),
    next(c for c in chunks if c["filename"] == "project_solar.txt" and c["chunk_index"] == 0),
    next(c for c in chunks if c["filename"] == "project_skyline.txt" and c["chunk_index"] == 1),
]

retrieved_results = []

for query in queries:
    ranked_chunks = hybrid_mock_retrieve(query["query_text"], chunks, top_k=5)
    retrieved_results.append(ranked_chunks)

# Logging main evalution results
with open(output_path, "w", encoding="utf-8") as f:
    log(f"Run timestamp: {timestamp}", f)
    results = evaluate_queries(queries, retrieved_results, correct_chunks, ground_truth, log_fn = lambda msg: log(msg, f))
    log("=== Evaluation Results ===", f)
    log(f"Top-1 Accuracy: {results['top1_accuracy'] * 100:.1f}%", f)
    log(f"Top-3 Accuracy: {results['top3_accuracy'] * 100:.1f}%", f)
    log(f"LLM Response Accuracy: {results['info_correctness'] * 100:.1f}%", f)
    log("=" * 60, f)
    log("\n\nDetailed query results:", f)

    # Detailed hybrid retrieval results for each query
    for i, query in enumerate(queries):
        log(f"\nQuery {i + 1}: {query['query_text']}", f)
        log(f"Query type: {query['query_type']}", f)
        log("Top-5 retrieved chunks (filename, chunk_index, score):", f)
        for rank, r in enumerate(retrieved_results[i], 1):
            log(
                f"Rank {rank}: {r['chunk']['filename']}, chunk {r['chunk']['chunk_index']}, final_score={r['final_score']:.3f}",
                f,
            )
        correct = correct_chunks[i]
        log(
            f"Correct chunk should be: {correct['filename']}, chunk {correct['chunk_index']}",
            f,
        )

# Logging structured results in JSON format for potential future use and analysis
structured_results = {
    "metrics": {
        "top1_accuracy": results["top1_accuracy"],
        "top3_accuracy": results["top3_accuracy"],
        "llm_response_accuracy": results["info_correctness"],
    },
    "queries": [],
}

for i, query in enumerate(queries):
    structured_results["queries"].append(
        {
            "query": query["query_text"],
            "query_type": query["query_type"],
            "retrieved_chunks": [
                {
                    "rank": rank + 1,
                    "filename": r["chunk"]["filename"],
                    "chunk_index": r["chunk"]["chunk_index"],
                    "score": r["final_score"],
                }
                for rank, r in enumerate(retrieved_results[i])
            ],
            "correct_chunk": {
                "filename": correct_chunks[i]["filename"],
                "chunk_index": correct_chunks[i]["chunk_index"],
            },
        }
    )

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(structured_results, f, indent=2)