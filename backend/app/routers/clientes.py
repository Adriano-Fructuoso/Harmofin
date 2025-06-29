"""
Router para endpoints de gestão de clientes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.database import get_db
from app.models import Cliente as ClienteModel
from app.schemas import (
    ClienteCreate, 
    ClienteUpdate, 
    Cliente, 
    ClienteListResponse
)

# Criar router para clientes
router = APIRouter()

@router.post("/clientes", response_model=Cliente, status_code=201)
async def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Cadastrar novo cliente
    
    Args:
        cliente: Dados do cliente a ser criado
        db: Sessão do banco de dados
    
    Returns:
        Cliente: Cliente criado com ID
    """
    # Criar novo cliente
    db_cliente = ClienteModel(
        nome=cliente.nome,
        telefone=cliente.telefone,
        email=cliente.email,
        observacao=cliente.observacao
    )
    
    # Salvar no banco
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente

@router.get("/clientes", response_model=ClienteListResponse)
async def listar_clientes(
    db: Session = Depends(get_db)
):
    """
    Listar todos os clientes ordenados por nome
    
    Args:
        db: Sessão do banco de dados
    
    Returns:
        ClienteListResponse: Lista de clientes e total
    """
    # Buscar todos os clientes ordenados por nome
    clientes = db.query(ClienteModel).order_by(ClienteModel.nome).all()
    
    return ClienteListResponse(
        clientes=clientes,
        total=len(clientes)
    )

@router.get("/clientes/busca", response_model=ClienteListResponse)
async def buscar_clientes(
    termo: str = Query(..., description="Termo de busca (nome ou telefone)"),
    db: Session = Depends(get_db)
):
    """
    Buscar clientes por nome ou telefone
    """
    clientes = db.query(ClienteModel).filter(
        or_(
            ClienteModel.nome.ilike(f"%{termo}%"),
            ClienteModel.telefone.ilike(f"%{termo}%")
        )
    ).order_by(ClienteModel.nome).all()
    return ClienteListResponse(
        clientes=clientes,
        total=len(clientes)
    )

@router.get("/clientes/{cliente_id}", response_model=Cliente)
async def buscar_cliente_por_id(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Buscar cliente por ID
    
    Args:
        cliente_id: ID do cliente
        db: Sessão do banco de dados
    
    Returns:
        Cliente: Dados do cliente
    
    Raises:
        HTTPException: Se cliente não encontrado
    """
    # Buscar cliente por ID
    cliente = db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    return cliente

@router.put("/clientes/{cliente_id}", response_model=Cliente)
async def editar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Editar dados do cliente
    
    Args:
        cliente_id: ID do cliente
        cliente_update: Dados para atualização
        db: Sessão do banco de dados
    
    Returns:
        Cliente: Cliente atualizado
    
    Raises:
        HTTPException: Se cliente não encontrado
    """
    # Buscar cliente por ID
    db_cliente = db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
    
    if not db_cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Atualizar apenas os campos fornecidos
    update_data = cliente_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_cliente, field, value)
    
    # Salvar alterações
    db.commit()
    db.refresh(db_cliente)
    
    return db_cliente

@router.delete("/clientes/{cliente_id}", status_code=204)
async def remover_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Remover cliente
    
    Args:
        cliente_id: ID do cliente
        db: Sessão do banco de dados
    
    Raises:
        HTTPException: Se cliente não encontrado
    """
    # Buscar cliente por ID
    db_cliente = db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()
    
    if not db_cliente:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Remover cliente
    db.delete(db_cliente)
    db.commit()
    
    return None 