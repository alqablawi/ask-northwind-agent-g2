import time
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, ValidationError, Field

class ToolResult(BaseModel):
    """Uniform result returned by every tool execution.

    Attributes:
        tool_name: Name of the tool that ran.
        success: Whether execution succeeded.
        output: The tool's output (matches the tool's output_schema) when successful.
        error: A human-readable error message when success is False.
        duration_ms: How long the tool took to execute, in milliseconds.
    """
    tool_name: str 
    success: bool
    output: dict[str, Any] | None = None
    error: str | None = None
    duration_ms: float

class BaseTool(ABC):
    """Abstract base class that every agent tool must implement.

    Subclasses must define:
        name: A short, unique, machine-readable tool name (e.g. "list_tables").
        description: A natural-language description the LLM uses to decide
            when to call this tool.
        input_schema: A Pydantic model describing the tool's expected input.
        output_schema: A Pydantic model describing the tool's output shape.

    Subclasses must implement `run(self, input_data)` with the tool's
    actual logic. Do NOT override `execute` — it handles validation,
    timing, and error normalization for you.
    """

    name: str
    description: str
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]

    @abstractmethod
    def run(self, input_data: BaseModel) -> BaseModel:
        """Execute the tool's core logic. Must return an output_schema instance."""
        raise NotImplementedError

    def execute(self, raw_input: dict[str, Any]) -> ToolResult:
        """Validate input, run the tool, time it, and normalize any errors.

        This is the single entry point the agent should call. It never
        raises — failures are captured inside the returned ToolResult so
        the agent loop can inspect `result.success` and recover.
        """
        start = time.perf_counter()

        try:
            validated_input = self.input_schema.model_validate(raw_input)
        except ValidationError as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return ToolResult(
                tool_name=self.name,
                success=False,
                error=f"Invalid input: {exc}",
                duration_ms=round(duration_ms, 2),
            )

        try:
            output = self.run(validated_input)
        except ToolError as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return ToolResult(
                tool_name=self.name,
                success=False,
                error=exc.message,
                duration_ms=round(duration_ms, 2),
            )
        except Exception as exc:  # noqa: BLE001 - normalize any unexpected error
            duration_ms = (time.perf_counter() - start) * 1000
            return ToolResult(
                tool_name=self.name,
                success=False,
                error=f"Unexpected error: {exc}",
                duration_ms=round(duration_ms, 2),
            )

        duration_ms = (time.perf_counter() - start) * 1000
        return ToolResult(
            tool_name=self.name,
            success=True,
            output=output.model_dump(),
            duration_ms=round(duration_ms, 2),
        )

    def spec(self) -> dict[str, Any]:
        """Return a compact description of this tool for the LLM's tool list."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema.model_json_schema(),
        }

class ToolError(Exception):
    """Normalized error raised when a tool fails to execute.

    Wraps the original exception so the caller always deals with the
    same error type, regardless of which tool or library raised it.
    """

    def __init__(self, tool_name: str, message: str, original: Exception | None = None):
        self.tool_name = tool_name
        self.message = message
        self.original = original
        super().__init__(f"[{tool_name}] {message}")