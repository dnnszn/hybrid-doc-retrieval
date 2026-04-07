# Hybrid Information Retrieval Pipeline for Construction Documents

A high-level prototype project, demonstrating data ingestion, hybrid chunk retrieval (BM25 + semantic), structured information extraction and evalution on noisy construction data.

---

## Motivation

Construction projects generate highly **unstructured, heterogeneous data** (PDFs, reports, scans), making reliable information extraction challenging.

This project simulates a real-world pipeline for:

- Document ingestion
- Hybrid retrieval (BM25 + semantic)
- Structured information extraction
- Evaluation with ground truth (Top-1/Top-3 Chunk Retrieval, LLM Response Accuracy)

The goal is to demonstrate practical system design decisions for applied AI in such environments.

---

## Key Features

### 1. Document Ingestion & Chunking
- Processes noisy .txt documents (simulating PDFs)
- Splits into overlapping chunks
- Preserves metadata (`filename`, `chunk_index`)
- No chunk vectorization (Since I am simulating mock LLM responses, vectorization is not done. Please refer to ingestion_pipeline.py)

### 2. Hybrid Retrieval
- Combines:
  - **BM25 (0.9 weight)** — strong lexical baseline
  - **Semantic score (0.1 weight)** — simulated embeddings (Since no real embeddings are used, the weight is set to 0.1)
- Returns **Top-K (K=5)** chunks per query

### 3. Evaluation Pipeline
- **Top-1 Chunk Accuracy**
- **Top-3 Chunk Accuracy**
- **LLM Response Accuracy**
- Evaluation results are created as both a structured JSON file, and .txt file. Please refer to the `output` folder.

### 4. Relevant Details
- The data used, which is in the `data` folder, is generated to simulate real-life messy construction documents. To simulate this, different wording and formatting has been used across the .txt files.
- The ground truths reside in the `ground_truth.json` file, which is used to simulate evaluation of real-life systems. This is also used to generate the mock LLM responses.
- The chunks are not vectorized, and no vector database is used. Since this project serves as a high-level prototype, the semantic search is set to a random value of 0 and 1. This is also why the semantic search has a weight of 0.1 in the hybrid chunk retrieval.

---

## Project Structure
```
project/
├── data/                           # Noisy construction related documents
├── output/                         # Output of running main.py
├── src/
│   ├── ground_truth.json           # Structured ground truth for evaluation
│   ├── ingestion_pipeline.py
│   ├── hybrid_retrieval.py
│   ├── evaluation.py
│   └── main.py
├── .gitignore
├── pyproject.toml
├── poetry.lock
├── README.md
```
---

## How to Run

### 1. Install dependencies
`poetry install`

### 2. Run the Pipeline
`python src/main.py`

---

## Example Query
```json
{
    "query_text": "When did the construction begin for the Harbor Residential Complex Project?",
    "query_type": "start_date",
}
```

In order to simulate evaluation, the script also requires the ground truth chunk while creating a query (For more detail, please refer to main.py).
The filename refers to the relevant .txt file in the `data` folder, followed by the correct chunk index:

`["filename"] == "project_residential.txt" and c["chunk_index"] == 0`

---

### Example Output

Here is how the relevant output would look like for the previous example in the "Example Query" section.

- For the JSON output file:
```json
{
      "query": "When did the construction begin for the Harbor Residential Complex Project?",
      "query_type": "start_date",
      "retrieved_chunks": [
        {
          "rank": 1,
          "filename": "project_residential.txt",
          "chunk_index": 0,
          "score": 0.9806360046845569
        },
        {
          "rank": 2,
          "filename": "project_riverside.txt",
          "chunk_index": 0,
          "score": 0.6364469980749788
        },
        {
          "rank": 3,
          "filename": "project_bridge.txt",
          "chunk_index": 2,
          "score": 0.48357446156450806
        },
        {
          "rank": 4,
          "filename": "project_airport.txt",
          "chunk_index": 0,
          "score": 0.4835098068849069
        },
        {
          "rank": 5,
          "filename": "project_skyline.txt",
          "chunk_index": 0,
          "score": 0.4659278039048042
        }
      ],
      "correct_chunk": {
        "filename": "project_residential.txt",
        "chunk_index": 0
      }
    }
```
- For the .txt output file:
```
Query 1: When did the construction begin for the Harbor Residential Complex Project?
Query type: start_date
Top-1 chunk filename: project_residential.txt, chunk index: 0
Expected info: 2025-02-14
Retrieved info: 2025-02-14
Top-1 hit: 1, Top-3 hit: 1, LLM Response: 1

Detailed query results:

Query 1: When did the construction begin for the Harbor Residential Complex Project?
Query type: start_date
Top-5 retrieved chunks (filename, chunk_index, score):
Rank 1: project_residential.txt, chunk 0, final_score=0.981
Rank 2: project_riverside.txt, chunk 0, final_score=0.636
Rank 3: project_bridge.txt, chunk 2, final_score=0.484
Rank 4: project_airport.txt, chunk 0, final_score=0.484
Rank 5: project_skyline.txt, chunk 0, final_score=0.466
Correct chunk should be: project_residential.txt, chunk 0
```

---

## Design Choices

### Why no real embeddings/LLM?
- This prototype mainly focuses on the pipeline design, evaluation, and high level understanding of creating such projects. In real implementations, the chunks would be vectorized with an LLM, and stored with its relevant metadata in a vector database. A dummy function, `vectorize_chunks`, is created in the ingestion_pipeline.py file to simulate this step.
- This also means that the semantic search and LLM responses are psuedo. For this reason, the semantic search has a weight of 0.1 in the hybrid retrieval pipeline, which is assigned a random value between 0 and 1. For the final evaluation part, the LLM response is set to 1 if the the top-1 retrieved chunk is the correct one. In this scenario, to mimic an LLM response, the relevant piece of information is retrieved from the `ground_truth.json` file.

### Why .txt files for messy input documents?
- .txt files with different wording and formatting were generated to simulate real-life messy data and documents. In real-life scenarios, especially for construction related documents, other formats are more common (pdf, scans, over drawing). For such cases, libraries that help to process such documents or LLMs would be used.

### Why Hybrid Retrieval?
- BM25 is useful for exact word matches and structured keywords.
- Semantic Retrieval is useful for situations like paraphrasing, missing keywords and typos. It is a great way of retrieving relevant chunks without necessarily relying on exact word matching.
- The combination of BM25 and Semantic Retrieval brings the best out of each other. The weights of them in a hybrid retrieval pipeline would change based on the project and data. In this prototype, BM25 has a weight of 0.9 and the semantic retrieval has a weight of 0.1. As already mentioned, this choice was made due to not vectorizing chunks, and simulating semantic retrieval scores with a random value between 0 and 1.

### Why include ground truths and evalution in a prototype project?
- Observability (logging, tracing, etc.) is a crucial part of real-life projects. Although working with dummy data and mock llm responses, having an evaluation pipeline to such a project was required to present a complete prototype version. In a real project, the vectorized chunks would be stored in a vector database with more metadata, logging pipelines can be setup with an external tool such as Grafana (Loki, OpenTelemetry), and a much bigger and high-quality ground truth document would be essential to debug, improve and understand certain system/LLM behaviours.

---

## Final Thoughts

This project was built to demonstrate:
- Ability in building end-to-end applied AI systems.
- Having a high-level understanding in how such systems are built with real-life data and LLMs.
- Understanding why Hybrid Information Retrieval is useful and necessary.
- Acknowledging that steps such as evaluation and observability are as essential as other steps.

---

## Closing

Happy to walk through my design choices, tradeoffs, and how I would implement this in a real-life project!