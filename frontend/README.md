# Frontend - Sistema de Gestão de Clientes

Interface React para o sistema de gestão de clientes.

## 🚀 Tecnologias

- **React 18** com TypeScript
- **Vite** - Build tool rápido
- **Ant Design** - UI Library
- **Axios** - HTTP Client
- **React Query** - Gerenciamento de estado

## 📋 Pré-requisitos

- Node.js 16+ 
- npm ou yarn

## 🛠️ Instalação

1. **Instalar dependências:**
```bash
npm install
```

2. **Executar em modo desenvolvimento:**
```bash
npm run dev
```

3. **Acessar a aplicação:**
- http://localhost:3000

## 🔧 Scripts Disponíveis

- `npm run dev` - Executa em modo desenvolvimento
- `npm run build` - Gera build de produção
- `npm run preview` - Visualiza build de produção
- `npm run lint` - Executa linter

## 📁 Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
│   ├── ClienteForm.tsx  # Formulário de cliente
│   └── ClienteTable.tsx # Tabela de clientes
├── pages/              # Páginas da aplicação
│   └── Clientes.tsx    # Página principal
├── services/           # Serviços de API
│   └── api.ts         # Configuração da API
├── types/              # Tipos TypeScript
│   └── cliente.ts     # Tipos de cliente
├── App.tsx            # Componente principal
└── main.tsx           # Ponto de entrada
```

## 🔗 Integração com Backend

O frontend está configurado para se comunicar com a API FastAPI na porta 8001.

**Configuração do proxy (vite.config.ts):**
```typescript
proxy: {
  '/api': {
    target: 'http://localhost:8001',
    changeOrigin: true,
  },
}
```

## 🎨 Funcionalidades

- ✅ Listagem de clientes com paginação
- ✅ Criação de novos clientes
- ✅ Edição de clientes existentes
- ✅ Remoção de clientes
- ✅ Busca por nome/telefone
- ✅ Estatísticas em tempo real
- ✅ Interface responsiva

## 🚀 Deploy

Para gerar build de produção:
```bash
npm run build
```

Os arquivos serão gerados na pasta `dist/`. 