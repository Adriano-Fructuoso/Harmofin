#!/bin/bash

echo "�� Preparando projeto para GitHub..."

# 1. Remover arquivos desnecessários
echo "�� Removendo arquivos desnecessários..."
rm -f clientes.db
rm -rf venv-clientes
rm -rf .vscode
rm -f backend/test_connection.py
rm -f backend/fix_procedimentos.py

# 2. Verificar .gitignore
echo "📝 Verificando .gitignore..."
if ! grep -q "clientes.db" .gitignore; then
    echo "clientes.db" >> .gitignore
fi

# 3. Criar arquivos necessários
echo "📄 Criando arquivos necessários..."

# LICENSE
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Adriano Fructuoso

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# CONTRIBUTING.md
cat > CONTRIBUTING.md << 'EOF'
# Guia de Contribuição - Harmofin

Obrigado por considerar contribuir com o projeto Harmofin! 🚀

## 📋 Como Contribuir

### 1. Fork e Clone
```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/Harmofin.git
cd Harmofin
```

### 2. Configurar Ambiente
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 3. Criar Branch
```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
```

### 4. Desenvolver
- Faça suas alterações
- Teste localmente
- Siga os padrões de código

### 5. Commit e Push
```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade
```

### 6. Pull Request
- Abra um Pull Request no GitHub
- Descreva as mudanças
- Aguarde a revisão

## 📝 Padrões de Commit

Use Conventional Commits:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes
- `chore:` manutenção

## �� Testes

Execute os testes antes de submeter:
```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend
npm test
```

## 📚 Documentação

- Mantenha a documentação atualizada
- Adicione comentários em código complexo
- Atualize o README se necessário

Obrigado por contribuir! 🙏
EOF

# 4. Atualizar README com badges
echo "�� Atualizando README..."
sed -i '' '1s/^/[![Python](https:\/\/img.shields.io\/badge\/Python-3.8+-blue.svg)](https:\/\/www.python.org\/)\n[![React](https:\/\/img.shields.io\/badge\/React-18-blue.svg)](https:\/\/reactjs.org\/)\n[![FastAPI](https:\/\/img.shields.io\/badge\/FastAPI-0.104.1-green.svg)](https:\/\/fastapi.tiangolo.com\/)\n[![License](https:\/\/img.shields.io\/badge\/License-MIT-yellow.svg)](LICENSE)\n[![Status](https:\/\/img.shields.io\/badge\/Status-Produção-brightgreen.svg)]()\n\n/' README.md

echo "✅ Projeto preparado para GitHub!"
echo ""
echo "�� Próximos passos:"
echo "1. git add ."
echo "2. git commit -m 'feat: prepara projeto para GitHub'"
echo "3. git push origin main"
echo ""
echo "🔗 URLs importantes:"
echo "- Frontend: http://localhost:5173"
echo "- Backend: http://localhost:8001"
echo "- API Docs: http://localhost:8001/docs" 