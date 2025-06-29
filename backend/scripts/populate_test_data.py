#!/usr/bin/env python3
"""
Script para adicionar dados de teste ao banco de dados
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.database import SessionLocal
from app.models import Cliente, Procedimento, Material, Atendimento, AtendimentoProcedimento, AtendimentoMaterial
from datetime import datetime

def populate_test_data():
    """Adiciona dados de teste ao banco"""
    print("📝 Adicionando dados de teste...")
    
    db = SessionLocal()
    try:
        # Verificar se já existem dados
        if db.query(Cliente).count() > 0:
            print("ℹ️  Banco já possui dados. Pulando população.")
            return
        
        # 1. Criar clientes
        clientes = [
            Cliente(nome="Maria Silva", telefone="(11) 99999-1111", email="maria@email.com", observacao="Cliente VIP"),
            Cliente(nome="João Santos", telefone="(11) 99999-2222", email="joao@email.com"),
            Cliente(nome="Ana Costa", telefone="(11) 99999-3333", email="ana@email.com", observacao="Alérgica a alguns produtos"),
            Cliente(nome="Pedro Oliveira", telefone="(11) 99999-4444", email="pedro@email.com"),
            Cliente(nome="Carla Ferreira", telefone="(11) 99999-5555", email="carla@email.com")
        ]
        
        for cliente in clientes:
            db.add(cliente)
        db.flush()  # Para obter os IDs
        
        print(f"✅ {len(clientes)} clientes criados")
        
        # 2. Criar materiais
        materiais = [
            Material(nome="Toxina Botulínica", descricao="Botox 100U", quantidade_disponivel=10, unidade="frasco", valor_unitario=150.00, estoque_minimo=2),
            Material(nome="Ácido Hialurônico", descricao="Preenchimento labial", quantidade_disponivel=5, unidade="ml", valor_unitario=200.00, estoque_minimo=1),
            Material(nome="Agulha 30G", descricao="Agulha para aplicação", quantidade_disponivel=50, unidade="un", valor_unitario=2.50, estoque_minimo=10),
            Material(nome="Seringa 1ml", descricao="Seringa descartável", quantidade_disponivel=30, unidade="un", valor_unitario=1.50, estoque_minimo=5),
            Material(nome="Lidocaína 2%", descricao="Anestésico local", quantidade_disponivel=20, unidade="ml", valor_unitario=15.00, estoque_minimo=5)
        ]
        
        for material in materiais:
            db.add(material)
        db.flush()
        
        print(f"✅ {len(materiais)} materiais criados")
        
        # 3. Criar procedimentos
        procedimentos = [
            Procedimento(nome="Botox - Rugas da Testa", descricao="Aplicação de toxina botulínica na região frontal", valor_padrao=800.00),
            Procedimento(nome="Botox - Pés de Galinha", descricao="Aplicação de toxina botulínica na região periocular", valor_padrao=600.00),
            Procedimento(nome="Preenchimento Labial", descricao="Aplicação de ácido hialurônico nos lábios", valor_padrao=1200.00),
            Procedimento(nome="Preenchimento Malar", descricao="Aplicação de ácido hialurônico na região malar", valor_padrao=1500.00),
            Procedimento(nome="Botox - Masseter", descricao="Aplicação de toxina botulínica no músculo masseter", valor_padrao=1000.00)
        ]
        
        for procedimento in procedimentos:
            db.add(procedimento)
        db.flush()
        
        print(f"✅ {len(procedimentos)} procedimentos criados")
        
        # 4. Criar atendimentos
        atendimentos = [
            Atendimento(
                cliente_id=clientes[0].id,
                data_hora=datetime.now(),
                valor_cobrado=1400.00,
                observacoes="Primeira aplicação de Botox",
                status="realizado"
            ),
            Atendimento(
                cliente_id=clientes[1].id,
                data_hora=datetime.now(),
                valor_cobrado=1200.00,
                observacoes="Preenchimento labial realizado com sucesso",
                status="realizado"
            ),
            Atendimento(
                cliente_id=clientes[2].id,
                data_hora=datetime.now(),
                valor_cobrado=1600.00,
                observacoes="Botox + Preenchimento malar",
                status="realizado"
            )
        ]
        
        for atendimento in atendimentos:
            db.add(atendimento)
        db.flush()
        
        print(f"✅ {len(atendimentos)} atendimentos criados")
        
        # 5. Adicionar procedimentos aos atendimentos
        atendimento_procedimentos = [
            AtendimentoProcedimento(
                atendimento_id=atendimentos[0].id,
                procedimento_id=procedimentos[0].id,
                valor_cobrado=800.00,
                observacoes="Aplicação na região frontal"
            ),
            AtendimentoProcedimento(
                atendimento_id=atendimentos[0].id,
                procedimento_id=procedimentos[1].id,
                valor_cobrado=600.00,
                observacoes="Aplicação nos pés de galinha"
            ),
            AtendimentoProcedimento(
                atendimento_id=atendimentos[1].id,
                procedimento_id=procedimentos[2].id,
                valor_cobrado=1200.00,
                observacoes="Preenchimento labial completo"
            ),
            AtendimentoProcedimento(
                atendimento_id=atendimentos[2].id,
                procedimento_id=procedimentos[0].id,
                valor_cobrado=800.00,
                observacoes="Botox frontal"
            ),
            AtendimentoProcedimento(
                atendimento_id=atendimentos[2].id,
                procedimento_id=procedimentos[3].id,
                valor_cobrado=800.00,
                observacoes="Preenchimento malar"
            )
        ]
        
        for ap in atendimento_procedimentos:
            db.add(ap)
        
        # 6. Adicionar materiais utilizados
        atendimento_materiais = [
            AtendimentoMaterial(
                atendimento_id=atendimentos[0].id,
                material_id=materiais[0].id,
                quantidade_utilizada=1,
                valor_unitario_momento=150.00
            ),
            AtendimentoMaterial(
                atendimento_id=atendimentos[0].id,
                material_id=materiais[2].id,
                quantidade_utilizada=2,
                valor_unitario_momento=2.50
            ),
            AtendimentoMaterial(
                atendimento_id=atendimentos[1].id,
                material_id=materiais[1].id,
                quantidade_utilizada=2,
                valor_unitario_momento=200.00
            ),
            AtendimentoMaterial(
                atendimento_id=atendimentos[1].id,
                material_id=materiais[3].id,
                quantidade_utilizada=1,
                valor_unitario_momento=1.50
            )
        ]
        
        for am in atendimento_materiais:
            db.add(am)
        
        db.commit()
        print("✅ Dados de teste adicionados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao adicionar dados: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    populate_test_data() 