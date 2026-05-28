from __future__ import annotations

from graph_rag.context_builder import ContextFragment


def rerank_context(
    fragments: list[ContextFragment],
    intent: str,
    limit: int = 8,
) -> list[ContextFragment]:
    intent_bonus = {
        "root_cause": {"metric_change": 0.2, "driver_metric": 0.2, "semantic_evidence": 0.1},
        "comparison": {"regional_metric": 0.2, "metric_change": 0.1},
        "trend": {"metric_change": 0.2, "regional_metric": 0.1},
    }
    bonuses = intent_bonus.get(intent, {})

    return sorted(
        fragments,
        key=lambda fragment: fragment.score + bonuses.get(fragment.kind, 0.0),
        reverse=True,
    )[:limit]
