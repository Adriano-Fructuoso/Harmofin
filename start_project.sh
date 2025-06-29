#!/bin/bash

echo "🚀 Iniciando o projeto Harmofin..."

# Verificar se estamos no diretório correto
if [ ! -f "backend/app/main.py" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto (pasta Harmofin)"
    exit 1
fi

# Função para verificar se uma porta está em uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Porta $1 já está em uso"
        return 1
    else
        echo "✅ Porta $1 está livre"
        return 0
    fi
}

# Verificar portas
echo "🔍 Verificando portas..."
check_port 8001
check_port 5173

# Iniciar backend
echo ""
echo "🔧 Iniciando backend..."
cd backend

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "📦 Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Instalar dependências se necessário
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Verificar se o banco existe, se não, criar
if [ ! -f "clientes.db" ]; then
    echo "🗄️  Configurando banco de dados..."
    python scripts/setup_db.py
fi

# Iniciar backend em background
echo "🚀 Iniciando backend na porta 8001..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

# Aguardar um pouco para o backend inicializar
sleep 3

# Testar se o backend está funcionando
echo "🧪 Testando backend..."
python test_connection.py

if [ $? -eq 0 ]; then
    echo "✅ Backend iniciado com sucesso!"
else
    echo "❌ Falha ao iniciar backend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Voltar para a raiz e iniciar frontend
cd ..
echo ""
echo "🎨 Iniciando frontend..."
cd frontend

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependências do frontend..."
    npm install
fi

# Iniciar frontend
echo "🚀 Iniciando frontend na porta 5173..."
npm run dev &
FRONTEND_PID=$!

# Aguardar um pouco para o frontend inicializar
sleep 5

echo ""
echo "🎉 Projeto iniciado com sucesso!"
echo ""
echo "📱 Acesse:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "🛑 Para parar o projeto, pressione Ctrl+C"

# Função para limpar processos ao sair
cleanup() {
    echo ""
    echo "🛑 Parando serviços..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Serviços parados"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Manter o script rodando
wait 