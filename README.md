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