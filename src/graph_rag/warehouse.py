from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class QueryResult:
    sql: str
    rows: list[dict[str, Any]]


class Warehouse:
    """Small SQLite stand-in for Snowflake.

    A real Snowflake implementation would keep this public interface and swap
    the connection/query execution internals.
    """

    def __init__(self, db_path: str | None = None) -> None:
        self.connection = sqlite3.connect(db_path or ":memory:")
        self.connection.row_factory = sqlite3.Row

    def initialize(
        self,
        schema_path: Path | None = None,
        seed_path: Path | None = None,
    ) -> None:
        schema = schema_path or PROJECT_ROOT / "data" / "schema.sql"
        seed = seed_path or PROJECT_ROOT / "data" / "seed.sql"
        self.connection.executescript(schema.read_text(encoding="utf-8"))
        self.connection.executescript(seed.read_text(encoding="utf-8"))
        self.connection.commit()

    def query(self, sql: str, params: tuple[Any, ...] = ()) -> QueryResult:
        cursor = self.connection.execute(sql, params)
        rows = [dict(row) for row in cursor.fetchall()]
        return QueryResult(sql=sql, rows=rows)

    def close(self) -> None:
        self.connection.close()
