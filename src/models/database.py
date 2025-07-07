from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
import enum

Base = declarative_base()


class ThemeCategoryEnum(str, enum.Enum):
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


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, index=True)
    tema_geral = Column(String(255), nullable=False)
    subtema = Column(String(255), nullable=False)
    categoria = Column(SQLAEnum(ThemeCategoryEnum), nullable=False)
    palavras_chave = Column(Text, nullable=False)  # JSON string
    relevancia = Column(Float, default=1.0)
    occurrence_count = Column(Integer, default=1)
    embedding = Column(Vector(384))  # Dimensão para sentence-transformers/all-MiniLM-L6-v2
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Theme(id={self.id}, tema_geral='{self.tema_geral}', subtema='{self.subtema}')>"