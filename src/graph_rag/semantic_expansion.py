from __future__ import annotations

from dataclasses import dataclass

from graph_rag.grounding import GroundedQuery
from graph_rag.ontology_store import Concept, OntologyStore


@dataclass(frozen=True)
class SemanticEvidence:
    source: str
    relationship: str
    target: str
    note: str


@dataclass(frozen=True)
class SemanticExpansion:
    expanded_regions: list[Concept]
    related_metrics: list[Concept]
    evidence: list[SemanticEvidence]


REASONING_RELATIONSHIPS = {
    "depends_on",
    "impacts",
    "contributes_to",
    "linked_to",
    "sold_by",
}


def expand_semantics(
    grounded: GroundedQuery,
    ontology: OntologyStore,
) -> SemanticExpansion:
    expanded_regions: list[Concept] = []
    related_metrics: list[Concept] = []
    evidence: list[SemanticEvidence] = []

    if grounded.region:
        children = ontology.children_of(grounded.region.id)
        expanded_regions.extend(children or [grounded.region])
        for child in children:
            evidence.append(
                SemanticEvidence(
                    source=child.label,
                    relationship="rolls_up_to",
                    target=grounded.region.label,
                    note=f"{child.label} is included when querying {grounded.region.label}.",
                )
            )

    for concept in grounded.concepts:
        for relationship, related in ontology.related_concepts(
            concept.id,
            REASONING_RELATIONSHIPS,
        ):
            if related.type in {"Metric", "KPI"} and related.id != concept.id:
                related_metrics.append(related)
            evidence.append(
                SemanticEvidence(
                    source=ontology.get(relationship.source).label,
                    relationship=relationship.type,
                    target=ontology.get(relationship.target).label,
                    note=(
                        f"{ontology.get(relationship.source).label} "
                        f"{relationship.type} {ontology.get(relationship.target).label}."
                    ),
                )
            )

    unique_metrics = {metric.id: metric for metric in related_metrics}
    return SemanticExpansion(
        expanded_regions=expanded_regions,
        related_metrics=list(unique_metrics.values()),
        evidence=evidence,
    )
