from __future__ import annotations

from graph_rag.context_builder import ContextFragment
from graph_rag.grounding import GroundedQuery


class DeterministicFinancialAnalyst:
    """Offline LLM stand-in for demos and rehearsals."""

    def synthesize(
        self,
        grounded: GroundedQuery,
        context: list[ContextFragment],
    ) -> str:
        metric_change = next(
            (fragment for fragment in context if fragment.kind == "metric_change"),
            None,
        )
        driver_metric = next(
            (fragment for fragment in context if fragment.kind == "driver_metric"),
            None,
        )
        semantic = [
            fragment.content
            for fragment in context
            if fragment.kind == "semantic_evidence"
        ][:3]

        lines = [
            f"Grounded answer for: {grounded.query}",
            "",
            "APAC Retail revenue declined because the underlying governed metrics moved in the wrong direction.",
        ]

        if metric_change:
            lines.append(f"- Revenue evidence: {metric_change.content}")
        if driver_metric:
            lines.append(f"- Driver evidence: {driver_metric.content}")
        if semantic:
            lines.append(
                "- Ontology evidence: "
                + " ".join(semantic)
            )

        lines.append(
            "The graph improves the answer by expanding APAC into its child regions and by linking Revenue to dependent metrics such as Units Sold, Refunds, and Net Revenue before SQL retrieval."
        )
        return "\n".join(lines)
