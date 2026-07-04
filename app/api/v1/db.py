"""Database smoke endpoint.

GET /api/v1/db/smoke — verifies the API can query Northwind.
Returns table count and sample product count.
Does NOT require LLM or Redis — only PostgreSQL.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.engine import get_db
from app.db.exceptions import DatabaseConnectionError

router = APIRouter(prefix="/db", tags=["database"])

@router.get("/smoke")
def db_smoke(
    request: Request,
    db: Session = Depends(get_db),  # noqa: B008
) -> JSONResponse:
    """Run a simple read-only query against Northwind.

    Returns 200 with table_count and product_count on success.
    Returns 503 with an error message if the database is unreachable.
    """
    settings = request.app.state.settings

    try:
        table_count = db.execute(
            text(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'"
            )
        ).scalar()

        product_count = db.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar()

        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "database": settings.postgres_db,
                "table_count": table_count,
                "product_count": product_count,
            },
        )

    except DatabaseConnectionError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "detail": f"Database unavailable: {exc}",
            },
        )
    except SQLAlchemyError as exc:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "detail": f"Database query failed: {exc}",
            },
        )
