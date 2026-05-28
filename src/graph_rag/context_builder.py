from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from graph_rag.grounding import GroundedQuery
from graph_rag.semantic_expansion import SemanticExpansion
from graph_rag.warehouse import QueryResult


@dataclass(frozen=True)
class ContextFragment:
    kind: str
    title: str
    content: str
    score: float


def _sum_by_period(rows: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    totals: dict[str, dict[str, float]] = {}
    for row in rows:
        period = row["period"]
        bucket = totals.setdefault(
            period,
            {
                "revenue": 0.0,
                "refunds": 0.0,
                "expense": 0.0,
                "units": 0.0,
                "net_revenue": 0.0,
                "profitability": 0.0,
            },
        )
        for metric in bucket:
            bucket[metric] += float(row[metric])
    return totals


def _change(new_value: float, old_value: float) -> float:
    if old_value == 0:
        return 0.0
    return (new_value - old_value) / old_value * 100


def build_context(
    grounded: GroundedQuery,
    expansion: SemanticExpansion,
    result: QueryResult,
) -> list[ContextFragment]:
    rows = result.rows
    totals = _sum_by_period(rows)
    periods = sorted(totals)
    fragments: list[ContextFragment] = []

    if len(periods) >= 2:
        previous_period, current_period = periods[0], periods[-1]
        previous = totals[previous_period]
        current = totals[current_period]
        revenue_delta = current["revenue"] - previous["revenue"]
        refund_delta = current["refunds"] - previous["refunds"]
        units_delta = current["units"] - previous["units"]

        fragments.append(
            ContextFragment(
                kind="metric_change",
                title="APAC Retail revenue changed by period",
                content=(
                    f"{previous_period} revenue was {previous['revenue']:,.0f}; "
                    f"{current_period} revenue was {current['revenue']:,.0f}; "
                    f"change was {revenue_delta:,.0f} "
                    f"({_change(current['revenue'], previous['revenue']):.1f}%)."
                ),
                score=0.95,
            )
        )
        fragments.append(
            ContextFragment(
                kind="driver_metric",
                title="Refunds and units moved against revenue",
                content=(
                    f"Refunds changed by {refund_delta:,.0f} and units changed by "
                    f"{units_delta:,.0f} from {previous_period} to {current_period}."
                ),
                score=0.9,
            )
        )

    for row in rows:
        fragments.append(
            ContextFragment(
                kind="regional_metric",
                title=f"{row['region_name']} {row['period']} metrics",
                content=(
                    f"{row['region_name']} {row['business_unit']} in {row['period']}: "
                    f"revenue={row['revenue']:,.0f}, refunds={row['refunds']:,.0f}, "
                    f"expense={row['expense']:,.0f}, units={row['units']:,.0f}."
                ),
                score=0.7,
            )
        )

    for evidence in expansion.evidence:
        fragments.append(
            ContextFragment(
                kind="semantic_evidence",
                title=f"{evidence.source} {evidence.relationship} {evidence.target}",
                content=evidence.note,
                score=0.65,
            )
        )

    fragments.append(
        ContextFragment(
            kind="grounding",
            title="Grounded query",
            content=(
                f"Intent={grounded.intent}; "
                f"metric={grounded.metric.label if grounded.metric else 'unknown'}; "
                f"region={grounded.region.label if grounded.region else 'unknown'}; "
                f"business_unit={grounded.business_unit.label if grounded.business_unit else 'unknown'}."
            ),
            score=0.8,
        )
    )
    return fragments
