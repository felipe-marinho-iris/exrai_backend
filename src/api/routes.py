from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.core.database import get_db
from src.services.conversation_processor import ConversationProcessor
from src.services.theme_repository import ThemeRepository
from src.models.schemas import (
    ConversationAnalysisRequest,
    ConversationAnalysisResponse,
    ThemeResponse
)
from loguru import logger

router = APIRouter(prefix="/themes", tags=["themes"])


@router.post("/analyze", response_model=ConversationAnalysisResponse)
async def analyze_conversations(
    request: ConversationAnalysisRequest,
    db: AsyncSession = Depends(get_db)
):
    """Analisa conversas e identifica temas relevantes"""
    try:
        processor = ConversationProcessor()
        result = await processor.process_conversations(
            request.conversations,
            db
        )
        return result
    except Exception as e:
        logger.error(f"Erro ao analisar conversas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ThemeResponse])
async def get_all_themes(
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Retorna todos os temas ordenados por relevância"""
    try:
        repository = ThemeRepository(db)
        themes = await repository.get_all_themes(limit=limit)
        
        # Converter para schema de resposta
        response_themes = []
        for theme in themes:
            import json
            palavras_chave = json.loads(theme.palavras_chave) if isinstance(theme.palavras_chave, str) else theme.palavras_chave
            
            response_themes.append(ThemeResponse(
                id=theme.id,
                tema_geral=theme.tema_geral,
                subtema=theme.subtema,
                categoria=theme.categoria,
                palavras_chave=palavras_chave,
                relevancia=theme.relevancia,
                occurrence_count=theme.occurrence_count,
                created_at=theme.created_at,
                updated_at=theme.updated_at
            ))
        
        return response_themes
    except Exception as e:
        logger.error(f"Erro ao buscar temas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_theme_statistics(db: AsyncSession = Depends(get_db)):
    """Retorna estatísticas sobre os temas"""
    try:
        repository = ThemeRepository(db)
        themes = await repository.get_all_themes()
        
        # Calcular estatísticas
        total_themes = len(themes)
        total_occurrences = sum(theme.occurrence_count for theme in themes)
        avg_relevance = sum(theme.relevancia for theme in themes) / total_themes if total_themes > 0 else 0
        
        # Categorias mais comuns
        category_counts = {}
        for theme in themes:
            category = theme.categoria.value if hasattr(theme.categoria, 'value') else theme.categoria
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "total_themes": total_themes,
            "total_occurrences": total_occurrences,
            "average_relevance": round(avg_relevance, 2),
            "categories": category_counts,
            "top_themes": [
                {
                    "tema_geral": theme.tema_geral,
                    "subtema": theme.subtema,
                    "relevancia": theme.relevancia,
                    "occurrences": theme.occurrence_count
                }
                for theme in themes[:10]  # Top 10 temas
            ]
        }
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))