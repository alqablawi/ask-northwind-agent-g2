from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import get_settings
from app.db.exceptions import DatabaseConnectionError, DatabaseQueryError

settings = get_settings()

engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=settings.debug,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session]:
    """FastAPI dependency that yields a database session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> None:
    """Verify that PostgreSQL is reachable; raise on failure.

    Raises:
        DatabaseConnectionError: if the server is unreachable.
        DatabaseQueryError: if the connection opens but a simple query fails.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as exc:
        raise DatabaseConnectionError(
            f"Cannot connect to PostgreSQL at {settings.database_url.split('@')[-1]}"
        ) from exc
    except SQLAlchemyError as exc:
        raise DatabaseQueryError(f"Unexpected database error: {exc}") from exc
