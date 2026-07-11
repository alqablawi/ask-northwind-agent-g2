"""list_tables agent tool.

Exposes database table discovery to the agent. Wraps
`app.services.schema_inspection.list_tables` behind the BaseTool
interface so the LLM can call it in a uniform, traceable way.
"""

from pydantic import BaseModel

from app.db.engine import SessionLocal
from app.db.exceptions import DatabaseConnectionError, DatabaseQueryError
from app.services.schema_inspection import list_tables
from app.tools.base import BaseTool, ToolError


class ListTablesInput(BaseModel):
    """No parameters needed — this tool always lists every business table."""


class ListTablesOutput(BaseModel):
    """Concise output: just the table names and how many there are."""

    tables: list[str]
    count: int


class ListTablesTool(BaseTool):
    """Agent tool that lists Northwind business tables.

    The agent calls this first, before describe_table or run_sql_query,
    to discover what data is available.
    """

    name = "list_tables"
    description = (
        "List all business tables available in the Northwind database. "
        "Call this first when you don't know which tables exist."
    )
    input_schema = ListTablesInput
    output_schema = ListTablesOutput

    def run(self, input_data: ListTablesInput) -> ListTablesOutput:
        db = SessionLocal()
        try:
            tables = list_tables(db)
        except (DatabaseConnectionError, DatabaseQueryError) as exc:
            raise ToolError(self.name, f"Database error: {exc}", exc) from exc
        except Exception as exc:  # noqa: BLE001 - normalize any unexpected error
            raise ToolError(self.name, f"Failed to list tables: {exc}", exc) from exc
        finally:
            db.close()

        return ListTablesOutput(tables=tables, count=len(tables))
