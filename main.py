from fastapi import FastAPI

from src.infrastructure.app_config import configure_app

app = FastAPI(
    title="Auth Service",
    description="Serviço de autenticação com suporte a OAuth2",
    version="1.0.0",
)

configure_app(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
