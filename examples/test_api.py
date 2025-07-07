import asyncio
import httpx
from datetime import datetime

# URL base da API
BASE_URL = "http://localhost:8000/api/v1"

# Exemplos de conversas para análise
SAMPLE_CONVERSATIONS = [
    """João: Estou trabalhando no novo sistema de autenticação com OAuth2.
    Maria: Ótimo! Você já implementou o refresh token?
    João: Sim, usei JWT com expiração de 7 dias. Também adicionei rate limiting.
    Maria: Perfeito, isso vai melhorar bastante a segurança da API.""",
    
    """Carlos: A reunião com o cliente foi produtiva hoje.
    Ana: Conseguimos fechar o escopo do projeto?
    Carlos: Sim, vamos desenvolver um dashboard de analytics com gráficos em tempo real.
    Ana: Vou preparar a proposta técnica com React e D3.js então.""",
    
    """Pedro: Você viu as novas features do Python 3.12?
    Laura: Sim! A melhoria de performance está incrível, principalmente nos type hints.
    Pedro: Estou animado para migrar nossos projetos. O pattern matching também evoluiu muito.
    Laura: Vamos planejar a migração gradual dos microserviços.""",
    
    """Equipe de vendas: Precisamos melhorar nossa taxa de conversão.
    Marketing: Sugiro implementarmos um CRM mais robusto com automação.
    Vendas: Concordo, e podemos integrar com nossas campanhas de email marketing.
    Marketing: Vou pesquisar soluções como HubSpot e Salesforce.""",
    
    """Dev1: O bug no sistema de pagamentos foi crítico ontem.
    Dev2: Descobri que era um race condition no processamento assíncrono.
    Dev1: Como você resolveu?
    Dev2: Implementei um lock distribuído com Redis. Agora está estável."""
]


async def test_analyze_conversations():
    """Testa o endpoint de análise de conversas"""
    async with httpx.AsyncClient() as client:
        print("=== Testando análise de conversas ===\n")
        
        response = await client.post(
            f"{BASE_URL}/themes/analyze",
            json={
                "conversations": SAMPLE_CONVERSATIONS,
                "period_hours": 24
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Análise concluída com sucesso!")
            print(f"📊 Temas identificados: {len(data['themes_identified'])}")
            print(f"🆕 Novos temas: {data['new_themes_count']}")
            print(f"🔄 Temas atualizados: {data['existing_themes_updated']}")
            print(f"⏰ Timestamp: {data['analysis_timestamp']}")
            
            print("\n📋 Temas encontrados:")
            for theme in data['themes_identified']:
                print(f"\n  - Tema: {theme['tema_geral']}")
                print(f"    Subtema: {theme['subtema']}")
                print(f"    Categoria: {theme['categoria']}")
                print(f"    Palavras-chave: {', '.join(theme['palavras_chave'])}")
                print(f"    Relevância: {theme['relevancia']}")
        else:
            print(f"❌ Erro: {response.status_code}")
            print(response.text)


async def test_get_all_themes():
    """Testa o endpoint de listagem de temas"""
    async with httpx.AsyncClient() as client:
        print("\n\n=== Testando listagem de temas ===\n")
        
        response = await client.get(f"{BASE_URL}/themes/")
        
        if response.status_code == 200:
            themes = response.json()
            print(f"✅ Total de temas no banco: {len(themes)}")
            
            if themes:
                print("\n🏆 Top 5 temas mais relevantes:")
                for theme in themes[:5]:
                    print(f"\n  - {theme['tema_geral']} / {theme['subtema']}")
                    print(f"    Relevância: {theme['relevancia']} | Ocorrências: {theme['occurrence_count']}")
        else:
            print(f"❌ Erro: {response.status_code}")


async def test_get_statistics():
    """Testa o endpoint de estatísticas"""
    async with httpx.AsyncClient() as client:
        print("\n\n=== Testando estatísticas ===\n")
        
        response = await client.get(f"{BASE_URL}/themes/stats")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estatísticas gerais:")
            print(f"   - Total de temas únicos: {stats['total_themes']}")
            print(f"   - Total de ocorrências: {stats['total_occurrences']}")
            print(f"   - Relevância média: {stats['average_relevance']}")
            
            print(f"\n📊 Distribuição por categoria:")
            for cat, count in stats['categories'].items():
                print(f"   - {cat}: {count}")
        else:
            print(f"❌ Erro: {response.status_code}")


async def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API Exrai Theme Analyzer")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Testar análise de conversas
    await test_analyze_conversations()
    
    # Aguardar um pouco antes do próximo teste
    await asyncio.sleep(2)
    
    # Testar listagem de temas
    await test_get_all_themes()
    
    # Testar estatísticas
    await test_get_statistics()
    
    print("\n✅ Testes concluídos!")


if __name__ == "__main__":
    asyncio.run(main())