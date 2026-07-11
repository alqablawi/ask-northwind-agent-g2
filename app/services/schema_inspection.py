"""Schema inspection service for Northwind database.

Reads table names, columns, primary keys, and foreign-key relationships
from PostgreSQL using information_schema — no ORM models required.
Output is compact so it fits into agent context windows.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session


def list_tables(db: Session) -> list[str]:
    """Return all user table names in the public schema, sorted alphabetically.

    System tables (pg_catalog, information_schema) are excluded automatically
    because we filter on table_schema = 'public'.
    """
    result = db.execute(
        text(
            "SELECT table_name "
            "FROM information_schema.tables "
            "WHERE table_schema = 'public' "
            "AND table_type = 'BASE TABLE' "
            "ORDER BY table_name"
        )
    )
    return [row[0] for row in result]


def describe_table(db: Session, table_name: str) -> dict:
    """Return a compact description of one table.

    Returns a dict with:
        - table: table name
        - columns: list of {name, type, nullable, is_primary_key}
        - primary_keys: list of column names
        - foreign_keys: list of {column, references_table, references_column}

    Raises ValueError if the table does not exist in the public schema.
    """
    if not _table_exists(db, table_name):
        raise ValueError(f"Table '{table_name}' does not exist in the public schema.")

    columns = _get_columns(db, table_name)
    primary_keys = _get_primary_keys(db, table_name)
    foreign_keys = _get_foreign_keys(db, table_name)

    for col in columns:
        col["is_primary_key"] = col["name"] in primary_keys

    return {
        "table": table_name,
        "columns": columns,
        "primary_keys": primary_keys,
        "foreign_keys": foreign_keys,
    }


def describe_table_compact(db: Session, table_name: str) -> str:
    """Return a human-readable compact text summary of a table.

    Format:
        Table: customers
        PK: customer_id
        FK: -> orders.customer_id
        Columns:
          - customer_id (varchar, NOT NULL, PK)
          - company_name (varchar, NOT NULL)
          ...
    """
    info = describe_table(db, table_name)
    lines = [f"Table: {info['table']}"]

    if info["primary_keys"]:
        lines.append(f"PK: {', '.join(info['primary_keys'])}")

    for fk in info["foreign_keys"]:
        lines.append(
            f"FK: {fk['column']} -> {fk['references_table']}.{fk['references_column']}"
        )

    lines.append("Columns:")
    for col in info["columns"]:
        parts = [col["name"], f"({col['type']})"]
        if not col["nullable"]:
            parts.append("NOT NULL")
        if col["is_primary_key"]:
            parts.append("PK")
        lines.append(f"  - {' '.join(parts)}")

    return "\n".join(lines)


def list_tables_compact(db: Session) -> str:
    """Return a one-line compact list of all tables."""
    tables = list_tables(db)
    return f"Tables ({len(tables)}): {', '.join(tables)}"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _table_exists(db: Session, table_name: str) -> bool:
    """Check whether a table exists in the public schema."""
    result = db.execute(
        text(
            "SELECT 1 FROM information_schema.tables "
            "WHERE table_schema = 'public' "
            "AND table_type = 'BASE TABLE' "
            "AND table_name = :name"
        ),
        {"name": table_name},
    )
    return result.fetchone() is not None


def _get_columns(db: Session, table_name: str) -> list[dict]:
    """Return all columns with type and nullability for a table."""
    result = db.execute(
        text(
            "SELECT column_name, data_type, is_nullable "
            "FROM information_schema.columns "
            "WHERE table_schema = 'public' "
            "AND table_name = :name "
            "ORDER BY ordinal_position"
        ),
        {"name": table_name},
    )
    columns = []
    for row in result:
        columns.append(
            {
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "YES",
                "is_primary_key": False,
            }
        )
    return columns


def _get_primary_keys(db: Session, table_name: str) -> list[str]:
    """Return the primary-key column names for a table."""
    result = db.execute(
        text(
            "SELECT kcu.column_name "
            "FROM information_schema.table_constraints tc "
            "JOIN information_schema.key_column_usage kcu "
            "  ON tc.constraint_name = kcu.constraint_name "
            "  AND tc.table_schema = kcu.table_schema "
            "WHERE tc.constraint_type = 'PRIMARY KEY' "
            "  AND tc.table_schema = 'public' "
            "  AND tc.table_name = :name "
            "ORDER BY kcu.ordinal_position"
        ),
        {"name": table_name},
    )
    return [row[0] for row in result]


def _get_foreign_keys(db: Session, table_name: str) -> list[dict]:
    """Return foreign-key relationships for a table.

    Each entry: {column, references_table, references_column}
    """
    result = db.execute(
        text(
            """
            SELECT
                kcu.column_name,
                ccu.table_name AS references_table,
                ccu.column_name AS references_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_schema = 'public'
              AND tc.table_name = :name
            ORDER BY kcu.column_name
            """,
        ),
        {"name": table_name},
    )
    fks = []
    for row in result:
        fks.append(
            {
                "column": row[0],
                "references_table": row[1],
                "references_column": row[2],
            }
        )
    return fks
