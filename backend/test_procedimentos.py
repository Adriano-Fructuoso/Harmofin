#!/usr/bin/env python3
"""
Script para testar a funcionalidade de procedimentos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import SessionLocal
from app.models import Procedimento, Material, ProcedimentoMaterial

def test_procedimentos():
    """Testa a funcionalidade de procedimentos"""
    print("🔍 Testando funcionalidade de procedimentos...")
    
    db = SessionLocal()
    try:
        # 1. Verificar procedimentos existentes
        procedimentos = db.query(Procedimento).all()
        print(f"✅ Procedimentos encontrados: {len(procedimentos)}")
        
        for proc in procedimentos:
            print(f"   - ID: {proc.id}, Nome: {proc.nome}, Valor: R$ {proc.valor_padrao}")
            
            # Verificar materiais padrão
            materiais_padrao = db.query(ProcedimentoMaterial).filter(
                ProcedimentoMaterial.procedimento_id == proc.id
            ).all()
            
            if materiais_padrao:
                print(f"     Materiais padrão: {len(materiais_padrao)}")
                for mp in materiais_padrao:
                    material = db.query(Material).filter(Material.id == mp.material_id).first()
                    print(f"       - {material.nome if material else 'Material não encontrado'} (Qtd: {mp.quantidade_padrao})")
            else:
                print("     Nenhum material padrão")
        
        # 2. Verificar materiais disponíveis
        materiais = db.query(Material).filter(Material.ativo == True).all()
        print(f"\n✅ Materiais ativos disponíveis: {len(materiais)}")
        
        for material in materiais:
            print(f"   - ID: {material.id}, Nome: {material.nome}, Estoque: {material.quantidade_disponivel} {material.unidade}")
        
        # 3. Testar criação de procedimento
        print("\n🧪 Testando criação de procedimento...")
        
        # Verificar se já existe um procedimento de teste
        proc_teste = db.query(Procedimento).filter(Procedimento.nome == "Teste Frontend").first()
        if proc_teste:
            print("   Procedimento de teste já existe")
        else:
            # Criar procedimento de teste
            novo_proc = Procedimento(
                nome="Teste Frontend",
                descricao="Procedimento para testar o frontend",
                valor_padrao=300.0,
                ativo=True
            )
            db.add(novo_proc)
            db.flush()
            
            # Adicionar materiais padrão
            if materiais:
                material_teste = materiais[0]  # Usar o primeiro material disponível
                mp_teste = ProcedimentoMaterial(
                    procedimento_id=novo_proc.id,
                    material_id=material_teste.id,
                    quantidade_padrao=1.0
                )
                db.add(mp_teste)
                print(f"   Procedimento criado: ID {novo_proc.id}")
                print(f"   Material padrão adicionado: {material_teste.nome}")
            
            db.commit()
        
        print("\n✅ Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_procedimentos() 