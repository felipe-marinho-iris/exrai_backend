from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from src.core.config import settings
from src.models.schemas import ThemeBase
from loguru import logger


class EmbeddingService:
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Carrega o modelo de embeddings"""
        try:
            self.model = SentenceTransformer(settings.embedding_model)
            logger.info(f"Modelo de embeddings carregado: {settings.embedding_model}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo de embeddings: {e}")
            raise
    
    def create_theme_text(self, theme: ThemeBase) -> str:
        """Cria uma representação textual do tema para embedding"""
        # Combinar informações do tema em um texto único
        keywords = ", ".join(theme.palavras_chave)
        text = f"{theme.tema_geral}. {theme.subtema}. Categoria: {theme.categoria}. Palavras-chave: {keywords}"
        return text
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Gera embeddings para um ou mais textos"""
        if isinstance(texts, str):
            texts = [texts]
        
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            logger.error(f"Erro ao gerar embeddings: {e}")
            raise
    
    def encode_theme(self, theme: ThemeBase) -> List[float]:
        """Gera embedding para um tema"""
        theme_text = self.create_theme_text(theme)
        embedding = self.encode(theme_text)[0]
        return embedding.tolist()
    
    def encode_themes(self, themes: List[ThemeBase]) -> List[List[float]]:
        """Gera embeddings para múltiplos temas"""
        theme_texts = [self.create_theme_text(theme) for theme in themes]
        embeddings = self.encode(theme_texts)
        return [emb.tolist() for emb in embeddings]
    
    def cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calcula a similaridade de cosseno entre dois embeddings"""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Normalizar vetores
        vec1_norm = vec1 / np.linalg.norm(vec1)
        vec2_norm = vec2 / np.linalg.norm(vec2)
        
        # Calcular similaridade
        similarity = np.dot(vec1_norm, vec2_norm)
        return float(similarity)