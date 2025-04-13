from fastapi import FastAPI

from src.infrastructure.middleware.cors import configure_cors
from src.presentation.routes import auth_routes


def configure_app(app: FastAPI) -> None:
    """Configura a aplicação FastAPI com todas as dependências necessárias."""
    # Configura CORS
    configure_cors(app)

    # Configura rotas
    app.include_router(auth_routes.router, prefix="/api/v1", tags=["auth"])
