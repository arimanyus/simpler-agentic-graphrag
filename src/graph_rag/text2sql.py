from __future__ import annotations

from dataclasses import dataclass

from graph_rag.grounding import GroundedQuery


@dataclass(frozen=True)
class SqlRequest:
    sql: str
    params: tuple[str, ...]


def _period_expression() -> str:
    return """
        CASE
            WHEN CAST(strftime('%m', fs.date) AS INTEGER) BETWEEN 1 AND 3 THEN strftime('%Y', fs.date) || '-Q1'
            WHEN CAST(strftime('%m', fs.date) AS INTEGER) BETWEEN 4 AND 6 THEN strftime('%Y', fs.date) || '-Q2'
            WHEN CAST(strftime('%m', fs.date) AS INTEGER) BETWEEN 7 AND 9 THEN strftime('%Y', fs.date) || '-Q3'
            ELSE strftime('%Y', fs.date) || '-Q4'
        END
    """


def build_governed_sql(grounded: GroundedQuery) -> SqlRequest:
    """Build SQL from grounded ontology concepts, not free-form LLM text."""

    where_clauses: list[str] = []
    params: list[str] = []

    if grounded.region and grounded.region.maps_to:
        mapping = grounded.region.maps_to
        if mapping["column"] == "parent_region":
            where_clauses.append("r.parent_region = ?")
        else:
            where_clauses.append("r.region_name = ?")
        params.append(mapping["value"])

    if grounded.business_unit and grounded.business_unit.maps_to:
        where_clauses.append("bu.name = ?")
        params.append(grounded.business_unit.maps_to["value"])

    period = _period_expression()
    where_sql = " AND ".join(where_clauses) if where_clauses else "1 = 1"

    sql = f"""
        SELECT
            r.region_name,
            r.parent_region,
            bu.name AS business_unit,
            {period} AS period,
            SUM(fs.revenue) AS revenue,
            SUM(fs.refunds) AS refunds,
            SUM(fs.expense) AS expense,
            SUM(fs.units) AS units,
            SUM(fs.revenue - fs.refunds) AS net_revenue,
            SUM(fs.revenue - fs.refunds - fs.expense) AS profitability
        FROM fact_sales fs
        JOIN dim_region r ON r.region_id = fs.region_id
        JOIN dim_business_unit bu ON bu.business_unit_id = fs.business_unit_id
        WHERE {where_sql}
        GROUP BY r.region_name, r.parent_region, bu.name, period
        ORDER BY r.region_name, period
    """

    return SqlRequest(sql=sql, params=tuple(params))
