#!/bin/bash

echo "🐳 Iniciando Harmofin com Docker..."
echo ""

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Instale o Docker Compose primeiro."
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados"

# Verificar se estamos no diretório correto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Execute este script na raiz do projeto Harmofin"
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Construir e iniciar containers
echo "🔨 Construindo containers..."
docker-compose build --no-cache

echo "🚀 Iniciando aplicação..."
docker-compose up -d

# Aguardar containers iniciarem
echo "⏳ Aguardando containers iniciarem..."
sleep 10

# Verificar status
echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "🎉 Harmofin iniciado com Docker!"
echo ""
echo "📱 Acesse:"
echo "   🌐 Frontend: http://localhost:5173"
echo "   🔧 Backend:  http://localhost:8001"
echo "   📚 API Docs: http://localhost:8001/docs"
echo ""
echo "🛑 Para parar: docker-compose down"
echo "📋 Para ver logs: docker-compose logs -f" 