from fastapi import FastAPI
from app.core.settings import get_settings
from app.api.v1.router import api_router

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)
app.state.settings = settings


app.include_router(api_router)