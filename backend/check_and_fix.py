#!/usr/bin/env python3
"""
Script para verificar e corrigir problemas no banco de dados
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal, engine
from app.models import Base, Cliente, Procedimento, Material, Atendimento
from app.scripts.populate_test_data import populate_test_data

def check_database():
    """Verifica o estado do banco de dados"""
    print("🔍 Verificando banco de dados...")
    
    try:
        # Criar tabelas se não existirem
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas/verificadas")
        
        db = SessionLocal()
        try:
            # Verificar dados
            clientes_count = db.query(Cliente).count()
            procedimentos_count = db.query(Procedimento).count()
            materiais_count = db.query(Material).count()
            atendimentos_count = db.query(Atendimento).count()
            
            print(f"📊 Status do banco:")
            print(f"   Clientes: {clientes_count}")
            print(f"   Procedimentos: {procedimentos_count}")
            print(f"   Materiais: {materiais_count}")
            print(f"   Atendimentos: {atendimentos_count}")
            
            # Se não há dados, popular
            if clientes_count == 0:
                print("📝 Banco vazio. Populando dados de teste...")
                db.close()
                populate_test_data()
                print("✅ Dados de teste adicionados!")
            else:
                print("✅ Banco já possui dados")
                
        except Exception as e:
            print(f"❌ Erro ao verificar banco: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")

def test_api_endpoints():
    """Testa os endpoints da API"""
    print("\n🌐 Testando endpoints da API...")
    
    try:
        import requests
        
        endpoints = [
            ("Health Check", "http://localhost:8001/health"),
            ("Procedimentos", "http://localhost:8001/api/v1/procedimentos"),
            ("Atendimentos", "http://localhost:8001/api/v1/atendimentos"),
            ("Clientes", "http://localhost:8001/api/v1/clientes"),
            ("Materiais", "http://localhost:8001/api/v1/materiais")
        ]
        
        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {name}: OK")
                else:
                    print(f"❌ {name}: {response.status_code}")
            except requests.exceptions.ConnectionError:
                print(f"❌ {name}: Backend não está rodando")
            except Exception as e:
                print(f"❌ {name}: {str(e)}")
                
    except ImportError:
        print("⚠️  requests não instalado. Instale com: pip install requests")

def main():
    """Função principal"""
    print("🔧 Verificação e Correção - Harmofin")
    print("=" * 40)
    
    # Verificar banco
    check_database()
    
    # Testar API
    test_api_endpoints()
    
    print("\n🏁 Verificação concluída!")
    print("\n💡 Se ainda houver problemas:")
    print("1. Verifique se o backend está rodando: uvicorn app.main:app --reload --host 0.0.0.0 --port 8001")
    print("2. Verifique se o frontend está rodando: npm run dev")
    print("3. Execute este script novamente se necessário")

if __name__ == "__main__":
    main() 