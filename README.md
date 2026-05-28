# GraphRAG Pipeline for Structured Financial Data

This repo is a compact assignment/demo for:

> Create a Graph RAG pipeline for structured data in Snowflake with a domain ontology mapped.

The domain is financial analytics. The demo is intentionally self-contained:

- SQLite stands in for Snowflake.
- An in-memory ontology graph stands in for Neo4j.
- A deterministic local synthesizer stands in for an LLM.

The architecture keeps the production boundary clear: Snowflake stores structured truth, while the ontology graph stores semantic business relationships and mappings from business concepts to warehouse tables/columns.

## Run the Demo

```bash
python demo.py
```

The default query is:

```text
Why did APAC retail revenue decline?
```

The demo prints each pipeline stage:

1. Query understanding
2. Ontology grounding
3. Semantic graph expansion
4. Governed SQL
5. Structured retrieval
6. Ranked context
7. Grounded response

## What to Present

Start with [`docs/architecture.md`](docs/architecture.md). It contains the core thesis, architecture diagram, ontology model, pipeline walkthrough, GraphRAG defense answers, and tradeoffs.

The short explanation:

> This is not a chatbot over Neo4j. It is an ontology-driven retrieval system where the graph provides business meaning and Snowflake provides governed truth.

## Project Layout

- `docs/architecture.md` - presentation-ready architecture writeup
- `ontology/ontology.yaml` - financial ontology with concept-to-warehouse mappings
- `data/schema.sql` - mock Snowflake star schema
- `data/seed.sql` - small APAC Retail decline dataset
- `src/graph_rag/` - local pipeline implementation
- `demo.py` - end-to-end demo

## Production Mapping

- `Warehouse` can be replaced with a Snowflake adapter.
- `OntologyStore` can be replaced with a Neo4j/Cypher adapter.
- `DeterministicFinancialAnalyst` can be replaced with an LLM client.
- `GraphRAGPipeline` can be wired into real LangGraph nodes.
