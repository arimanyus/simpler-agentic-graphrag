from __future__ import annotations

from dataclasses import dataclass

from graph_rag.ontology_store import Concept, OntologyStore


@dataclass(frozen=True)
class QueryUnderstanding:
    query: str
    intent: str
    mentions: list[Concept]

    @property
    def by_type(self) -> dict[str, list[Concept]]:
        grouped: dict[str, list[Concept]] = {}
        for concept in self.mentions:
            grouped.setdefault(concept.type, []).append(concept)
        return grouped


def detect_intent(query: str) -> str:
    normalized = query.lower()
    if "why" in normalized or "decline" in normalized or "drop" in normalized:
        return "root_cause"
    if "compare" in normalized or "versus" in normalized or "vs" in normalized:
        return "comparison"
    if "trend" in normalized or "over time" in normalized:
        return "trend"
    return "metric_lookup"


def understand_query(query: str, ontology: OntologyStore) -> QueryUnderstanding:
    return QueryUnderstanding(
        query=query,
        intent=detect_intent(query),
        mentions=ontology.resolve_text(query),
    )
