"""
Rotas para gerenciamento de materiais/estoque
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Material
from app.schemas import MaterialCreate, MaterialUpdate, Material as MaterialSchema, MaterialList
from app.utils.material_normalizer import encontrar_materiais_similares, normalizar_nome

router = APIRouter()

@router.get("/materiais", response_model=MaterialList)
async def listar_materiais(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    estoque_baixo: Optional[bool] = Query(None, description="Filtrar por estoque baixo"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os materiais
    """
    query = db.query(Material)
    
    if ativo is not None:
        query = query.filter(Material.ativo == ativo)
    
    if estoque_baixo is not None:
        if estoque_baixo:
            query = query.filter(Material.quantidade_disponivel <= Material.estoque_minimo)
        else:
            query = query.filter(Material.quantidade_disponivel > Material.estoque_minimo)
    
    total = query.count()
    materiais = query.offset(skip).limit(limit).all()
    
    # Converter os objetos do modelo para schemas
    materiais_schemas = [MaterialSchema.model_validate(material) for material in materiais]
    
    return MaterialList(materiais=materiais_schemas, total=total)

@router.get("/materiais/{material_id}", response_model=MaterialSchema)
async def obter_material(material_id: int, db: Session = Depends(get_db)):
    """
    Obtém um material específico por ID
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    return material

@router.post("/materiais", response_model=MaterialSchema, status_code=201)
async def criar_material(material: MaterialCreate, db: Session = Depends(get_db)):
    """
    Cria um novo material
    """
    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    
    return db_material

@router.put("/materiais/{material_id}", response_model=MaterialSchema)
async def atualizar_material(
    material_id: int, 
    material_update: MaterialUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza um material existente
    """
    db_material = db.query(Material).filter(Material.id == material_id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    update_data = material_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_material, field, value)
    
    db.commit()
    db.refresh(db_material)
    
    return db_material

@router.delete("/materiais/{material_id}", status_code=204)
async def remover_material(material_id: int, db: Session = Depends(get_db)):
    """
    Remove um material
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    db.delete(material)
    db.commit()
    
    return None

@router.post("/materiais/{material_id}/ajustar-estoque")
async def ajustar_estoque(
    material_id: int,
    quantidade: float,
    tipo: str = Query(..., regex="^(entrada|saida)$", description="Tipo de ajuste: entrada ou saida"),
    db: Session = Depends(get_db)
):
    """
    Ajusta o estoque de um material (entrada ou saída)
    """
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    
    if tipo == "entrada":
        material.quantidade_disponivel = material.quantidade_disponivel + quantidade
    elif tipo == "saida":
        if material.quantidade_disponivel < quantidade:
            raise HTTPException(
                status_code=400, 
                detail=f"Estoque insuficiente. Disponível: {material.quantidade_disponivel}"
            )
        material.quantidade_disponivel -= quantidade
    
    db.commit()
    db.refresh(material)
    
    return {
        "message": f"Estoque ajustado com sucesso. Nova quantidade: {material.quantidade_disponivel}",
        "quantidade_atual": material.quantidade_disponivel
    }

@router.get("/materiais/estoque/baixo")
async def listar_estoque_baixo(db: Session = Depends(get_db)):
    """
    Lista materiais com estoque baixo
    """
    materiais = db.query(Material).filter(
        Material.quantidade_disponivel <= Material.estoque_minimo,
        Material.ativo == True
    ).all()
    
    materiais_schemas = [MaterialSchema.model_validate(m) for m in materiais]
    
    return {
        "materiais": materiais_schemas,
        "total": len(materiais_schemas)
    }

@router.get("/materiais/buscar/similares")
async def buscar_materiais_similares(
    nome: str = Query(..., description="Nome do material para buscar similares"),
    threshold: float = Query(0.8, ge=0.0, le=1.0, description="Limite de similaridade"),
    db: Session = Depends(get_db)
):
    """
    Busca materiais similares ao nome fornecido
    """
    # Buscar todos os materiais ativos
    materiais = db.query(Material).filter(Material.ativo == True).all()
    
    # Converter para dicionários
    materiais_dict = [
        {
            'id': m.id,
            'nome': m.nome,
            'descricao': m.descricao,
            'quantidade_disponivel': m.quantidade_disponivel,
            'unidade': m.unidade,
            'valor_unitario': m.valor_unitario,
            'estoque_minimo': m.estoque_minimo,
            'ativo': m.ativo
        }
        for m in materiais
    ]
    
    # Encontrar similares
    similares = encontrar_materiais_similares(nome, materiais_dict, threshold)
    
    return {
        "nome_buscado": nome,
        "threshold": threshold,
        "materiais_similares": similares,
        "total_encontrado": len(similares)
    }

@router.post("/materiais/criar-ou-buscar", response_model=MaterialSchema)
async def criar_ou_buscar_material(
    nome: str = Query(..., description="Nome do material"),
    descricao: Optional[str] = Query(None, description="Descrição do material"),
    quantidade_disponivel: float = Query(0.0, ge=0.0, description="Quantidade a somar"),
    unidade: str = Query("un", description="Unidade de medida"),
    valor_unitario: float = Query(0.0, ge=0.0, description="Valor unitário"),
    estoque_minimo: float = Query(0.0, ge=0.0, description="Estoque mínimo"),
    db: Session = Depends(get_db)
):
    """
    Cria um novo material ou soma a quantidade ao material similar existente
    """
    materiais = db.query(Material).filter(Material.ativo == True).all()
    materiais_dict = [
        {
            'id': m.id,
            'nome': m.nome,
            'descricao': m.descricao,
            'quantidade_disponivel': m.quantidade_disponivel,
            'unidade': m.unidade,
            'valor_unitario': m.valor_unitario,
            'estoque_minimo': m.estoque_minimo,
            'ativo': m.ativo
        }
        for m in materiais
    ]
    similares = encontrar_materiais_similares(nome, materiais_dict, threshold=0.9)
    if similares:
        # Se encontrou material muito similar, apenas soma a quantidade ao estoque
        material_similar = similares[0]
        db_material = db.query(Material).filter(Material.id == material_similar['id']).first()
        if db_material:
            db_material.quantidade_disponivel += quantidade_disponivel
            db.commit()
            db.refresh(db_material)
            return MaterialSchema.model_validate(db_material)
    # Se não encontrou similar, criar novo material
    novo_material = Material(
        nome=nome,
        descricao=descricao,
        quantidade_disponivel=quantidade_disponivel,
        unidade=unidade,
        valor_unitario=valor_unitario,
        estoque_minimo=estoque_minimo,
        ativo=True
    )
    db.add(novo_material)
    db.commit()
    db.refresh(novo_material)
    return MaterialSchema.model_validate(novo_material) 