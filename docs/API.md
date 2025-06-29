# Documentação da API

## Visão Geral

API REST para sistema de gestão de clínicas de harmonização orofacial, desenvolvida com FastAPI e SQLAlchemy.

## Base URL

```
http://localhost:8001
```

## Endpoints

### Clientes

#### `GET /api/v1/clientes`
Lista todos os clientes cadastrados.

**Resposta:**
```json
{
  "clientes": [...],
  "total": 10
}
```

#### `POST /api/v1/clientes`
Cadastra um novo cliente.

**Body:**
```json
{
  "nome": "João Silva",
  "telefone": "(11) 99999-9999",
  "email": "joao@email.com",
  "observacao": "Cliente VIP"
}
```

#### `GET /api/v1/clientes/{id}`
Busca cliente por ID.

#### `PUT /api/v1/clientes/{id}`
Atualiza dados do cliente.

#### `DELETE /api/v1/clientes/{id}`
Remove cliente.

#### `GET /api/v1/clientes/search?query=termo`
Busca clientes por nome ou telefone.

### Atendimentos

#### `GET /api/v1/atendimentos`
Lista todos os atendimentos.

#### `POST /api/v1/atendimentos`
Cria novo atendimento.

#### `GET /api/v1/atendimentos/{id}`
Busca atendimento por ID.

#### `PUT /api/v1/atendimentos/{id}`
Atualiza atendimento.

#### `DELETE /api/v1/atendimentos/{id}`
Remove atendimento.

### Procedimentos

#### `GET /api/v1/procedimentos`
Lista todos os procedimentos.

#### `POST /api/v1/procedimentos`
Cria novo procedimento.

#### `GET /api/v1/procedimentos/{id}`
Busca procedimento por ID.

#### `PUT /api/v1/procedimentos/{id}`
Atualiza procedimento.

#### `DELETE /api/v1/procedimentos/{id}`
Remove procedimento.

#### `GET /api/v1/procedimentos/{id}/materiais`
Lista materiais padrão do procedimento.

### Materiais

#### `GET /api/v1/materiais`
Lista todos os materiais.

#### `POST /api/v1/materiais`
Cria novo material.

#### `GET /api/v1/materiais/{id}`
Busca material por ID.

#### `PUT /api/v1/materiais/{id}`
Atualiza material.

#### `DELETE /api/v1/materiais/{id}`
Remove material.

## Códigos de Status

- `200` - Sucesso
- `201` - Criado
- `400` - Bad Request
- `404` - Não encontrado
- `422` - Dados inválidos
- `500` - Erro interno

## Autenticação

Atualmente a API não possui autenticação. Em produção, implementar JWT ou OAuth2.

## Rate Limiting

Não implementado. Considerar implementar em produção.

## Versionamento

API versão 2.0.0 