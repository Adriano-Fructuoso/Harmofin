"""
Schemas Pydantic para validação de dados
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Sequence, TYPE_CHECKING
from datetime import datetime

# Schemas para Clientes
class ClienteBase(BaseModel):
    """
    Schema base para cliente com campos comuns
    """
    nome: str
    telefone: str
    email: Optional[str] = None
    observacao: Optional[str] = None

class ClienteCreate(ClienteBase):
    """
    Schema para criação de cliente
    """
    pass

class ClienteUpdate(ClienteBase):
    """
    Schema para atualização de cliente (todos os campos opcionais)
    """
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    observacao: Optional[str] = None

class Cliente(ClienteBase):
    id: int
    data_cadastro: datetime
    
    class Config:
        """Configuração para permitir conversão de ORM para dict"""
        from_attributes = True

class ClienteListResponse(BaseModel):
    """
    Schema para resposta de lista de clientes
    """
    clientes: Sequence[Cliente]
    total: int

class ErrorResponse(BaseModel):
    """
    Schema para respostas de erro
    """
    detail: str 

# Schemas para Procedimentos
class ProcedimentoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    valor_padrao: float
    ativo: bool = True

# Schemas para Materiais Padrão dos Procedimentos (definir antes de ProcedimentoCreate)
class ProcedimentoMaterialBase(BaseModel):
    material_id: int
    quantidade_padrao: float = 1.0

class ProcedimentoMaterialCreate(ProcedimentoMaterialBase):
    pass

class ProcedimentoMaterialUpdate(ProcedimentoMaterialBase):
    quantidade_padrao: Optional[float] = None

class ProcedimentoMaterial(ProcedimentoMaterialBase):
    id: int
    material: Optional['Material'] = None
    
    class Config:
        from_attributes = True

class ProcedimentoCreate(ProcedimentoBase):
    materiais_padrao: Optional[List[ProcedimentoMaterialCreate]] = None

class ProcedimentoUpdate(ProcedimentoBase):
    nome: Optional[str] = None
    valor_padrao: Optional[float] = None
    ativo: Optional[bool] = None
    materiais_padrao: Optional[List[ProcedimentoMaterialCreate]] = None

class Procedimento(ProcedimentoBase):
    id: int
    data_cadastro: datetime
    materiais_padrao: List[ProcedimentoMaterial] = []
    
    class Config:
        from_attributes = True

class ProcedimentoList(BaseModel):
    procedimentos: List[Procedimento]
    total: int

# Schemas para Materiais
class MaterialBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    quantidade_disponivel: float
    unidade: str = "un"
    valor_unitario: float
    estoque_minimo: float = 0.0
    ativo: bool = True

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    nome: Optional[str] = None
    quantidade_disponivel: Optional[float] = None
    valor_unitario: Optional[float] = None
    ativo: Optional[bool] = None

class Material(MaterialBase):
    id: int
    data_cadastro: datetime
    
    class Config:
        from_attributes = True

class MaterialList(BaseModel):
    materiais: List[Material]
    total: int

# Schemas para Atendimentos
class AtendimentoProcedimentoBase(BaseModel):
    procedimento_id: int
    valor_cobrado: float
    observacoes: Optional[str] = None

class AtendimentoProcedimentoCreate(AtendimentoProcedimentoBase):
    pass

class AtendimentoProcedimento(AtendimentoProcedimentoBase):
    id: int
    procedimento: Procedimento
    
    class Config:
        from_attributes = True

class AtendimentoMaterialBase(BaseModel):
    material_id: int
    quantidade_utilizada: float
    valor_unitario_momento: float

class AtendimentoMaterialCreate(AtendimentoMaterialBase):
    pass

class AtendimentoMaterial(AtendimentoMaterialBase):
    id: int
    material: Material
    
    class Config:
        from_attributes = True

class AtendimentoBase(BaseModel):
    cliente_id: int
    data_hora: datetime
    valor_cobrado: float
    observacoes: Optional[str] = None
    status: str = "realizado"

class AtendimentoCreate(AtendimentoBase):
    procedimentos: List[AtendimentoProcedimentoCreate]
    materiais_utilizados: Optional[List[AtendimentoMaterialCreate]] = None

class AtendimentoUpdate(BaseModel):
    cliente_id: Optional[int] = None
    data_hora: Optional[datetime] = None
    valor_cobrado: Optional[float] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None

class Atendimento(AtendimentoBase):
    id: int
    data_cadastro: datetime
    cliente: Cliente
    procedimentos: List[AtendimentoProcedimento] = []
    materiais_utilizados: List[AtendimentoMaterial] = []
    
    class Config:
        from_attributes = True

class AtendimentoList(BaseModel):
    atendimentos: List[Atendimento]
    total: int

# Schemas para filtros
class AtendimentoFiltro(BaseModel):
    cliente_id: Optional[int] = None
    procedimento_id: Optional[int] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    status: Optional[str] = None 

# Adicionar referência para Material no final do arquivo para evitar problemas de importação circular
if TYPE_CHECKING:
    from .schemas import Material 