# Guia de Troubleshooting - Harmofin

## 🔧 Problemas Comuns e Soluções

### 1. Erro "No module named 'app'"

**Problema:** Ao executar `python app/main.py` de dentro da pasta `app/`

**Solução:**
```bash
# ❌ Errado
cd backend/app
python main.py

# ✅ Correto
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 2. Porta 8001 já está em uso

**Problema:** `[Errno 48] Address already in use`

**Solução:**
```bash
# Verificar o que está usando a porta
lsof -ti:8001

# Matar o processo
kill -9 <PID>

# Ou usar outra porta
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### 3. Frontend não consegue conectar com o backend

**Problema:** Erro de CORS ou conexão recusada

**Soluções:**

#### A. Verificar se o backend está rodando
```bash
curl http://localhost:8001/health
```

#### B. Verificar configuração do proxy
O frontend deve usar o proxy do Vite:
```typescript
// ✅ Correto
const API_BASE_URL = '/api/v1';

// ❌ Errado
const API_BASE_URL = 'http://localhost:8001/api/v1';
```

#### C. Verificar configuração CORS
O backend deve permitir a origem do frontend:
```python
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite padrão
    "http://localhost:3000",  # Vite alternativo
    "*"  # Desenvolvimento
]
```

### 4. Banco de dados não encontrado

**Problema:** `sqlite3.OperationalError: no such table`

**Solução:**
```bash
cd backend
python scripts/setup_db.py
```

### 5. Dependências não instaladas

**Problema:** `ModuleNotFoundError`

**Solução:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Frontend não carrega

**Problema:** Erro no npm ou node_modules

**Solução:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 🧪 Testes de Conectividade

### Testar Backend
```bash
cd backend
python test_connection.py
```

### Testar Frontend
```bash
# Abrir DevTools (F12)
# Verificar aba Network
# Tentar acessar http://localhost:5173
```

### Testar API Manualmente
```bash
# Health check
curl http://localhost:8001/health

# Listar clientes
curl http://localhost:8001/api/v1/clientes

# Swagger docs
curl http://localhost:8001/docs
```

## 🔍 Logs e Debug

### Backend Logs
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 --log-level debug
```

### Frontend Logs
```bash
# No browser DevTools Console
# Verificar erros de rede na aba Network
```

### Verificar Processos
```bash
# Verificar se os serviços estão rodando
ps aux | grep uvicorn
ps aux | grep node

# Verificar portas em uso
lsof -i :8001
lsof -i :5173
```

## 🚀 Inicialização Correta

### Script Automático (Recomendado)
```bash
chmod +x start_project.sh
./start_project.sh
```

### Manual
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 📱 URLs de Acesso

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

## 🆘 Ainda com Problemas?

1. **Verificar logs** do backend e frontend
2. **Testar conectividade** com os comandos acima
3. **Verificar firewall** e antivírus
4. **Reiniciar serviços** completamente
5. **Verificar versões** do Python e Node.js

---

**Dica:** Use o script `start_project.sh` para inicialização automática e verificação de problemas! 