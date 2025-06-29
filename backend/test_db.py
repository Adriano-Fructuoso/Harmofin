#!/usr/bin/env python3
"""
Script para testar a conexão com o banco de dados
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal
from app.models import Procedimento, Material, Cliente, Atendimento

def test_database():
    """Testa a conexão com o banco de dados"""
    print("🔍 Testando conexão com o banco de dados...")
    
    db = SessionLocal()
    try:
        # Testar contagem de cada tabela
        clientes_count = db.query(Cliente).count()
        print(f"✅ Clientes: {clientes_count}")
        
        materiais_count = db.query(Material).count()
        print(f"✅ Materiais: {materiais_count}")
        
        atendimentos_count = db.query(Atendimento).count()
        print(f"✅ Atendimentos: {atendimentos_count}")
        
        # Testar procedimentos especificamente
        try:
            procedimentos_count = db.query(Procedimento).count()
            print(f"✅ Procedimentos: {procedimentos_count}")
            
            # Tentar buscar um procedimento específico
            procedimentos = db.query(Procedimento).limit(5).all()
            print(f"✅ Primeiros 5 procedimentos carregados: {len(procedimentos)}")
            
            for proc in procedimentos:
                print(f"   - ID: {proc.id}, Nome: {proc.nome}")
                
        except Exception as e:
            print(f"❌ Erro ao consultar procedimentos: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_database() 