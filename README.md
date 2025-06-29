# Harmofin - Sistema de Gestão de Clínicas de Harmonização

Sistema completo para gestão de clínicas de harmonização orofacial, desenvolvido com FastAPI (backend) e React (frontend).

## 🚀 Funcionalidades

### ✅ Gestão de Clientes
- Cadastro completo de clientes
- Busca e filtros avançados
- Histórico de atendimentos
- Observações personalizadas

### ✅ Gestão de Atendimentos
- Agendamento de consultas
- Múltiplos procedimentos por atendimento
- Controle de valores cobrados
- Status de atendimento

### ✅ Gestão de Procedimentos
- Cadastro de procedimentos
- Materiais padrão por procedimento
- Valores de referência
- Controle de ativação

### ✅ Gestão de Materiais
- Controle de estoque
- Alertas de estoque mínimo
- Histórico de utilização
- Valores unitários

## 🏗️ Arquitetura

```
Harmofin/
├── backend/          # API FastAPI
│   ├── app/         # Código da aplicação
│   ├── scripts/     # Scripts utilitários
│   ├── tests/       # Testes automatizados
│   └── migrations/  # Migrações de banco
├── frontend/        # Aplicação React
│   ├── src/         # Código fonte
│   ├── public/      # Arquivos públicos
│   └── dist/        # Build de produção
├── data/           # Dados de exemplo
├── docs/           # Documentação
└── clientes.db     # Banco SQLite
```

## 🛠️ Tecnologias

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **SQLite** - Banco de dados (desenvolvimento)
- **Pytest** - Testes automatizados

### Frontend
- **React 18** - Biblioteca JavaScript
- **TypeScript** - Tipagem estática
- **Vite** - Build tool moderna
- **Ant Design** - Componentes UI
- **Axios** - Cliente HTTP

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 16+
- npm ou yarn

## 🚀 Instalação Rápida

### Opção 1: Script Automático (Recomendado)

```bash
# Na raiz do projeto
chmod +x start_project.sh
./start_project.sh
```

### Opção 2: Instalação Manual

#### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd Harmofin
```

#### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python scripts/setup_db.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

#### 4. Acesse
- **API**: http://localhost:8001
- **Frontend**: http://localhost:5173
- **Documentação**: http://localhost:8001/docs

## 🐳 Docker (Opcional)

```bash
docker-compose up -d
```

## 📚 Documentação

- [Guia de Setup](docs/SETUP.md)
- [Documentação da API](docs/API.md)
- [Swagger UI](http://localhost:8001/docs)

## 🧪 Testes

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

## 🔧 Desenvolvimento

### Estrutura de Branches
- `main` - Código de produção
- `develop` - Desenvolvimento
- `feature/*` - Novas funcionalidades
- `hotfix/*` - Correções urgentes

### Padrões de Código
- **Python**: PEP 8
- **JavaScript**: ESLint + Prettier
- **Commits**: Conventional Commits

## 📊 Status do Projeto

- ✅ Backend API completa
- ✅ Frontend funcional
- ✅ Banco de dados estruturado
- ✅ Documentação básica
- 🔄 Testes automatizados
- 🔄 CI/CD pipeline
- 🔄 Deploy automatizado

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Adriano Fructuoso** - Desenvolvimento inicial

## 🙏 Agradecimentos

- FastAPI pela excelente documentação
- Ant Design pelos componentes UI
- Comunidade open source

---

**Harmofin** - Transformando a gestão de clínicas de harmonização orofacial 🏥✨
