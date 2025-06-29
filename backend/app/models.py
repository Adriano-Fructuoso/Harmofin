"""
Modelos SQLAlchemy para o sistema de gestão de clientes
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Cliente(Base):
    """
    Modelo para a tabela de clientes
    """
    __tablename__ = "clientes"
    
    # Campos da tabela
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    observacao = Column(Text, nullable=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com atendimentos
    atendimentos = relationship("Atendimento", back_populates="cliente")

    def __repr__(self):
        """Representação string do objeto"""
        return f"<Cliente(id={self.id}, nome='{self.nome}', telefone='{self.telefone}')>"

class Procedimento(Base):
    """Modelo para procedimentos realizados"""
    __tablename__ = "procedimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    valor_padrao = Column(Float, nullable=False, default=0.0)
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    atendimentos = relationship("AtendimentoProcedimento", back_populates="procedimento")
    materiais_padrao = relationship("ProcedimentoMaterial", back_populates="procedimento")

class Material(Base):
    """Modelo para materiais/insumos"""
    __tablename__ = "materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    quantidade_disponivel = Column(Float, nullable=False, default=0.0)
    unidade = Column(String(20), nullable=False, default="un")
    valor_unitario = Column(Float, nullable=False, default=0.0)
    estoque_minimo = Column(Float, nullable=False, default=0.0)
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com atendimentos
    atendimento_materiais = relationship("AtendimentoMaterial", back_populates="material")

class Atendimento(Base):
    """Modelo para atendimentos realizados"""
    __tablename__ = "atendimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_hora = Column(DateTime, nullable=False, default=datetime.utcnow)
    valor_cobrado = Column(Float, nullable=False)
    observacoes = Column(Text, nullable=True)
    status = Column(String(20), default="realizado")  # realizado, cancelado, reagendado
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("Cliente", back_populates="atendimentos")
    procedimentos = relationship("AtendimentoProcedimento", back_populates="atendimento")
    materiais_utilizados = relationship("AtendimentoMaterial", back_populates="atendimento")

class AtendimentoProcedimento(Base):
    """Modelo para relacionamento entre atendimentos e procedimentos realizados"""
    __tablename__ = "atendimento_procedimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False)
    procedimento_id = Column(Integer, ForeignKey("procedimentos.id"), nullable=False)
    valor_cobrado = Column(Float, nullable=False)  # Valor específico para este procedimento
    observacoes = Column(Text, nullable=True)  # Observações específicas do procedimento
    
    # Relacionamentos
    atendimento = relationship("Atendimento", back_populates="procedimentos")
    procedimento = relationship("Procedimento", back_populates="atendimentos")

class AtendimentoMaterial(Base):
    """Modelo para relacionamento entre atendimentos e materiais utilizados"""
    __tablename__ = "atendimento_materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    quantidade_utilizada = Column(Float, nullable=False)
    valor_unitario_momento = Column(Float, nullable=False)  # Valor no momento do uso
    
    # Relacionamentos
    atendimento = relationship("Atendimento", back_populates="materiais_utilizados")
    material = relationship("Material", back_populates="atendimento_materiais")

class ProcedimentoMaterial(Base):
    """Modelo para relacionamento entre procedimentos e seus materiais padrão"""
    __tablename__ = "procedimento_materiais"
    
    id = Column(Integer, primary_key=True, index=True)
    procedimento_id = Column(Integer, ForeignKey("procedimentos.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materiais.id"), nullable=False)
    quantidade_padrao = Column(Float, nullable=False, default=1.0)  # Quantidade média de uso
    
    # Relacionamentos
    procedimento = relationship("Procedimento", back_populates="materiais_padrao")
    material = relationship("Material") 