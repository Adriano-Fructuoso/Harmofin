# 🐳 Harmofin - Deploy com Docker

Este documento explica como executar o Harmofin usando Docker.

## 📋 Pré-requisitos

- Docker Desktop instalado
- Docker Compose instalado
- Git

## 🚀 Início Rápido

### 1. Clone o repositório
```bash
git clone https://github.com/Adriano-Fructuoso/Harmofin.git
cd Harmofin
```

### 2. Execute com Docker
```bash
./docker-start.sh
```

Ou manualmente:
```bash
docker-compose up -d
```

### 3. Acesse a aplicação
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

## 🛠️ Comandos Úteis

### Iniciar aplicação
```bash
docker-compose up -d
```

### Parar aplicação
```bash
docker-compose down
```

### Ver logs
```bash
# Todos os serviços
docker-compose logs -f

# Apenas backend
docker-compose logs -f backend

# Apenas frontend
docker-compose logs -f frontend
```

### Reconstruir containers
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Verificar status
```bash
docker-compose ps
```

## 📁 Estrutura dos Containers

### Backend (FastAPI)
- **Porta**: 8001
- **Imagem**: Python 3.9
- **Comando**: uvicorn app.main:app --host 0.0.0.0 --port 8001

### Frontend (React/Vite)
- **Porta**: 5173
- **Imagem**: Node.js 18
- **Comando**: npm run dev -- --host 0.0.0.0 --port 5173

## 🔧 Configurações

### Variáveis de Ambiente

#### Backend
- `ENVIRONMENT`: production
- `HOST`: 0.0.0.0
- `PORT`: 8001

#### Frontend
- `VITE_API_URL`: http://localhost:8001

### Volumes
- `./backend/clientes.db` → `/app/clientes.db` (banco de dados)
- `./backend/app` → `/app/app` (código do backend)
- `./frontend/src` → `/app/src` (código do frontend)

## 🚀 Deploy em Produção

### Railway
1. Conecte seu repositório GitHub
2. Configure as variáveis de ambiente
3. Deploy automático

### Render
1. Conecte seu repositório GitHub
2. Configure o Docker Compose
3. Deploy automático

### DigitalOcean App Platform
1. Conecte seu repositório GitHub
2. Configure o Docker Compose
3. Deploy automático

## 🐛 Troubleshooting

### Container não inicia
```bash
# Verificar logs
docker-compose logs

# Reconstruir
docker-compose build --no-cache
```

### Porta já em uso
```bash
# Parar containers
docker-compose down

# Verificar portas
lsof -i :8001
lsof -i :5173
```

### Problemas de permissão
```bash
# Dar permissão ao script
chmod +x docker-start.sh
```

## 📞 Suporte

Para problemas específicos do Docker, verifique:
1. Logs dos containers
2. Status dos serviços
3. Configurações de rede
4. Volumes montados 