from __future__ import annotations

from graph_rag.context_builder import ContextFragment
from graph_rag.grounding import GroundedQuery
from graph_rag.llm import DeterministicFinancialAnalyst


def synthesize_response(
    grounded: GroundedQuery,
    ranked_context: list[ContextFragment],
) -> str:
    analyst = DeterministicFinancialAnalyst()
    return analyst.synthesize(grounded, ranked_context)
