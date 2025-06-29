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
