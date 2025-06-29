#!/usr/bin/env python3
"""
Script para corrigir problemas com procedimentos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal
from app.models import Procedimento, Material, ProcedimentoMaterial
from app.scripts.populate_test_data import populate_test_data

def verificar_banco():
    """Verifica se o banco está funcionando"""
    print("🔍 Verificando banco de dados...")
    
    db = SessionLocal()
    try:
        # Verificar se as tabelas existem
        procedimentos_count = db.query(Procedimento).count()
        materiais_count = db.query(Material).count()
        
        print(f"✅ Procedimentos: {procedimentos_count}")
        print(f"✅ Materiais: {materiais_count}")
        
        if procedimentos_count == 0:
            print("�� Banco vazio. Populando dados de teste...")
            db.close()
            populate_test_data()
        else:
            print("✅ Banco já possui dados")
            
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

def testar_procedimentos():
    """Testa a funcionalidade de procedimentos"""
    print("🧪 Testando procedimentos...")
    
    db = SessionLocal()
    try:
        # Testar listagem
        procedimentos = db.query(Procedimento).all()
        print(f"✅ {len(procedimentos)} procedimentos encontrados")
        
        for proc in procedimentos:
            print(f"   - ID: {proc.id}, Nome: {proc.nome}")
            
            # Testar materiais padrão
            materiais_padrao = db.query(ProcedimentoMaterial).filter(
                ProcedimentoMaterial.procedimento_id == proc.id
            ).all()
            
            print(f"     Materiais padrão: {len(materiais_padrao)}")
            
    except Exception as e:
        print(f"❌ Erro ao testar procedimentos: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    verificar_banco()
    testar_procedimentos() 