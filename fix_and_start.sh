#!/bin/bash

echo "🔧 Corrigindo ambiente e iniciando projeto Harmofin..."

# Verificar se estamos no diretório correto
if [ ! -f "README.md" ]; then
    echo "❌ Execute este script na raiz do projeto Harmofin"
    exit 1
fi

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependências
echo "📋 Verificando dependências..."

if ! command_exists python3; then
    echo "❌ Python 3 não encontrado. Instale Python 3.8+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js não encontrado. Instale Node.js 16+"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm não encontrado. Instale npm"
    exit 1
fi

echo "✅ Dependências verificadas"

# Setup do Backend
echo "🔧 Configurando Backend..."

cd backend

# Remover ambiente virtual corrompido se existir
if [ -d "venv" ]; then
    echo "🗑️ Removendo ambiente virtual corrompido..."
    rm -rf venv
fi

# Criar novo ambiente virtual
echo "📦 Criando novo ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📥 Instalando dependências Python..."
pip install -r requirements.txt

# Setup do banco de dados
echo "🗄️ Configurando banco de dados..."
python scripts/setup_db.py

# Voltar para a raiz
cd ..

# Setup do Frontend
echo "🎨 Configurando Frontend..."

cd frontend

# Instalar dependências
echo "📥 Instalando dependências Node.js..."
npm install

# Voltar para a raiz
cd ..

echo "✅ Setup concluído!"
echo ""
echo "🚀 Iniciando serviços..."
echo ""

# Iniciar Backend em background
echo "🔧 Iniciando Backend..."
cd backend
source venv/bin/activate
python app/main.py &
BACKEND_PID=$!
cd ..

# Aguardar backend inicializar
sleep 3

# Iniciar Frontend em background
echo "🎨 Iniciando Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Aguardar frontend inicializar
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