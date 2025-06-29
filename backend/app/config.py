"""
Configurações centralizadas da aplicação
"""

import os
from typing import List

class Settings:
    # Configurações da aplicação
    APP_TITLE: str = "Sistema de Gestão de Clínicas de Harmonização"
    APP_DESCRIPTION: str = "API para cadastro e gestão de clientes, atendimentos, procedimentos e materiais"
    APP_VERSION: str = "2.0.0"
    
    # Configurações do banco de dados
    DATABASE_URL: str = "sqlite:///./clientes.db"
    
    # Configurações CORS - Melhoradas para desenvolvimento
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:4173",  # Porta de preview do Vite
        "http://127.0.0.1:4173",
        "*"  # Em produção, remover este wildcard
    ]
    
    # Configurações do servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # Configurações de ambiente
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"

settings = Settings() 