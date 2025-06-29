#!/usr/bin/env python3
"""
Script de diagnóstico para APIs de procedimentos e atendimentos
"""

import sys
import os
import requests
import json
from datetime import datetime

# Configurações
API_BASE = "http://localhost:8001"
ENDPOINTS = [
    "/health",
    "/api/v1/procedimentos",
    "/api/v1/procedimentos?ativo=true",
    "/api/v1/atendimentos",
    "/api/v1/clientes",
    "/api/v1/materiais"
]

def test_endpoint(endpoint):
    """Testa um endpoint específico"""
    try:
        url = f"{API_BASE}{endpoint}"
        print(f"🔍 Testando: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            if isinstance(data, dict) and 'total' in data:
                print(f"   📊 Total: {data.get('total', 'N/A')}")
            elif isinstance(data, list):
                print(f"   📊 Items: {len(data)}")
            else:
                print(f"   📊 Resposta: {type(data)}")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   📄 Resposta: {response.text[:200]}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro: Não foi possível conectar ao backend")
    except requests.exceptions.Timeout:
        print(f"❌ Erro: Timeout na requisição")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    print()

def test_database():
    """Testa conexão com banco de dados"""
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        
        from app.database import SessionLocal
        from app.models import Procedimento, Atendimento, Cliente, Material
        
        print("🗄️  Testando banco de dados...")
        
        db = SessionLocal()
        try:
            # Contar registros
            procedimentos_count = db.query(Procedimento).count()
            atendimentos_count = db.query(Atendimento).count()
            clientes_count = db.query(Cliente).count()
            materiais_count = db.query(Material).count()
            
            print(f"✅ Procedimentos: {procedimentos_count}")
            print(f"✅ Atendimentos: {atendimentos_count}")
            print(f"✅ Clientes: {clientes_count}")
            print(f"✅ Materiais: {materiais_count}")
            
            # Testar consulta específica
            if procedimentos_count > 0:
                proc = db.query(Procedimento).first()
                print(f"✅ Primeiro procedimento: {proc.nome}")
                
                # Testar relacionamento
                if hasattr(proc, 'materiais_padrao'):
                    print(f"✅ Materiais padrão: {len(proc.materiais_padrao)}")
                else:
                    print("⚠️  Relacionamento materiais_padrao não encontrado")
            
        except Exception as e:
            print(f"❌ Erro no banco: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erro ao conectar com banco: {e}")

def test_schema_conversion():
    """Testa conversão de schemas"""
    try:
        import sys
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        
        from app.database import SessionLocal
        from app.models import Procedimento
        from app.schemas import ProcedimentoSchema
        
        print("📋 Testando conversão de schemas...")
        
        db = SessionLocal()
        try:
            procedimentos = db.query(Procedimento).limit(1).all()
            
            if procedimentos:
                p = procedimentos[0]
                print(f"🔍 Testando conversão do procedimento: {p.nome}")
                
                # Testar conversão manual
                procedimento_dict = {
                    'id': p.id,
                    'nome': p.nome,
                    'descricao': p.descricao,
                    'valor_padrao': p.valor_padrao,
                    'ativo': p.ativo,
                    'data_cadastro': p.data_cadastro,
                    'materiais_padrao': []
                }
                
                # Adicionar materiais padrão se existirem
                if hasattr(p, 'materiais_padrao') and p.materiais_padrao:
                    for mp in p.materiais_padrao:
                        material_dict = {
                            'id': mp.id,
                            'material_id': mp.material_id,
                            'quantidade_padrao': mp.quantidade_padrao,
                            'material': None
                        }
                        procedimento_dict['materiais_padrao'].append(material_dict)
                
                schema = ProcedimentoSchema(**procedimento_dict)
                print(f"✅ Conversão manual bem-sucedida: {schema.nome}")
                
                # Testar conversão automática
                try:
                    schema_auto = ProcedimentoSchema.model_validate(p)
                    print(f"✅ Conversão automática bem-sucedida: {schema_auto.nome}")
                except Exception as e:
                    print(f"❌ Conversão automática falhou: {e}")
                
            else:
                print("⚠️  Nenhum procedimento encontrado para teste")
                
        except Exception as e:
            print(f"❌ Erro na conversão: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erro ao testar schemas: {e}")

def main():
    """Função principal"""
    print("🔧 Diagnóstico das APIs - Harmofin")
    print("=" * 50)
    print(f"⏰ Timestamp: {datetime.now()}")
    print()
    
    # Testar endpoints
    print("🌐 Testando endpoints...")
    for endpoint in ENDPOINTS:
        test_endpoint(endpoint)
    
    # Testar banco de dados
    test_database()
    print()
    
    # Testar conversão de schemas
    test_schema_conversion()
    print()
    
    print("🏁 Diagnóstico concluído!")

if __name__ == "__main__":
    main() 