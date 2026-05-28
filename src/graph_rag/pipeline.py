from __future__ import annotations

from dataclasses import dataclass

from graph_rag.context_builder import ContextFragment, build_context
from graph_rag.grounding import GroundedQuery, ground_query
from graph_rag.ontology_store import OntologyStore
from graph_rag.query_understanding import QueryUnderstanding, understand_query
from graph_rag.reranker import rerank_context
from graph_rag.semantic_expansion import SemanticExpansion, expand_semantics
from graph_rag.synthesis import synthesize_response
from graph_rag.text2sql import SqlRequest, build_governed_sql
from graph_rag.warehouse import QueryResult, Warehouse


@dataclass(frozen=True)
class PipelineTrace:
    understanding: QueryUnderstanding
    grounded: GroundedQuery
    expansion: SemanticExpansion
    sql_request: SqlRequest
    sql_result: QueryResult
    context: list[ContextFragment]
    ranked_context: list[ContextFragment]
    answer: str


class GraphRAGPipeline:
    """LangGraph-shaped orchestration with a deterministic local runner.

    Production orchestration would wire these same nodes in LangGraph:
    understand -> ground -> (expand and retrieve) -> assemble -> rerank -> synthesize.
    """

    def __init__(
        self,
        ontology: OntologyStore | None = None,
        warehouse: Warehouse | None = None,
    ) -> None:
        self.ontology = ontology or OntologyStore()
        self.warehouse = warehouse or Warehouse()
        self.warehouse.initialize()

    def run(self, query: str) -> PipelineTrace:
        understanding = understand_query(query, self.ontology)
        grounded = ground_query(understanding, self.ontology)

        # In LangGraph these are natural parallel branches after grounding.
        expansion = expand_semantics(grounded, self.ontology)
        sql_request = build_governed_sql(grounded)
        sql_result = self.warehouse.query(sql_request.sql, sql_request.params)

        context = build_context(grounded, expansion, sql_result)
        ranked_context = rerank_context(context, grounded.intent)
        answer = synthesize_response(grounded, ranked_context)

        return PipelineTrace(
            understanding=understanding,
            grounded=grounded,
            expansion=expansion,
            sql_request=sql_request,
            sql_result=sql_result,
            context=context,
            ranked_context=ranked_context,
            answer=answer,
        )
