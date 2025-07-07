from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router as theme_router
from src.core.config import settings
from loguru import logger

# Configurar logging
logger.add("logs/app.log", rotation="500 MB", level="INFO")

# Criar aplicação
app = FastAPI(
    title=settings.app_name,
    description="Sistema de análise de temas em conversas com busca semântica",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(theme_router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    return {
        "message": "Exrai Theme Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )