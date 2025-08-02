"""
Gerenciador de banco de dados usando SQLAlchemy.
"""
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from config import get_config

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gerenciador de banco de dados usando SQLAlchemy.
    
    Esta classe gerencia a conexão com o banco de dados e fornece
    métodos para criar sessões e gerenciar transações.
    """
    
    def __init__(self, database_url: str, echo: bool = False):
        """
        Inicializa o gerenciador de banco de dados.
        
        Args:
            database_url: URL de conexão com o banco
            echo: Se deve mostrar as queries SQL no console
        """
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._setup_engine(echo)
    
    def _setup_engine(self, echo: bool) -> None:
        """
        Configura o engine do SQLAlchemy.
        
        Args:
            echo: Se deve mostrar as queries SQL
        """
        try:
            self.engine = create_engine(
                self.database_url,
                echo=echo,
                pool_pre_ping=True,  # Verifica conexão antes de usar
                pool_recycle=3600,   # Recicla conexões a cada hora
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            logger.info(f"Engine SQLAlchemy configurado para: {self.database_url}")
        except Exception as e:
            logger.error(f"Erro ao configurar engine: {e}")
            raise
    
    def create_tables(self) -> None:
        """
        Cria todas as tabelas definidas nos modelos.
        """
        try:
            from .venda import Base
            Base.metadata.create_all(bind=self.engine)
            logger.info("Tabelas criadas com sucesso")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            raise
    
    def get_session(self) -> Session:
        """
        Retorna uma nova sessão do banco de dados.
        
        Returns:
            Session: Sessão do SQLAlchemy
            
        Raises:
            SQLAlchemyError: Se houver erro ao criar a sessão
        """
        try:
            session = self.SessionLocal()
            return session
        except SQLAlchemyError as e:
            logger.error(f"Erro ao criar sessão: {e}")
            raise
    
    def close_session(self, session: Session) -> None:
        """
        Fecha uma sessão do banco de dados.
        
        Args:
            session: Sessão a ser fechada
        """
        try:
            if session:
                session.close()
        except Exception as e:
            logger.error(f"Erro ao fechar sessão: {e}")
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o banco de dados.
        
        Returns:
            bool: True se a conexão estiver funcionando
        """
        try:
            with self.engine.connect() as connection:
                connection.execute("SELECT 1")
            logger.info("Conexão com banco de dados testada com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {e}")
            return False
    
    def get_database_info(self) -> dict:
        """
        Retorna informações sobre o banco de dados.
        
        Returns:
            dict: Informações do banco
        """
        try:
            with self.engine.connect() as connection:
                # Para SQLite
                if 'sqlite' in self.database_url:
                    result = connection.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                    table_count = result.scalar()
                    
                    result = connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = [row[0] for row in result.fetchall()]
                    
                    return {
                        'type': 'SQLite',
                        'url': self.database_url,
                        'table_count': table_count,
                        'tables': tables
                    }
                else:
                    return {
                        'type': 'Unknown',
                        'url': self.database_url,
                        'error': 'Database type not supported for info'
                    }
        except Exception as e:
            logger.error(f"Erro ao obter informações do banco: {e}")
            return {
                'type': 'Error',
                'url': self.database_url,
                'error': str(e)
            }


# Instância global do gerenciador de banco
config = get_config()
db_manager = DatabaseManager(
    database_url=config['database']['url'],
    echo=config['database']['echo']
)


def get_db_session() -> Session:
    """
    Função helper para obter uma sessão do banco.
    
    Returns:
        Session: Sessão do banco de dados
    """
    return db_manager.get_session()


def init_database() -> None:
    """
    Inicializa o banco de dados criando as tabelas.
    """
    try:
        db_manager.create_tables()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        raise 