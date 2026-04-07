from ingestion_pipeline import ingest_documents
from hybrid_retrieval import hybrid_mock_retrieve
from evaluation import load_ground_truth, evaluate_queries

chunks = ingest_documents()  # All chunks from your .txt files
ground_truth = load_ground_truth()  # Ground truth data for evaluation


# Define queries and their corresponding query types for evaluation (Query type is used to generate mock llm responses)
queries = [
    {
        "query_text": "When did the contruction begin for the Harbor Residential Complex Project?",
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

results = evaluate_queries(queries, retrieved_results, correct_chunks, ground_truth)


# Main evalution results
print("=== Evaluation Results ===")
print(f"Top-1 Accuracy: {results['top1_accuracy'] * 100:.1f}%")
print(f"Top-3 Accuracy: {results['top3_accuracy'] * 100:.1f}%")
print(f"LLM Response Accuracy: {results['info_correctness'] * 100:.1f}%")
print("=" * 60)
print("\n\nDetailed query results:")


# Detailed hybrid retrieval results for each query
for i, query in enumerate(queries):
    print(f"\nQuery {i + 1}: {query['query_text']}")
    print(f"Query type: {query['query_type']}")
    print("Top-5 retrieved chunks (filename, chunk_index, score):")
    for rank, r in enumerate(retrieved_results[i], 1):
        print(
            f"Rank {rank}: {r['chunk']['filename']}, chunk {r['chunk']['chunk_index']}, final_score={r['final_score']:.3f}"
        )
    correct = correct_chunks[i]
    print(
        f"Correct chunk should be: {correct['filename']}, chunk {correct['chunk_index']}"
    )
