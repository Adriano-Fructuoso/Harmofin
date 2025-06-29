"""
Configuração de testes para pytest
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Adicionar o diretório do app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.database import engine, Base, SessionLocal

@pytest.fixture
def client():
    """Cliente de teste para a aplicação"""
    return TestClient(app)

@pytest.fixture
def db_session():
    """Sessão de banco de dados para testes"""
    # Criar tabelas de teste
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Limpar tabelas após teste
        Base.metadata.drop_all(bind=engine) 