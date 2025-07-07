import json
from typing import List, Dict, Any
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from src.core.config import settings
from src.models.schemas import ThemeBase, ThemeCategory
from loguru import logger


class ThemeAnalyzer:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        if settings.anthropic_api_key:
            self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    
    async def analyze_conversations(self, conversations: List[str]) -> List[ThemeBase]:
        """Analisa conversas e extrai temas relevantes"""
        
        # Combinar conversas em um texto único para análise
        combined_text = "\n\n---\n\n".join(conversations)
        
        # Preparar prompt
        prompt = self._prepare_prompt(combined_text)
        
        # Usar o cliente disponível
        if self.anthropic_client:
            themes_data = await self._analyze_with_anthropic(prompt)
        elif self.openai_client:
            themes_data = await self._analyze_with_openai(prompt)
        else:
            raise ValueError("Nenhuma API key configurada (OpenAI ou Anthropic)")
        
        # Parsear e validar temas
        themes = self._parse_themes(themes_data)
        return themes
    
    def _prepare_prompt(self, text: str) -> str:
        """Prepara o prompt para análise de temas"""
        return f"""Analise as seguintes conversas e identifique os temas relevantes discutidos.

Para cada tema identificado, forneça:
1. tema_geral: O tema principal em poucas palavras
2. subtema: Um aspecto específico do tema (bem detalhado)
3. categoria: Uma das seguintes - profissional, social, informativo, emocional, técnico, educacional, entretenimento, saúde, financeiro, outro
4. palavras_chave: Lista de 3-5 palavras-chave relacionadas

Retorne APENAS um JSON válido com uma lista de objetos tema, sem texto adicional.

Exemplo de formato:
[
  {{
    "tema_geral": "Desenvolvimento de Software",
    "subtema": "Implementação de APIs REST com FastAPI",
    "categoria": "técnico",
    "palavras_chave": ["API", "FastAPI", "REST", "backend", "Python"]
  }}
]

Conversas para análise:

{text}

Identifique no máximo {settings.max_themes_per_analysis} temas mais relevantes."""
    
    async def _analyze_with_anthropic(self, prompt: str) -> str:
        """Analisa usando Claude da Anthropic"""
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Erro ao analisar com Anthropic: {e}")
            raise
    
    async def _analyze_with_openai(self, prompt: str) -> str:
        """Analisa usando OpenAI"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erro ao analisar com OpenAI: {e}")
            raise
    
    def _parse_themes(self, themes_json: str) -> List[ThemeBase]:
        """Parseia e valida os temas extraídos"""
        try:
            # Tentar parsear o JSON
            themes_data = json.loads(themes_json)
            
            # Validar e criar objetos ThemeBase
            themes = []
            for theme_data in themes_data:
                # Normalizar categoria
                categoria = theme_data.get("categoria", "outro").lower()
                if categoria not in [cat.value for cat in ThemeCategory]:
                    categoria = ThemeCategory.OTHER.value
                
                theme = ThemeBase(
                    tema_geral=theme_data["tema_geral"],
                    subtema=theme_data["subtema"],
                    categoria=ThemeCategory(categoria),
                    palavras_chave=theme_data["palavras_chave"]
                )
                themes.append(theme)
            
            return themes
            
        except Exception as e:
            logger.error(f"Erro ao parsear temas: {e}")
            logger.error(f"JSON recebido: {themes_json}")
            raise ValueError(f"Erro ao parsear resposta da análise: {e}")