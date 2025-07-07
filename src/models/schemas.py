from datetime import datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ThemeCategory(str, Enum):
    PROFESSIONAL = "profissional"
    SOCIAL = "social"
    INFORMATIVE = "informativo"
    EMOTIONAL = "emocional"
    TECHNICAL = "técnico"
    EDUCATIONAL = "educacional"
    ENTERTAINMENT = "entretenimento"
    HEALTH = "saúde"
    FINANCIAL = "financeiro"
    OTHER = "outro"


class ThemeBase(BaseModel):
    tema_geral: str = Field(..., description="Tema geral identificado")
    subtema: str = Field(..., description="Subtema específico")
    categoria: ThemeCategory = Field(..., description="Categoria do tema")
    palavras_chave: List[str] = Field(..., description="Palavras-chave relacionadas")


class ThemeCreate(ThemeBase):
    pass


class ThemeInDB(ThemeBase):
    id: int
    relevancia: float = Field(default=1.0, description="Score de relevância do tema")
    embedding: Optional[List[float]] = Field(None, description="Vetor de embedding do tema")
    created_at: datetime
    updated_at: datetime
    occurrence_count: int = Field(default=1, description="Número de ocorrências do tema")

    class Config:
        from_attributes = True


class ThemeResponse(ThemeBase):
    id: int
    relevancia: float
    occurrence_count: int
    created_at: datetime
    updated_at: datetime


class ConversationAnalysisRequest(BaseModel):
    conversations: List[str] = Field(..., description="Lista de conversas para análise")
    period_hours: int = Field(default=24, description="Período de análise em horas")


class ConversationAnalysisResponse(BaseModel):
    themes_identified: List[ThemeResponse]
    new_themes_count: int
    existing_themes_updated: int
    analysis_timestamp: datetime