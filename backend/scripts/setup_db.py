#!/usr/bin/env python3
"""
Script para configurar o banco de dados inicial
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import engine, SessionLocal
from app.models import Base, Cliente, Procedimento, Material, Atendimento
from datetime import datetime

def setup_database():
    """Configura o banco de dados inicial"""
    print("🔧 Configurando banco de dados...")
    
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")
    
    # Verificar se já existem dados
    db = SessionLocal()
    try:
        if db.query(Cliente).count() > 0:
            print("ℹ️  Banco já possui dados. Setup concluído!")
            return
        
        print("📝 Banco vazio. Setup concluído!")
        
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    setup_database() 