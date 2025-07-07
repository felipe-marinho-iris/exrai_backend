import asyncio
import sys
from pathlib import Path

# Adicionar o diretório pai ao path para imports
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import text
from src.core.database import engine
from src.models.database import Base
from loguru import logger


async def init_database():
    """Inicializa o banco de dados e cria as tabelas"""
    try:
        logger.info("Iniciando criação do banco de dados...")
        
        async with engine.begin() as conn:
            # Criar extensão pgvector se não existir
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            logger.info("Extensão pgvector criada/verificada")
            
            # Criar todas as tabelas
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tabelas criadas com sucesso")
            
        logger.info("Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_database())