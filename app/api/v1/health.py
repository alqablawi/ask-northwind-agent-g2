from fastapi import APIRouter, Request

router = APIRouter()



@router.get("/health")
def health_check(request: Request) -> dict[str, str]:
    settings = request.app.state.settings
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.app_env,
    }