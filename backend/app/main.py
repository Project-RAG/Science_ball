"""R&D Knowledge Map — FastAPI application."""

from fastapi import FastAPI

from app.api.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="R&D Knowledge Map",
        description="Search, analysis and knowledge mapping for mining and metallurgy research.",
        version="0.1.0",
    )
    app.include_router(api_router)
    return app


app = create_app()
