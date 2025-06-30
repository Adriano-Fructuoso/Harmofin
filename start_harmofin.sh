#!/bin/bash

echo "🚀 Iniciando Harmofin - Sistema de Gestão de Clínicas de Harmonização"
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Execute este script na raiz do projeto Harmofin"
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

echo ""
echo "🔧 Iniciando Backend..."
cd backend

# Ativar ambiente virtual
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Ambiente virtual ativado"
else
    echo "❌ Ambiente virtual não encontrado. Execute primeiro: ./fix_and_start.sh"
    exit 1
fi

# Iniciar backend em background
echo "🚀 Iniciando backend na porta 8001..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

cd ..

# Aguardar backend inicializar
sleep 3

# Testar backend
echo "🧪 Testando backend..."
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ Backend iniciado com sucesso!"
else
    echo "❌ Falha ao iniciar backend"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎨 Iniciando Frontend..."
cd frontend

# Iniciar frontend
echo "🚀 Iniciando frontend..."
npm run dev &
FRONTEND_PID=$!

cd ..

# Aguardar frontend inicializar
sleep 5

echo ""
echo "🎉 Harmofin iniciado com sucesso!"
echo ""
echo "📱 Acesse:"
echo "   🌐 Frontend: http://localhost:5173"
echo "   🔧 Backend:  http://localhost:8001"
echo "   📚 API Docs: http://localhost:8001/docs"
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