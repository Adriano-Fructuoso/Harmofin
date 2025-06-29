# Guia de Setup do Projeto

## Pré-requisitos

- Python 3.8+
- Node.js 16+
- npm ou yarn

## Estrutura do Projeto

```
Harmofin/
├── backend/          # API FastAPI
├── frontend/         # Aplicação React
├── data/            # Dados de exemplo
├── docs/            # Documentação
└── clientes.db      # Banco SQLite
```

## Setup do Backend

### 1. Ambiente Virtual

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Banco de Dados

```bash
python scripts/setup_db.py
```

### 4. Executar API

```bash
python app/main.py
```

A API estará disponível em: http://localhost:8001

## Setup do Frontend

### 1. Instalar Dependências

```bash
cd frontend
npm install
```

### 2. Executar Aplicação

```bash
npm run dev
```

O frontend estará disponível em: http://localhost:5173

## Testes

### Backend

```bash
cd backend
pytest tests/
```

### Frontend

```bash
cd frontend
npm test
```

## Desenvolvimento

### Variáveis de Ambiente

Criar arquivo `.env` no backend:

```env
ENVIRONMENT=development
DATABASE_URL=sqlite:///./clientes.db
```

### Logs

Os logs são exibidos no console durante o desenvolvimento.

## Produção

### Backend

1. Configurar variáveis de ambiente
2. Usar gunicorn ou uvicorn em produção
3. Configurar proxy reverso (nginx)

### Frontend

1. Build de produção: `npm run build`
2. Servir arquivos estáticos
3. Configurar CDN se necessário

## Troubleshooting

### Porta Ocupada

Se a porta 8001 estiver ocupada:

```bash
lsof -ti:8001 | xargs kill -9
```

### Banco de Dados

Para resetar o banco:

```bash
rm clientes.db
python backend/scripts/setup_db.py
```

### Dependências

Para atualizar dependências:

```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
npm update
``` 