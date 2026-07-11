"""describe_table agent tool.

Exposes single-table schema inspection to the agent. Wraps
`app.services.schema_inspection.describe_table` behind the BaseTool
interface so the LLM can call it in a uniform, traceable way.
"""

from pydantic import BaseModel, Field

from app.db.engine import SessionLocal
from app.db.exceptions import DatabaseConnectionError, DatabaseQueryError
from app.services.schema_inspection import describe_table
from app.tools.base import BaseTool, ToolError


class DescribeTableInput(BaseModel):
    """The agent must supply the exact table name (from list_tables)."""

    table_name: str = Field(
        ...,
        description="Exact name of the table to describe, as returned by list_tables.",
    )


class ColumnInfo(BaseModel):
    name: str
    type: str
    nullable: bool
    is_primary_key: bool


class ForeignKeyInfo(BaseModel):
    column: str
    references_table: str
    references_column: str


class DescribeTableOutput(BaseModel):
    """Concise schema description: columns, primary keys, and relationships."""

    table: str
    columns: list[ColumnInfo]
    primary_keys: list[str]
    foreign_keys: list[ForeignKeyInfo]


class DescribeTableTool(BaseTool):
    """Agent tool that describes a single table's columns and relationships.

    The agent calls this after list_tables, for each table it plans to
    query, so it knows exact column names, types, and how tables join.
    """

    name = "describe_table"
    description = (
        "Describe one table's columns, types, primary keys, and foreign key "
        "relationships. Call this before writing SQL for a table you have not "
        "already described."
    )
    input_schema = DescribeTableInput
    output_schema = DescribeTableOutput

    def run(self, input_data: DescribeTableInput) -> DescribeTableOutput:
        db = SessionLocal()
        try:
            info = describe_table(db, input_data.table_name)
        except ValueError as exc:
            # Table does not exist — this is a normal, expected agent mistake.
            raise ToolError(self.name, str(exc), exc) from exc
        except (DatabaseConnectionError, DatabaseQueryError) as exc:
            raise ToolError(self.name, f"Database error: {exc}", exc) from exc
        except Exception as exc:  # noqa: BLE001 - normalize any unexpected error
            raise ToolError(self.name, f"Failed to describe table: {exc}", exc) from exc
        finally:
            db.close()

        return DescribeTableOutput(**info)
