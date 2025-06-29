"""
Rotas para gerenciamento de procedimentos
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Procedimento, ProcedimentoMaterial, Material
from app.schemas import (
    ProcedimentoCreate, ProcedimentoUpdate, Procedimento as ProcedimentoSchema, 
    ProcedimentoList, ProcedimentoMaterialCreate
)

router = APIRouter()

@router.get("/procedimentos/teste")
async def teste_procedimentos(db: Session = Depends(get_db)):
    """
    Endpoint de teste para verificar se o problema é específico
    """
    try:
        count = db.query(Procedimento).count()
        return {"message": "OK", "count": count}
    except Exception as e:
        return {"error": str(e)}

@router.get("/procedimentos", response_model=ProcedimentoList)
async def listar_procedimentos(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os procedimentos
    """
    try:
        query = db.query(Procedimento)
        
        if ativo is not None:
            query = query.filter(Procedimento.ativo == ativo)
        
        total = query.count()
        procedimentos = query.offset(skip).limit(limit).all()
        
        # Converter para schemas
        procedimentos_schemas = []
        for p in procedimentos:
            p_schema = ProcedimentoSchema.model_validate(p)
            procedimentos_schemas.append(p_schema)
        
        return ProcedimentoList(procedimentos=procedimentos_schemas, total=total)
        
    except Exception as e:
        print(f"❌ Erro ao listar procedimentos: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/procedimentos/{procedimento_id}", response_model=ProcedimentoSchema)
async def obter_procedimento(procedimento_id: int, db: Session = Depends(get_db)):
    """
    Obtém um procedimento específico por ID
    """
    procedimento = db.query(Procedimento).filter(Procedimento.id == procedimento_id).first()
    if not procedimento:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    
    return ProcedimentoSchema.model_validate(procedimento)

@router.post("/procedimentos", response_model=ProcedimentoSchema, status_code=201)
async def criar_procedimento(procedimento: ProcedimentoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo procedimento
    """
    print(f"🔍 Criando procedimento: {procedimento.dict()}")
    
    try:
        # Extrair materiais padrão do request
        materiais_padrao = procedimento.materiais_padrao or []
        procedimento_data = procedimento.dict(exclude={'materiais_padrao'})
        
        print(f"📝 Dados do procedimento: {procedimento_data}")
        print(f"📦 Materiais padrão: {materiais_padrao}")
        
        # Criar o procedimento
        db_procedimento = Procedimento(**procedimento_data)
        db.add(db_procedimento)
        db.flush()  # Para obter o ID do procedimento
        
        print(f"✅ Procedimento criado com ID: {db_procedimento.id}")
        
        # Adicionar materiais padrão
        for material_data in materiais_padrao:
            print(f"🔧 Adicionando material padrão: {material_data}")
            db_material = ProcedimentoMaterial(
                procedimento_id=db_procedimento.id,
                **material_data.dict()
            )
            db.add(db_material)
        
        db.commit()
        db.refresh(db_procedimento)
        
        print(f"✅ Procedimento finalizado: {db_procedimento.id}")
        return ProcedimentoSchema.model_validate(db_procedimento)
        
    except Exception as e:
        print(f"❌ Erro ao criar procedimento: {e}")
        import traceback
        traceback.print_exc()
        raise

@router.put("/procedimentos/{procedimento_id}", response_model=ProcedimentoSchema)
async def atualizar_procedimento(
    procedimento_id: int, 
    procedimento_update: ProcedimentoUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza um procedimento existente
    """
    db_procedimento = db.query(Procedimento).filter(Procedimento.id == procedimento_id).first()
    if not db_procedimento:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    
    # Extrair materiais padrão do request
    materiais_padrao = procedimento_update.materiais_padrao
    update_data = procedimento_update.dict(exclude_unset=True, exclude={'materiais_padrao'})
    
    # Atualizar campos do procedimento
    for field, value in update_data.items():
        setattr(db_procedimento, field, value)
    
    # Se materiais padrão foram fornecidos, atualizar
    if materiais_padrao is not None:
        # Remover materiais padrão existentes
        db.query(ProcedimentoMaterial).filter(
            ProcedimentoMaterial.procedimento_id == procedimento_id
        ).delete()
        
        # Adicionar novos materiais padrão
        for material_data in materiais_padrao:
            db_material = ProcedimentoMaterial(
                procedimento_id=procedimento_id,
                **material_data.dict()
            )
            db.add(db_material)
    
    db.commit()
    db.refresh(db_procedimento)
    
    return ProcedimentoSchema.model_validate(db_procedimento)

@router.delete("/procedimentos/{procedimento_id}", status_code=204)
async def remover_procedimento(procedimento_id: int, db: Session = Depends(get_db)):
    """
    Remove um procedimento
    """
    procedimento = db.query(Procedimento).filter(Procedimento.id == procedimento_id).first()
    if not procedimento:
        raise HTTPException(status_code=404, detail="Procedimento não encontrado")
    
    db.delete(procedimento)
    db.commit()
    
    return None 