from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from graph_rag.pipeline import GraphRAGPipeline  # noqa: E402


def print_section(title: str, body: str) -> None:
    print(f"\n{'=' * 80}")
    print(title)
    print("=" * 80)
    print(body)


def main() -> None:
    query = "Why did APAC retail revenue decline?"
    pipeline = GraphRAGPipeline()
    trace = pipeline.run(query)

    print_section("User Query", query)
    print_section(
        "1. Query Understanding",
        "\n".join(
            [
                f"intent: {trace.understanding.intent}",
                "mentions: "
                + ", ".join(
                    f"{concept.label} ({concept.type})"
                    for concept in trace.understanding.mentions
                ),
            ]
        ),
    )
    print_section(
        "2. Ontology Grounding",
        "\n".join(
            [
                f"metric: {trace.grounded.metric.label if trace.grounded.metric else 'unknown'}",
                f"region: {trace.grounded.region.label if trace.grounded.region else 'unknown'}",
                (
                    "business_unit: "
                    f"{trace.grounded.business_unit.label if trace.grounded.business_unit else 'unknown'}"
                ),
            ]
        ),
    )
    print_section(
        "3. Semantic Expansion",
        "\n".join(
            [
                "expanded_regions: "
                + ", ".join(region.label for region in trace.expansion.expanded_regions),
                "related_metrics: "
                + ", ".join(metric.label for metric in trace.expansion.related_metrics),
                "evidence: "
                + " | ".join(item.note for item in trace.expansion.evidence[:5]),
            ]
        ),
    )
    print_section(
        "4. Governed SQL",
        trace.sql_request.sql.strip() + f"\nparams: {trace.sql_request.params}",
    )
    print_section(
        "5. Structured Retrieval",
        "\n".join(str(row) for row in trace.sql_result.rows),
    )
    print_section(
        "6. Ranked Context",
        "\n".join(
            f"[{item.kind}] {item.title}: {item.content}"
            for item in trace.ranked_context
        ),
    )
    print_section("7. Grounded Response", trace.answer)


if __name__ == "__main__":
    main()
