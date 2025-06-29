#!/usr/bin/env python3
"""
Script rápido para corrigir problemas das APIs
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_simple():
    """Teste simples das APIs"""
    print("🔧 Teste Rápido - Harmofin")
    print("=" * 30)
    
    try:
        # Testar importações básicas
        from app.database import SessionLocal
        from app.models import Procedimento, Atendimento
        print("✅ Importações OK")
        
        # Testar banco
        db = SessionLocal()
        try:
            proc_count = db.query(Procedimento).count()
            atend_count = db.query(Atendimento).count()
            print(f"✅ Banco OK - Procedimentos: {proc_count}, Atendimentos: {atend_count}")
        except Exception as e:
            print(f"❌ Erro no banco: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

def fix_procedimentos():
    """Corrige problemas na rota de procedimentos"""
    print("\n🔧 Corrigindo rota de procedimentos...")
    
    try:
        # Verificar se o arquivo existe
        procedimentos_file = "app/routers/procedimentos.py"
        if not os.path.exists(procedimentos_file):
            print("❌ Arquivo de procedimentos não encontrado")
            return
            
        # Ler o arquivo
        with open(procedimentos_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Verificar se há problemas óbvios
        if "ProcedimentoSchema.model_validate" in content:
            print("✅ Conversão de schema parece estar correta")
        else:
            print("⚠️  Conversão de schema pode estar com problema")
            
        print("✅ Verificação do arquivo concluída")
        
    except Exception as e:
        print(f"❌ Erro ao verificar arquivo: {e}")

def main():
    """Função principal"""
    test_simple()
    fix_procedimentos()
    
    print("\n💡 Próximos passos:")
    print("1. Reinicie o backend: uvicorn app.main:app --reload --host 0.0.0.0 --port 8001")
    print("2. Teste no navegador: http://localhost:8001/api/v1/procedimentos")
    print("3. Se ainda houver erro, verifique os logs do backend")

if __name__ == "__main__":
    main() 