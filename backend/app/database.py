"""
Configuração do banco de dados SQLite
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./clientes.db"

# Criar engine do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário para SQLite
)

# Criar sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db():
    """
    Função para obter uma sessão do banco de dados
    Usada como dependência nos endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Importar todos os modelos para garantir que sejam criados
from .models import Cliente, Procedimento, Material, Atendimento, AtendimentoMaterial, AtendimentoProcedimento 