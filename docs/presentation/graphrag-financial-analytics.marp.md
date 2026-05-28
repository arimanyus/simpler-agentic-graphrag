---
marp: true
theme: default
paginate: true
size: 16:9
---

# GraphRAG for Structured Financial Analytics

## Problem

Enterprise finance questions require more than table lookup.

> Why did APAC Retail revenue decline?

The system must understand:

- business entities: `APAC`, `Retail`, `Revenue`
- hierarchies: APAC -> Japan, India, Singapore
- KPI dependencies: Revenue -> Units Sold, Refunds, Net Revenue
- governed data: Snowflake remains the source of truth

**Core thesis:** GraphRAG is ontology-driven, relationship-aware retrieval orchestration over structured enterprise data.

<!--
Speaker notes:
Start by translating the assignment into the real evaluation: can the system reason over structured enterprise data using business semantics?
Emphasize that this is not "chat with Neo4j."
-->

---

# Architecture

## Snowflake for Truth, Graph for Meaning

Use this as the main architecture diagram:

`docs/diagrams/graphrag-deep-architecture.drawio`

Flow:

1. User asks a business analytics question.
2. LangGraph extracts entities, intent, and constraints.
3. Ontology grounding maps words to business concepts.
4. Retrieval splits into graph expansion + governed Snowflake SQL.
5. Context builder combines metrics and semantic evidence.
6. LLM synthesizes a grounded business answer.

**Important:** The graph does not replace Snowflake. It makes Snowflake retrieval semantically intelligent.

<!--
Speaker notes:
Spend the most time here.
Walk left-to-right through the diagram.
Say: Snowflake stores truth; the ontology graph stores meaning; LangGraph decides retrieval; the LLM explains grounded evidence.
-->

---

# Domain Ontology

## The Semantic Layer That Makes This GraphRAG

The ontology models:

- concepts: Region, Business Unit, Metric, KPI, Customer Segment, Product
- hierarchies: APAC -> Japan, India, Singapore
- dependencies: Revenue -> Units Sold, Refunds, Net Revenue
- KPI logic: Profitability -> Net Revenue and Expense
- mappings: business concepts -> Snowflake tables and columns

Examples:

- Japan `rolls_up_to` APAC
- Revenue `depends_on` Units Sold
- Refunds `impacts` Revenue
- Revenue -> `fact_sales.revenue`
- APAC -> `dim_region.parent_region = 'APAC'`

**Why it matters:** the ontology prevents the LLM from guessing business meaning or inventing SQL.

It turns a vague business question into grounded retrieval instructions.

<!--
Speaker notes:
Spend time here. This is what makes the assignment GraphRAG.
Say: the ontology is not just visualization; it is an operational semantic layer that maps language to business concepts and warehouse fields.
Strong line: SQL joins connect tables, but the ontology explains what the connections mean.
-->

---

# Example + Defense

## "Why did APAC Retail revenue decline?"

Grounding:

- `Revenue`, `APAC`, `Retail`, `root cause`
- APAC -> Japan, India, Singapore
- Revenue -> Units Sold, Refunds, Net Revenue

Demo result:

- revenue declined from **350,000** to **283,000**
- change = **-67,000 (-19.1%)**
- refunds increased by **17,000**
- units decreased by **65**

Why GraphRAG:

- Standard RAG retrieves similar chunks.
- GraphRAG expands retrieval through explicit relationships.
- SQL returns governed truth; graph traversal adds business meaning.

Tradeoff:

The ontology must be maintained, versioned, governed, and synchronized with Snowflake.

<!--
Speaker notes:
This proves the architecture is concrete.
The system does not dump raw rows into the LLM. It creates analytical evidence packets: metric deltas, hierarchy facts, and related KPI drivers.
Run: python demo.py
Snowflake remains governed truth; the graph provides the semantic layer that makes retrieval business-aware.
That is what makes this GraphRAG, not RAG plus a graph database.
-->
