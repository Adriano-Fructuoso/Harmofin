"""
Rotas para gerenciamento de atendimentos
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.database import get_db
from app.models import Atendimento, Cliente, Procedimento, Material, AtendimentoMaterial, AtendimentoProcedimento, ProcedimentoMaterial as ProcedimentoMaterialModel
from app.schemas import (
    AtendimentoCreate, AtendimentoUpdate, Atendimento as AtendimentoSchema,
    AtendimentoList, AtendimentoFiltro, AtendimentoProcedimentoCreate,
    ProcedimentoMaterial as ProcedimentoMaterialSchema
)

router = APIRouter()

@router.get("/atendimentos", response_model=AtendimentoList)
async def listar_atendimentos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    procedimento_id: Optional[int] = Query(None, description="Filtrar por procedimento"),
    data_inicio: Optional[datetime] = Query(None, description="Data de início"),
    data_fim: Optional[datetime] = Query(None, description="Data de fim"),
    status: Optional[str] = Query(None, description="Status do atendimento"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os atendimentos com filtros opcionais
    """
    query = db.query(Atendimento).options(
        joinedload(Atendimento.procedimentos).joinedload(AtendimentoProcedimento.procedimento)
    )
    
    # Aplicar filtros
    if cliente_id is not None:
        query = query.filter(Atendimento.cliente_id == cliente_id)
    
    if procedimento_id is not None:
        # Filtrar por procedimento usando a tabela intermediária
        query = query.join(AtendimentoProcedimento).filter(
            AtendimentoProcedimento.procedimento_id == procedimento_id
        )
    
    if data_inicio is not None:
        query = query.filter(Atendimento.data_hora >= data_inicio)
    
    if data_fim is not None:
        query = query.filter(Atendimento.data_hora <= data_fim)
    
    if status is not None:
        query = query.filter(Atendimento.status == status)
    
    # Contar total antes da paginação
    total = query.count()
    
    # Aplicar paginação e ordenação
    atendimentos = query.order_by(Atendimento.data_hora.desc()).offset(skip).limit(limit).all()
    
    # Converter modelos para schemas antes de retornar
    atendimentos_schemas = [AtendimentoSchema.model_validate(atendimento) for atendimento in atendimentos]
    
    return AtendimentoList(atendimentos=atendimentos_schemas, total=total)

@router.get("/atendimentos/{atendimento_id}", response_model=AtendimentoSchema)
async def obter_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    """
    Obtém um atendimento específico por ID
    """
    atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    
    return atendimento

@router.post("/atendimentos", response_model=AtendimentoSchema, status_code=201)
async def criar_atendimento(atendimento: AtendimentoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo atendimento com múltiplos procedimentos
    """
    # Verificar se cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == atendimento.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verificar se todos os procedimentos existem
    for proc_data in atendimento.procedimentos:
        procedimento = db.query(Procedimento).filter(Procedimento.id == proc_data.procedimento_id).first()
        if not procedimento:
            raise HTTPException(status_code=404, detail=f"Procedimento ID {proc_data.procedimento_id} não encontrado")
    
    # Criar atendimento
    db_atendimento = Atendimento(
        cliente_id=atendimento.cliente_id,
        data_hora=atendimento.data_hora,
        valor_cobrado=atendimento.valor_cobrado,
        observacoes=atendimento.observacoes,
        status=atendimento.status
    )
    
    db.add(db_atendimento)
    db.flush()  # Para obter o ID do atendimento
    
    # Processar procedimentos
    for proc_data in atendimento.procedimentos:
        atendimento_procedimento = AtendimentoProcedimento(
            atendimento_id=db_atendimento.id,
            procedimento_id=proc_data.procedimento_id,
            valor_cobrado=proc_data.valor_cobrado,
            observacoes=proc_data.observacoes
        )
        db.add(atendimento_procedimento)
    
    # Processar materiais utilizados
    if atendimento.materiais_utilizados:
        for material_data in atendimento.materiais_utilizados:
            # Verificar se material existe
            material = db.query(Material).filter(Material.id == material_data.material_id).first()
            if not material:
                raise HTTPException(status_code=404, detail=f"Material ID {material_data.material_id} não encontrado")
            
            # Verificar estoque
            quantidade_atual = float(material.quantidade_disponivel)
            quantidade_solicitada = float(material_data.quantidade_utilizada)
            if quantidade_atual < quantidade_solicitada:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Estoque insuficiente para {material.nome}. Disponível: {quantidade_atual}"
                )
            
            # Criar registro de material utilizado
            atendimento_material = AtendimentoMaterial(
                atendimento_id=db_atendimento.id,
                material_id=material_data.material_id,
                quantidade_utilizada=material_data.quantidade_utilizada,
                valor_unitario_momento=material_data.valor_unitario_momento
            )
            
            db.add(atendimento_material)
            
            # Baixar do estoque
            material.quantidade_disponivel = float(quantidade_atual - quantidade_solicitada)
    
    db.commit()
    db.refresh(db_atendimento)
    
    return db_atendimento

@router.put("/atendimentos/{atendimento_id}", response_model=AtendimentoSchema)
async def atualizar_atendimento(
    atendimento_id: int, 
    atendimento_update: AtendimentoUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza um atendimento existente
    """
    db_atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if not db_atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    
    # Atualizar campos
    update_data = atendimento_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_atendimento, field, value)
    
    db.commit()
    db.refresh(db_atendimento)
    
    return db_atendimento

@router.delete("/atendimentos/{atendimento_id}", status_code=204)
async def remover_atendimento(atendimento_id: int, db: Session = Depends(get_db)):
    """
    Remove um atendimento
    """
    atendimento = db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()
    if not atendimento:
        raise HTTPException(status_code=404, detail="Atendimento não encontrado")
    
    # Remover procedimentos primeiro
    db.query(AtendimentoProcedimento).filter(AtendimentoProcedimento.atendimento_id == atendimento_id).delete()
    
    # Remover materiais utilizados
    db.query(AtendimentoMaterial).filter(AtendimentoMaterial.atendimento_id == atendimento_id).delete()
    
    # Remover atendimento
    db.delete(atendimento)
    db.commit()
    
    return None

@router.get("/atendimentos/estatisticas/resumo")
async def obter_estatisticas_atendimentos(db: Session = Depends(get_db)):
    """
    Obtém estatísticas resumidas dos atendimentos
    """
    total_atendimentos = db.query(Atendimento).count()
    atendimentos_hoje = db.query(Atendimento).filter(
        Atendimento.data_hora >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    
    atendimentos_mes = db.query(Atendimento).filter(
        Atendimento.data_hora >= datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ).count()
    
    valor_total_mes = db.query(func.sum(Atendimento.valor_cobrado)).filter(
        Atendimento.data_hora >= datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ).scalar() or 0.0
    
    return {
        "total_atendimentos": total_atendimentos,
        "atendimentos_hoje": atendimentos_hoje,
        "atendimentos_mes": atendimentos_mes,
        "valor_total_mes": valor_total_mes
    }

@router.get("/procedimentos/{procedimento_id}/materiais-padrao", response_model=List[ProcedimentoMaterialSchema])
async def obter_materiais_padrao_procedimento(procedimento_id: int, db: Session = Depends(get_db)):
    """
    Obtém os materiais padrão de um procedimento
    """
    # Verificar se o procedimento existe
    procedimento = db.query(Procedimento).filter(Procedimento.id == procedimento_id).first()
    if not procedimento:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    
    # Buscar materiais padrão
    materiais_padrao = db.query(ProcedimentoMaterialModel).filter(
        ProcedimentoMaterialModel.procedimento_id == procedimento_id
    ).all()
    
    # Converter para schemas
    return [ProcedimentoMaterialSchema.model_validate(mp) for mp in materiais_padrao] 