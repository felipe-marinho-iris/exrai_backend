# Plano: Sistema de Análise de Temas em Conversas

## Objetivo
Criar um agente que analise conversas de 24h para identificar temas relevantes, evitar duplicações usando busca semântica e gerenciar relevância dos temas.

## Schema JSON dos Temas
```json
{
  "tema_geral": "string",
  "subtema": "string (específico)",
  "categoria": "profissional | social | informativo | emocional | etc",
  "palavras_chave": ["string", "string", ...]
}
```

## Lista de Tarefas

### 1. Estrutura do Projeto
- [ ] Criar estrutura de pastas básica do projeto
- [ ] Configurar ambiente Python com dependências necessárias
- [ ] Criar arquivo requirements.txt

### 2. Modelo de Dados
- [ ] Definir schema do banco de dados para temas
- [ ] Criar modelos SQLAlchemy ou equivalente
- [ ] Incluir campos para vetorização e pontuação de relevância

### 3. Agente de Análise de Temas
- [ ] Implementar função para processar conversas de 24h
- [ ] Criar lógica de extração de temas usando LLM
- [ ] Implementar parsing do resultado em formato JSON

### 4. Sistema de Vetorização
- [ ] Configurar modelo de embeddings (ex: OpenAI, Sentence Transformers)
- [ ] Implementar função para vetorizar temas
- [ ] Criar índice vetorial para busca eficiente

### 5. Busca Semântica e Deduplicação
- [ ] Implementar busca por similaridade vetorial
- [ ] Definir threshold de similaridade para considerar tema duplicado
- [ ] Criar lógica de decisão: novo tema vs tema existente

### 6. Sistema de Pontuação/Relevância
- [ ] Definir algoritmo de pontuação para relevância
- [ ] Implementar incremento de relevância para temas existentes
- [ ] Criar sistema de decay temporal (opcional)

### 7. API/Interface
- [ ] Criar endpoint para processar batch de conversas
- [ ] Implementar endpoint para consultar temas
- [ ] Adicionar endpoint para estatísticas de temas

### 8. Testes
- [ ] Criar testes unitários para cada componente
- [ ] Implementar testes de integração
- [ ] Testar com dados reais de conversas

## Tecnologias Sugeridas
- Python 3.10+
- FastAPI para API
- PostgreSQL com pgvector para busca vetorial
- SQLAlchemy para ORM
- OpenAI/Anthropic API para análise de temas
- Sentence Transformers ou OpenAI Embeddings para vetorização

## Próximos Passos
1. Validar este plano
2. Começar pela estrutura básica do projeto
3. Implementar incrementalmente cada componente

## 📝 Revisão da Implementação

### ✅ Componentes Implementados

1. **Estrutura do Projeto** ✓
   - Organização modular com separação clara de responsabilidades
   - Configuração com variáveis de ambiente

2. **Modelos de Dados** ✓
   - Schema Pydantic para validação
   - Modelos SQLAlchemy com suporte pgvector
   - Suporte para embeddings de 384 dimensões

3. **Análise de Temas (LLM)** ✓
   - Suporte para OpenAI e Anthropic
   - Extração estruturada em formato JSON
   - Validação e normalização de categorias

4. **Sistema de Embeddings** ✓
   - Sentence Transformers para vetorização local
   - Função de similaridade de cosseno
   - Geração de embeddings para temas

5. **Busca Semântica** ✓
   - Busca vetorial com pgvector
   - Threshold configurável de similaridade
   - Detecção eficiente de temas duplicados

6. **Sistema de Relevância** ✓
   - Incremento automático de relevância
   - Contador de ocorrências
   - Ordenação por relevância

7. **API REST** ✓
   - Endpoints para análise, listagem e estatísticas
   - Documentação automática com FastAPI
   - Tratamento de erros

### 🔧 Detalhes Técnicos

- **Banco de Dados**: PostgreSQL com pgvector para busca vetorial eficiente
- **Framework**: FastAPI para alta performance e documentação automática
- **Embeddings**: Modelo all-MiniLM-L6-v2 (384 dimensões, rápido e eficiente)
- **Async**: Operações assíncronas para melhor performance

### 📊 Fluxo de Processamento

1. Recebe batch de conversas via API
2. Analisa com LLM para extrair temas estruturados
3. Gera embeddings para cada tema
4. Busca temas similares no banco (busca vetorial)
5. Se similar: atualiza relevância; Se novo: cria registro
6. Retorna análise completa com estatísticas

### 🚀 Próximos Passos Sugeridos

1. **Testes**: Implementar testes unitários e de integração
2. **Docker**: Criar Dockerfile e docker-compose
3. **CI/CD**: Configurar pipeline de deploy
4. **Monitoramento**: Adicionar métricas e logs estruturados
5. **Cache**: Implementar cache para embeddings frequentes
6. **Batch Processing**: Otimizar para grandes volumes