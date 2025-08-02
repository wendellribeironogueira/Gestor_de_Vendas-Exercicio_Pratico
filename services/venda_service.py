"""
Serviço de gerenciamento de vendas.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from models.venda import Venda
from models.database import get_db_session

logger = logging.getLogger(__name__)


class VendaService:
    """
    Serviço para gerenciar operações de vendas.
    
    Esta classe encapsula toda a lógica de negócio relacionada
    às vendas, incluindo validações e regras de negócio.
    """
    
    def __init__(self):
        """Inicializa o serviço de vendas."""
        self.session: Optional[Session] = None
    
    def __enter__(self):
        """Context manager entry."""
        self.session = get_db_session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.session:
            self.session.close()
    
    def criar_venda(self, nome: str, preco: float, quantidade: int, 
                   observacoes: Optional[str] = None) -> Venda:
        """
        Cria uma nova venda com validações.
        
        Args:
            nome: Nome do produto
            preco: Preço unitário
            quantidade: Quantidade vendida
            observacoes: Observações opcionais
            
        Returns:
            Venda: Venda criada
            
        Raises:
            ValueError: Se os dados forem inválidos
            SQLAlchemyError: Se houver erro no banco
        """
        # Validações de negócio
        if not nome or not nome.strip():
            raise ValueError("Nome do produto é obrigatório")
        
        if preco <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        if len(nome) > 100:
            raise ValueError("Nome do produto deve ter no máximo 100 caracteres")
        
        try:
            venda = Venda.criar_venda(
                session=self.session,
                nome=nome.strip(),
                preco=preco,
                quantidade=quantidade,
                observacoes=observacoes.strip() if observacoes else None
            )
            logger.info(f"Venda criada: {venda}")
            return venda
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar venda: {e}")
            raise
    
    def buscar_venda(self, venda_id: int) -> Optional[Venda]:
        """
        Busca uma venda pelo ID.
        
        Args:
            venda_id: ID da venda
            
        Returns:
            Optional[Venda]: Venda encontrada ou None
        """
        try:
            return Venda.buscar_por_id(self.session, venda_id)
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar venda {venda_id}: {e}")
            return None
    
    def buscar_por_nome(self, nome: str) -> List[Venda]:
        """
        Busca vendas pelo nome do produto.
        
        Args:
            nome: Nome do produto
            
        Returns:
            List[Venda]: Lista de vendas encontradas
        """
        try:
            return Venda.buscar_por_nome(self.session, nome)
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar vendas por nome '{nome}': {e}")
            return []
    
    def listar_todas(self) -> List[Venda]:
        """
        Lista todas as vendas.
        
        Returns:
            List[Venda]: Lista de todas as vendas
        """
        try:
            return Venda.listar_todas(self.session)
        except SQLAlchemyError as e:
            logger.error(f"Erro ao listar vendas: {e}")
            return []
    
    def atualizar_venda(self, venda_id: int, nome: Optional[str] = None,
                       preco: Optional[float] = None, quantidade: Optional[int] = None,
                       observacoes: Optional[str] = None) -> bool:
        """
        Atualiza uma venda existente.
        
        Args:
            venda_id: ID da venda
            nome: Novo nome (opcional)
            preco: Novo preço (opcional)
            quantidade: Nova quantidade (opcional)
            observacoes: Novas observações (opcional)
            
        Returns:
            bool: True se atualizado com sucesso
            
        Raises:
            ValueError: Se os dados forem inválidos
        """
        venda = self.buscar_venda(venda_id)
        if not venda:
            raise ValueError(f"Venda com ID {venda_id} não encontrada")
        
        # Validações
        if nome is not None and (not nome.strip() or len(nome) > 100):
            raise ValueError("Nome do produto deve ter entre 1 e 100 caracteres")
        
        if preco is not None and preco <= 0:
            raise ValueError("Preço deve ser maior que zero")
        
        if quantidade is not None and quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        try:
            return venda.atualizar(
                session=self.session,
                nome=nome.strip() if nome else None,
                preco=preco,
                quantidade=quantidade,
                observacoes=observacoes.strip() if observacoes else None
            )
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar venda {venda_id}: {e}")
            raise
    
    def deletar_venda(self, venda_id: int) -> bool:
        """
        Remove uma venda.
        
        Args:
            venda_id: ID da venda
            
        Returns:
            bool: True se removido com sucesso
            
        Raises:
            ValueError: Se a venda não for encontrada
        """
        venda = self.buscar_venda(venda_id)
        if not venda:
            raise ValueError(f"Venda com ID {venda_id} não encontrada")
        
        try:
            return venda.deletar(self.session)
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar venda {venda_id}: {e}")
            raise
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais das vendas.
        
        Returns:
            Dict[str, Any]: Estatísticas das vendas
        """
        try:
            vendas = self.listar_todas()
            
            if not vendas:
                return {
                    'total_vendas': 0,
                    'faturamento_total': 0.0,
                    'quantidade_total': 0,
                    'preco_medio': 0.0,
                    'quantidade_media': 0.0
                }
            
            faturamento_total = sum(v.calcular_faturamento() for v in vendas)
            quantidade_total = sum(v.quantidade for v in vendas)
            preco_medio = sum(v.preco for v in vendas) / len(vendas)
            quantidade_media = quantidade_total / len(vendas)
            
            return {
                'total_vendas': len(vendas),
                'faturamento_total': faturamento_total,
                'quantidade_total': quantidade_total,
                'preco_medio': preco_medio,
                'quantidade_media': quantidade_media
            }
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def validar_dados_venda(self, nome: str, preco: float, quantidade: int) -> List[str]:
        """
        Valida os dados de uma venda.
        
        Args:
            nome: Nome do produto
            preco: Preço unitário
            quantidade: Quantidade vendida
            
        Returns:
            List[str]: Lista de erros encontrados
        """
        erros = []
        
        if not nome or not nome.strip():
            erros.append("Nome do produto é obrigatório")
        elif len(nome.strip()) > 100:
            erros.append("Nome do produto deve ter no máximo 100 caracteres")
        
        if preco <= 0:
            erros.append("Preço deve ser maior que zero")
        
        if quantidade <= 0:
            erros.append("Quantidade deve ser maior que zero")
        
        return erros 