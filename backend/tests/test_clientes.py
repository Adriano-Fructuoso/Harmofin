"""
Testes para o módulo de clientes
"""

import pytest
from fastapi.testclient import TestClient
from app.models import Cliente

def test_create_cliente(client, db_session):
    """Testa criação de cliente"""
    cliente_data = {
        "nome": "João Silva",
        "telefone": "(11) 99999-9999",
        "email": "joao@email.com",
        "observacao": "Cliente teste"
    }
    
    response = client.post("/api/v1/clientes", json=cliente_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["nome"] == cliente_data["nome"]
    assert data["telefone"] == cliente_data["telefone"]
    assert "id" in data

def test_get_clientes(client, db_session):
    """Testa listagem de clientes"""
    response = client.get("/api/v1/clientes")
    assert response.status_code == 200
    
    data = response.json()
    assert "clientes" in data
    assert "total" in data

def test_health_check(client):
    """Testa endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy" 