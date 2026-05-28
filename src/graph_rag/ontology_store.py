from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import networkx as nx
except ImportError:  # pragma: no cover - keeps the demo runnable without installs.
    nx = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Concept:
    id: str
    label: str
    type: str
    aliases: list[str]
    maps_to: dict[str, Any] | None = None
    formula: str | None = None


@dataclass(frozen=True)
class Relationship:
    source: str
    target: str
    type: str


class OntologyStore:
    """Ontology graph abstraction.

    The local implementation uses NetworkX when available and a simple in-memory
    list otherwise. A production adapter would translate these methods to Cypher
    over Neo4j.
    """

    def __init__(self, ontology_path: Path | None = None) -> None:
        path = ontology_path or PROJECT_ROOT / "ontology" / "ontology.yaml"
        payload = json.loads(path.read_text(encoding="utf-8"))

        self.concepts = {
            item["id"]: Concept(
                id=item["id"],
                label=item["label"],
                type=item["type"],
                aliases=item.get("aliases", []),
                maps_to=item.get("maps_to"),
                formula=item.get("formula"),
            )
            for item in payload["concepts"]
        }
        self.relationships = [
            Relationship(
                source=item["source"],
                target=item["target"],
                type=item["type"],
            )
            for item in payload["relationships"]
        ]
        self.alias_index = self._build_alias_index()
        self.graph = self._build_graph()

    def _build_alias_index(self) -> dict[str, str]:
        index: dict[str, str] = {}
        for concept in self.concepts.values():
            index[concept.label.lower()] = concept.id
            for alias in concept.aliases:
                index[alias.lower()] = concept.id
        return index

    def _build_graph(self) -> Any:
        if nx is None:
            return None

        graph = nx.MultiDiGraph()
        for concept in self.concepts.values():
            graph.add_node(concept.id, concept=concept)
        for relationship in self.relationships:
            graph.add_edge(
                relationship.source,
                relationship.target,
                relationship=relationship,
                type=relationship.type,
            )
        return graph

    def get(self, concept_id: str) -> Concept:
        return self.concepts[concept_id]

    def resolve_mention(self, mention: str) -> Concept | None:
        return self.concepts.get(self.alias_index.get(mention.lower()))

    def resolve_text(self, text: str) -> list[Concept]:
        text_lower = f" {text.lower()} "
        matches: list[Concept] = []
        seen: set[str] = set()

        # Longest aliases first prevents "sales" from hiding "product sales".
        for alias, concept_id in sorted(
            self.alias_index.items(), key=lambda item: len(item[0]), reverse=True
        ):
            if f" {alias} " in text_lower and concept_id not in seen:
                matches.append(self.concepts[concept_id])
                seen.add(concept_id)
        return matches

    def relationships_for(
        self,
        concept_id: str,
        relationship_type: str | None = None,
    ) -> list[Relationship]:
        return [
            relationship
            for relationship in self.relationships
            if relationship.source == concept_id
            and (relationship_type is None or relationship.type == relationship_type)
        ]

    def incoming_relationships_for(
        self,
        concept_id: str,
        relationship_type: str | None = None,
    ) -> list[Relationship]:
        return [
            relationship
            for relationship in self.relationships
            if relationship.target == concept_id
            and (relationship_type is None or relationship.type == relationship_type)
        ]

    def children_of(self, concept_id: str) -> list[Concept]:
        return [
            self.concepts[relationship.source]
            for relationship in self.incoming_relationships_for(concept_id, "rolls_up_to")
        ]

    def related_concepts(
        self,
        concept_id: str,
        relationship_types: set[str] | None = None,
    ) -> list[tuple[Relationship, Concept]]:
        matches: list[tuple[Relationship, Concept]] = []
        for relationship in self.relationships:
            if relationship_types and relationship.type not in relationship_types:
                continue
            if relationship.source == concept_id:
                matches.append((relationship, self.concepts[relationship.target]))
            elif relationship.target == concept_id:
                matches.append((relationship, self.concepts[relationship.source]))
        return matches
