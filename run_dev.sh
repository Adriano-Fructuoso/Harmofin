#!/bin/bash

# Script para executar o ambiente de desenvolvimento

echo "🚀 Iniciando ambiente de desenvolvimento Harmofin..."

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

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

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
echo "🚀 Para iniciar o desenvolvimento:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app/main.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "🌐 Acesse:"
echo "  API: http://localhost:8001"
echo "  Frontend: http://localhost:5173"
echo "  Docs: http://localhost:8001/docs" 