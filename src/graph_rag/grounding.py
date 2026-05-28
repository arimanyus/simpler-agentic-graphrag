from __future__ import annotations

from dataclasses import dataclass

from graph_rag.ontology_store import Concept, OntologyStore
from graph_rag.query_understanding import QueryUnderstanding


@dataclass(frozen=True)
class GroundedQuery:
    query: str
    intent: str
    concepts: list[Concept]
    region: Concept | None
    business_unit: Concept | None
    metric: Concept | None


def _first_of_type(concepts: list[Concept], concept_type: str) -> Concept | None:
    return next((concept for concept in concepts if concept.type == concept_type), None)


def ground_query(
    understanding: QueryUnderstanding,
    ontology: OntologyStore,
) -> GroundedQuery:
    concepts = list(understanding.mentions)

    # Defaults make the demo robust while keeping the mapping explicit.
    if not _first_of_type(concepts, "Metric"):
        concepts.append(ontology.get("metric_revenue"))
    if not _first_of_type(concepts, "Region"):
        concepts.append(ontology.get("region_apac"))
    if not _first_of_type(concepts, "BusinessUnit"):
        concepts.append(ontology.get("bu_retail"))

    return GroundedQuery(
        query=understanding.query,
        intent=understanding.intent,
        concepts=concepts,
        region=_first_of_type(concepts, "Region"),
        business_unit=_first_of_type(concepts, "BusinessUnit"),
        metric=_first_of_type(concepts, "Metric"),
    )
