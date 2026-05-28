# GraphRAG Pipeline for Structured Financial Data

## Slide 1 — What Problem Are We Solving?

### Title
GraphRAG for Structured Financial Analytics in Snowflake

### Slide Content

Enterprise finance questions are rarely just lookup questions.

Example:

> Why did APAC Retail revenue decline?

To answer this well, the system must understand:

- business entities: APAC, Retail, Revenue
- hierarchies: APAC includes Japan, India, Singapore
- KPI dependencies: Revenue relates to Units Sold, Refunds, Net Revenue, Profitability
- governed structured data: Snowflake remains the source of truth

### Key Message

GraphRAG is not "chat with a graph database."

It is:

> ontology-driven, relationship-aware retrieval orchestration over structured enterprise data.

### Speaker Notes

Open with the assignment statement and translate it into the real test: can the system reason over structured enterprise data using business semantics?

Say:

"A raw SQL schema can tell us which tables join. It does not reliably tell us what APAC means, which metrics drive revenue, or which related KPIs should be considered for root-cause analysis. That is why the ontology layer matters."

---

## Slide 2 — Architecture

### Title
Architecture: Snowflake for Truth, Graph for Meaning

### Slide Content

Use the draw.io diagram:

`docs/diagrams/graphrag-deep-architecture.drawio`

Core components:

- User/API layer receives the natural-language analytics question
- LangGraph orchestrates query understanding, grounding, retrieval, reranking, and synthesis
- Ontology graph stores business concepts, relationships, hierarchies, and warehouse mappings
- Snowflake stores facts, dimensions, KPI marts, and governed aggregates
- Vector index optionally supports glossary terms, metric definitions, and examples
- Governance layer enforces access control, SQL guardrails, mapping registry, evaluation, and observability

### Speaker Notes

This is the main slide. Spend the most time here.

Walk left to right:

1. User asks a business question.
2. The orchestrator extracts entities and intent.
3. Ontology grounding maps words to business concepts.
4. Retrieval splits into two branches:
   - graph branch for semantic expansion
   - Snowflake branch for governed metrics
5. Context builder combines metrics and graph evidence.
6. LLM synthesizes a grounded response.

Important line:

"The graph does not replace Snowflake. It makes Snowflake retrieval more intelligent by adding business meaning before SQL is generated."

---

## Slide 3 — Domain Ontology

### Title
Ontology: The Semantic Layer That Makes This GraphRAG

### Slide Content

The ontology is the business reasoning layer between natural language and Snowflake.

It models:

- business concepts: Region, Business Unit, Metric, KPI, Customer Segment, Product
- business hierarchies: APAC -> Japan, India, Singapore
- metric dependencies: Revenue -> Units Sold, Refunds, Net Revenue
- KPI reasoning: Profitability depends on Net Revenue and Expense
- warehouse mappings: business concepts -> Snowflake tables and columns

### Example Ontology Relationships

- Japan `rolls_up_to` APAC
- India `rolls_up_to` APAC
- Singapore `rolls_up_to` APAC
- Revenue `depends_on` Units Sold
- Refunds `impacts` Revenue
- Net Revenue `depends_on` Revenue and Refunds
- Profitability `depends_on` Net Revenue and Expense

### Example Warehouse Mappings

- Revenue -> `fact_sales.revenue`
- Refunds -> `fact_sales.refunds`
- APAC -> `dim_region.parent_region = 'APAC'`
- Retail -> `dim_business_unit.name = 'Retail'`

### Why This Matters

The ontology prevents the LLM from guessing business meaning or inventing SQL.

It turns:

> "Why did APAC Retail revenue decline?"

into grounded retrieval instructions:

- expand APAC into child regions
- retrieve Revenue, Refunds, Units Sold, Net Revenue
- constrain SQL to Retail
- explain the decline through related business drivers

### Speaker Notes

Spend time here because this is what makes the assignment a GraphRAG architecture.

Say:

"The ontology is not a visualization layer. It is an operational semantic layer. It tells the system what concepts mean, how they relate, and how they map to governed warehouse fields."

Another strong line:

"SQL joins can connect tables, but the ontology explains what the connections mean."

---

## Slide 4 — Example Walkthrough + Defense

### Title
Example: "Why Did APAC Retail Revenue Decline?"

### Slide Content

Query understanding:

- `metric = Revenue`
- `region = APAC`
- `business_unit = Retail`
- `intent = root-cause analysis`

Ontology grounding:

- APAC -> Japan, India, Singapore
- Revenue -> Units Sold, Refunds, Net Revenue
- Profitability -> Net Revenue and Expense

Structured retrieval:

- SQL is generated from approved mappings, not invented freely by the LLM
- Snowflake returns governed metric aggregates
- The context builder sends analytical evidence, not raw rows

Demo result:

- APAC Retail revenue declined from 350,000 to 283,000
- change = -67,000 or -19.1%
- refunds increased by 17,000
- units decreased by 65

### Defense

Why GraphRAG?

> Standard RAG retrieves similar chunks. GraphRAG expands retrieval using explicit relationships and ontology-aware traversal.

Why not just SQL?

> SQL joins connect tables. The ontology encodes business meaning, hierarchy, and metric dependencies.

Main tradeoff:

> The ontology must be maintained, versioned, governed, and kept synchronized with Snowflake.

### Speaker Notes

This slide proves the architecture is concrete and gives you the defense answers.

If presenting the demo, run:

```bash
python demo.py
```

Say:

"The system does not dump raw rows into the LLM. It retrieves semantically meaningful analytical context: metric deltas, hierarchy evidence, and related KPI drivers."

Strong closing line:

"This architecture separates truth from meaning. Snowflake remains the governed source of truth, and the graph provides the semantic layer that makes retrieval business-aware."

End with:

"That is what makes this GraphRAG, not just RAG plus a graph database."
