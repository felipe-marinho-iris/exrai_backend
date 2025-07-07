import json
from typing import List, Optional, Tuple
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.database import Theme
from src.models.schemas import ThemeBase, ThemeCreate
from src.services.embeddings import EmbeddingService
from src.core.config import settings
from loguru import logger


class ThemeRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.embedding_service = EmbeddingService()
    
    async def find_similar_theme(self, theme: ThemeBase, embedding: List[float]) -> Optional[Tuple[Theme, float]]:
        """Busca tema similar usando busca vetorial"""
        try:
            # Query usando pgvector para busca por similaridade
            query = text("""
                SELECT id, tema_geral, subtema, categoria, palavras_chave, relevancia, 
                       occurrence_count, created_at, updated_at,
                       1 - (embedding <=> :embedding::vector) as similarity
                FROM themes
                WHERE 1 - (embedding <=> :embedding::vector) > :threshold
                ORDER BY similarity DESC
                LIMIT 1
            """)
            
            result = await self.db.execute(
                query,
                {
                    "embedding": embedding,
                    "threshold": settings.similarity_threshold
                }
            )
            
            row = result.first()
            if row:
                # Criar objeto Theme manualmente
                theme_dict = {
                    "id": row.id,
                    "tema_geral": row.tema_geral,
                    "subtema": row.subtema,
                    "categoria": row.categoria,
                    "palavras_chave": row.palavras_chave,
                    "relevancia": row.relevancia,
                    "occurrence_count": row.occurrence_count,
                    "created_at": row.created_at,
                    "updated_at": row.updated_at
                }
                
                existing_theme = Theme(**theme_dict)
                similarity = row.similarity
                
                return existing_theme, similarity
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar tema similar: {e}")
            raise
    
    async def create_theme(self, theme: ThemeBase, embedding: List[float]) -> Theme:
        """Cria um novo tema no banco de dados"""
        try:
            # Converter palavras-chave para JSON string
            palavras_chave_json = json.dumps(theme.palavras_chave, ensure_ascii=False)
            
            new_theme = Theme(
                tema_geral=theme.tema_geral,
                subtema=theme.subtema,
                categoria=theme.categoria.value,
                palavras_chave=palavras_chave_json,
                relevancia=1.0,
                occurrence_count=1,
                embedding=embedding
            )
            
            self.db.add(new_theme)
            await self.db.commit()
            await self.db.refresh(new_theme)
            
            logger.info(f"Novo tema criado: {new_theme.tema_geral} - {new_theme.subtema}")
            return new_theme
            
        except Exception as e:
            logger.error(f"Erro ao criar tema: {e}")
            await self.db.rollback()
            raise
    
    async def update_theme_relevance(self, theme_id: int, increment: float = None) -> Theme:
        """Atualiza a relevância de um tema existente"""
        try:
            if increment is None:
                increment = settings.relevance_increment
            
            # Buscar tema
            result = await self.db.execute(
                select(Theme).where(Theme.id == theme_id)
            )
            theme = result.scalar_one_or_none()
            
            if not theme:
                raise ValueError(f"Tema com ID {theme_id} não encontrado")
            
            # Atualizar relevância e contador
            theme.relevancia += increment
            theme.occurrence_count += 1
            
            await self.db.commit()
            await self.db.refresh(theme)
            
            logger.info(f"Relevância atualizada para tema {theme.id}: {theme.relevancia}")
            return theme
            
        except Exception as e:
            logger.error(f"Erro ao atualizar relevância: {e}")
            await self.db.rollback()
            raise
    
    async def get_all_themes(self, limit: int = 100) -> List[Theme]:
        """Retorna todos os temas ordenados por relevância"""
        try:
            result = await self.db.execute(
                select(Theme)
                .order_by(Theme.relevancia.desc())
                .limit(limit)
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Erro ao buscar temas: {e}")
            raise