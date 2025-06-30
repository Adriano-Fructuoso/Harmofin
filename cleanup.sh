#!/bin/bash

echo "🧹 Limpando arquivos desnecessários do projeto Harmofin..."
echo ""

# Verificar se estamos no diretório correto
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Execute este script na raiz do projeto Harmofin"
    exit 1
fi

echo "📋 Arquivos que serão removidos:"
echo ""

# Lista de arquivos para remover
files_to_remove=(
    "app.py"
    "streamlit_app.py"
    "packages.txt"
    "requirements.txt"
    "fix_and_start.sh"
    "start_harmofin.sh"
    "start_project.sh"
    "run_dev.sh"
    "package-lock.json"
)

# Lista de diretórios para remover
dirs_to_remove=(
    ".streamlit"
    ".devcontainer"
)

# Mostrar arquivos que serão removidos
echo "📄 Arquivos:"
for file in "${files_to_remove[@]}"; do
    if [ -f "$file" ]; then
        echo "   - $file"
    fi
done

echo ""
echo "📁 Diretórios:"
for dir in "${dirs_to_remove[@]}"; do
    if [ -d "$dir" ]; then
        echo "   - $dir"
    fi
done

echo ""
read -p "🤔 Continuar com a limpeza? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️ Removendo arquivos..."
    
    # Remover arquivos
    for file in "${files_to_remove[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "   ✅ Removido: $file"
        fi
    done
    
    # Remover diretórios
    for dir in "${dirs_to_remove[@]}"; do
        if [ -d "$dir" ]; then
            rm -rf "$dir"
            echo "   ✅ Removido: $dir"
        fi
    done
    
    echo ""
    echo "🎉 Limpeza concluída!"
    echo ""
    echo "📋 Arquivos mantidos:"
    echo "   ✅ docker-compose.yml"
    echo "   ✅ docker-start.sh"
    echo "   ✅ DOCKER.md"
    echo "   ✅ .dockerignore"
    echo "   ✅ backend/ (completo)"
    echo "   ✅ frontend/ (completo)"
    echo "   ✅ README.md"
    echo "   ✅ docs/API.md"
    echo ""
    echo "🚀 Agora você pode usar: ./docker-start.sh"
    
else
    echo "❌ Limpeza cancelada"
fi 