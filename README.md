# Exrai Theme Analyzer

Sistema de análise de conversas para identificação de temas relevantes com busca semântica e gerenciamento de relevância.

## 🚀 Funcionalidades

- **Análise de Conversas**: Extração automática de temas usando LLMs (OpenAI/Anthropic)
- **Busca Semântica**: Detecção de temas similares usando embeddings e pgvector
- **Sistema de Relevância**: Pontuação incremental para temas recorrentes
- **API REST**: Interface FastAPI para integração fácil
- **Persistência**: PostgreSQL com suporte vetorial

## 📋 Pré-requisitos

- Python 3.10+
- PostgreSQL com extensão pgvector
- API Key da OpenAI ou Anthropic

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/felipe-marinho-iris/exrai_backend.git
cd exrai_backend
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Configure o PostgreSQL:
```bash
# Certifique-se de que o PostgreSQL está rodando
# Crie o banco de dados
createdb exrai_db

# Instale a extensão pgvector
psql -d exrai_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

6. Inicialize o banco de dados:
```bash
python scripts/init_db.py
```

## 🚀 Executando o Projeto

1. Inicie o servidor:
```bash
python main.py
```

2. Acesse a documentação da API:
```
http://localhost:8000/docs
```

## 📝 Uso da API

### Analisar Conversas

```bash
POST /api/v1/themes/analyze
```

Payload:
```json
{
  "conversations": [
    "Conversa 1...",
    "Conversa 2..."
  ],
  "period_hours": 24
}
```

### Listar Temas

```bash
GET /api/v1/themes/
```

### Estatísticas

```bash
GET /api/v1/themes/stats
```

## 🧪 Testes

Execute o script de exemplo:
```bash
python examples/test_api.py
```

## 📁 Estrutura do Projeto

```
├── src/
│   ├── api/          # Rotas da API
│   ├── core/         # Configurações e database
│   ├── models/       # Modelos e schemas
│   ├── services/     # Lógica de negócio
│   └── utils/        # Utilitários
├── scripts/          # Scripts auxiliares
├── examples/         # Exemplos de uso
├── tests/            # Testes unitários
└── main.py           # Entrada da aplicação
```

## 🔧 Configurações

Principais variáveis de ambiente:

- `DATABASE_URL`: URL de conexão PostgreSQL
- `OPENAI_API_KEY`: Chave da API OpenAI
- `ANTHROPIC_API_KEY`: Chave da API Anthropic
- `SIMILARITY_THRESHOLD`: Limiar de similaridade (0.85 padrão)
- `EMBEDDING_MODEL`: Modelo de embeddings

## 📈 Schema JSON dos Temas

```json
{
  "tema_geral": "string",
  "subtema": "string (específico)",
  "categoria": "profissional | social | informativo | emocional | etc",
  "palavras_chave": ["string", "string", ...]
}
```

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request