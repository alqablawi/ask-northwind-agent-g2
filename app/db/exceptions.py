class DatabaseError(Exception):
    """Base error for all database-related failures."""


class DatabaseConnectionError(DatabaseError):
    """Raised when the application cannot reach PostgreSQL."""


class DatabaseQueryError(DatabaseError):
    """Raised when a query fails for a reason other than connectivity."""
