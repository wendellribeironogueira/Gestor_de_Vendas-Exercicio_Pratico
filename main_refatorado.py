"""
Sistema de Gestão de Vendas - Versão Refatorada

Este é o arquivo principal do sistema refatorado, que implementa:
- Programação Orientada a Objetos (POO)
- Persistência de dados com SQLAlchemy
- Interface gráfica moderna com Tkinter
- Arquitetura MVC (Model-View-Controller)
- Logging e tratamento de erros
- Configurações centralizadas
"""
import sys
import logging
import os
from pathlib import Path
from datetime import datetime

# Adicionar o diretório raiz ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from models.database import init_database
from gui.main_window import MainWindow


def setup_logging():
    """
    Configura o sistema de logging.
    """
    config = get_config()
    log_config = config['logging']
    
    # Criar diretório de logs se não existir
    logs_dir = Path(config['paths']['logs_dir'])
    logs_dir.mkdir(exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, log_config['level']),
        format=log_config['format'],
        handlers=[
            logging.FileHandler(logs_dir / log_config['file'], encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Sistema de logging configurado")
    return logger


def check_dependencies():
    """
    Verifica se todas as dependências estão disponíveis.
    """
    required_packages = [
        'sqlalchemy',
        'matplotlib',
        'seaborn',
        'pandas',
        'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Dependências faltando:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPara instalar as dependências, execute:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def initialize_database():
    """
    Inicializa o banco de dados.
    """
    try:
        init_database()
        logger.info("Banco de dados inicializado com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados: {e}")
        return False


def create_sample_data():
    """
    Cria dados de exemplo se o banco estiver vazio.
    """
    try:
        from services.venda_service import VendaService
        
        with VendaService() as service:
            vendas = service.listar_todas()
            
            if not vendas:
                logger.info("Criando dados de exemplo...")
                
                # Dados de exemplo
                sample_vendas = [
                    {"nome": "Camisa Básica", "preco": 29.90, "quantidade": 10, "observacoes": "Venda promocional"},
                    {"nome": "Calça Jeans", "preco": 89.90, "quantidade": 5, "observacoes": "Coleção nova"},
                    {"nome": "Tênis Esportivo", "preco": 159.90, "quantidade": 8, "observacoes": "Marca premium"},
                    {"nome": "Boné", "preco": 19.90, "quantidade": 15, "observacoes": "Acessório"},
                    {"nome": "Mochila", "preco": 79.90, "quantidade": 3, "observacoes": "Escolar"},
                    {"nome": "Relógio", "preco": 299.90, "quantidade": 2, "observacoes": "Luxo"},
                    {"nome": "Óculos", "preco": 129.90, "quantidade": 7, "observacoes": "Solar"},
                    {"nome": "Cinto", "preco": 39.90, "quantidade": 12, "observacoes": "Couro legítimo"}
                ]
                
                for venda_data in sample_vendas:
                    service.criar_venda(**venda_data)
                
                logger.info(f"Criados {len(sample_vendas)} registros de exemplo")
            else:
                logger.info(f"Banco já possui {len(vendas)} registros")
                
    except Exception as e:
        logger.error(f"Erro ao criar dados de exemplo: {e}")


def main():
    """
    Função principal da aplicação.
    """
    global logger
    
    try:
        # Configurar logging
        logger = setup_logging()
        logger.info("=" * 50)
        logger.info("Iniciando Sistema de Gestão de Vendas")
        logger.info(f"Versão: 2.0")
        logger.info(f"Data/Hora: {datetime.now()}")
        logger.info("=" * 50)
        
        # Verificar dependências
        logger.info("Verificando dependências...")
        if not check_dependencies():
            logger.error("Dependências não atendidas. Encerrando aplicação.")
            return 1
        
        # Obter configurações
        config = get_config()
        logger.info("Configurações carregadas")
        
        # Inicializar banco de dados
        logger.info("Inicializando banco de dados...")
        if not initialize_database():
            logger.error("Falha ao inicializar banco de dados. Encerrando aplicação.")
            return 1
        
        # Criar dados de exemplo (se necessário)
        create_sample_data()
        
        # Iniciar interface gráfica
        logger.info("Iniciando interface gráfica...")
        app = MainWindow()
        
        logger.info("Aplicação iniciada com sucesso")
        app.run()
        
        logger.info("Aplicação encerrada normalmente")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Aplicação interrompida pelo usuário")
        return 0
    except Exception as e:
        logger.error(f"Erro crítico na aplicação: {e}")
        print(f"❌ Erro crítico: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 