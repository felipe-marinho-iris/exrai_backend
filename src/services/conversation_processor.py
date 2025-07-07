from datetime import datetime
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.theme_analyzer import ThemeAnalyzer
from src.services.embeddings import EmbeddingService
from src.services.theme_repository import ThemeRepository
from src.models.schemas import ThemeBase, ThemeResponse, ConversationAnalysisResponse
from loguru import logger
import json


class ConversationProcessor:
    def __init__(self):
        self.theme_analyzer = ThemeAnalyzer()
        self.embedding_service = EmbeddingService()
    
    async def process_conversations(
        self, 
        conversations: List[str], 
        db: AsyncSession
    ) -> ConversationAnalysisResponse:
        """Processa um batch de conversas e retorna análise de temas"""
        
        logger.info(f"Processando {len(conversations)} conversas")
        
        # 1. Analisar conversas e extrair temas
        extracted_themes = await self.theme_analyzer.analyze_conversations(conversations)
        logger.info(f"{len(extracted_themes)} temas extraídos")
        
        # 2. Gerar embeddings para os temas
        embeddings = self.embedding_service.encode_themes(extracted_themes)
        
        # 3. Processar cada tema
        theme_repository = ThemeRepository(db)
        processed_themes = []
        new_themes_count = 0
        existing_themes_updated = 0
        
        for theme, embedding in zip(extracted_themes, embeddings):
            # Buscar tema similar no banco
            similar_result = await theme_repository.find_similar_theme(theme, embedding)
            
            if similar_result:
                # Tema similar encontrado - atualizar relevância
                existing_theme, similarity = similar_result
                logger.info(f"Tema similar encontrado (similaridade: {similarity:.2f}): {existing_theme.tema_geral}")
                
                updated_theme = await theme_repository.update_theme_relevance(existing_theme.id)
                processed_themes.append(self._theme_to_response(updated_theme))
                existing_themes_updated += 1
            else:
                # Novo tema - criar no banco
                new_theme = await theme_repository.create_theme(theme, embedding)
                processed_themes.append(self._theme_to_response(new_theme))
                new_themes_count += 1
        
        # 4. Preparar resposta
        response = ConversationAnalysisResponse(
            themes_identified=processed_themes,
            new_themes_count=new_themes_count,
            existing_themes_updated=existing_themes_updated,
            analysis_timestamp=datetime.utcnow()
        )
        
        logger.info(f"Análise concluída: {new_themes_count} novos temas, {existing_themes_updated} atualizados")
        return response
    
    def _theme_to_response(self, theme_db: any) -> ThemeResponse:
        """Converte tema do banco para schema de resposta"""
        # Parsear palavras-chave do JSON
        palavras_chave = json.loads(theme_db.palavras_chave) if isinstance(theme_db.palavras_chave, str) else theme_db.palavras_chave
        
        return ThemeResponse(
            id=theme_db.id,
            tema_geral=theme_db.tema_geral,
            subtema=theme_db.subtema,
            categoria=theme_db.categoria,
            palavras_chave=palavras_chave,
            relevancia=theme_db.relevancia,
            occurrence_count=theme_db.occurrence_count,
            created_at=theme_db.created_at,
            updated_at=theme_db.updated_at
        )