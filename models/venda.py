"""
Modelo de dados para Venda usando SQLAlchemy ORM.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

Base = declarative_base()
logger = logging.getLogger(__name__)


class Venda(Base):
    """
    Modelo de dados para representar uma venda.
    
    Attributes:
        id (int): Identificador único da venda
        nome (str): Nome do produto vendido
        preco (float): Preço unitário do produto
        quantidade (int): Quantidade vendida
        data_venda (datetime): Data e hora da venda
        observacoes (str): Observações adicionais sobre a venda
    """
    
    __tablename__ = 'vendas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, index=True)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    data_venda = Column(DateTime, default=datetime.now, nullable=False)
    observacoes = Column(Text, nullable=True)
    
    def __init__(self, nome: str, preco: float, quantidade: int, 
                 observacoes: Optional[str] = None, id: Optional[int] = None):
        """
        Inicializa uma nova instância de Venda.
        
        Args:
            nome: Nome do produto
            preco: Preço unitário
            quantidade: Quantidade vendida
            observacoes: Observações opcionais
            id: ID opcional (usado para carregar dados existentes)
        """
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.observacoes = observacoes
        if id:
            self.id = id
    
    def calcular_faturamento(self) -> float:
        """
        Calcula o faturamento total desta venda.
        
        Returns:
            float: Faturamento total (preço * quantidade)
        """
        return self.preco * self.quantidade
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a venda para um dicionário.
        
        Returns:
            Dict[str, Any]: Dicionário com os dados da venda
        """
        return {
            'id': self.id,
            'nome': self.nome,
            'preco': self.preco,
            'quantidade': self.quantidade,
            'data_venda': self.data_venda.isoformat() if self.data_venda else None,
            'observacoes': self.observacoes,
            'faturamento': self.calcular_faturamento()
        }
    
    def __str__(self) -> str:
        """Representação string da venda."""
        return (f"Venda(id={self.id}, produto='{self.nome}', "
                f"preço=R${self.preco:.2f}, quantidade={self.quantidade})")
    
    def __repr__(self) -> str:
        """Representação detalhada da venda."""
        return (f"Venda(id={self.id}, nome='{self.nome}', preco={self.preco}, "
                f"quantidade={self.quantidade}, data_venda={self.data_venda}, "
                f"observacoes='{self.observacoes}')")
    
    @classmethod
    def criar_venda(cls, session: Session, nome: str, preco: float, 
                    quantidade: int, observacoes: Optional[str] = None) -> 'Venda':
        """
        Cria e salva uma nova venda no banco de dados.
        
        Args:
            session: Sessão do SQLAlchemy
            nome: Nome do produto
            preco: Preço unitário
            quantidade: Quantidade vendida
            observacoes: Observações opcionais
            
        Returns:
            Venda: Instância da venda criada
            
        Raises:
            SQLAlchemyError: Se houver erro ao salvar no banco
        """
        try:
            venda = cls(nome=nome, preco=preco, quantidade=quantidade, 
                       observacoes=observacoes)
            session.add(venda)
            session.commit()
            session.refresh(venda)
            logger.info(f"Venda criada com sucesso: {venda}")
            return venda
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao criar venda: {e}")
            raise
    
    @classmethod
    def buscar_por_id(cls, session: Session, venda_id: int) -> Optional['Venda']:
        """
        Busca uma venda pelo ID.
        
        Args:
            session: Sessão do SQLAlchemy
            venda_id: ID da venda
            
        Returns:
            Optional[Venda]: Venda encontrada ou None
        """
        return session.query(cls).filter(cls.id == venda_id).first()
    
    @classmethod
    def buscar_por_nome(cls, session: Session, nome: str) -> list['Venda']:
        """
        Busca vendas pelo nome do produto.
        
        Args:
            session: Sessão do SQLAlchemy
            nome: Nome do produto
            
        Returns:
            list[Venda]: Lista de vendas encontradas
        """
        return session.query(cls).filter(cls.nome.ilike(f"%{nome}%")).all()
    
    @classmethod
    def listar_todas(cls, session: Session) -> list['Venda']:
        """
        Lista todas as vendas ordenadas por data.
        
        Args:
            session: Sessão do SQLAlchemy
            
        Returns:
            list[Venda]: Lista de todas as vendas
        """
        return session.query(cls).order_by(cls.data_venda.desc()).all()
    
    def atualizar(self, session: Session, nome: Optional[str] = None,
                  preco: Optional[float] = None, quantidade: Optional[int] = None,
                  observacoes: Optional[str] = None) -> bool:
        """
        Atualiza os dados da venda.
        
        Args:
            session: Sessão do SQLAlchemy
            nome: Novo nome (opcional)
            preco: Novo preço (opcional)
            quantidade: Nova quantidade (opcional)
            observacoes: Novas observações (opcional)
            
        Returns:
            bool: True se atualizado com sucesso
            
        Raises:
            SQLAlchemyError: Se houver erro ao atualizar
        """
        try:
            if nome is not None:
                self.nome = nome
            if preco is not None:
                self.preco = preco
            if quantidade is not None:
                self.quantidade = quantidade
            if observacoes is not None:
                self.observacoes = observacoes
            
            session.commit()
            logger.info(f"Venda atualizada com sucesso: {self}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao atualizar venda: {e}")
            raise
    
    def deletar(self, session: Session) -> bool:
        """
        Remove a venda do banco de dados.
        
        Args:
            session: Sessão do SQLAlchemy
            
        Returns:
            bool: True se removido com sucesso
            
        Raises:
            SQLAlchemyError: Se houver erro ao deletar
        """
        try:
            session.delete(self)
            session.commit()
            logger.info(f"Venda removida com sucesso: {self}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erro ao deletar venda: {e}")
            raise 