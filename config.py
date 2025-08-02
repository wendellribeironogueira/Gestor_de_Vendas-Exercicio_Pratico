"""
Configurações centralizadas do sistema de gestão de vendas.
"""
import os
from pathlib import Path
from typing import Dict, Any

# Configurações do banco de dados
DATABASE_CONFIG = {
    'url': 'sqlite:///vendas.db',
    'echo': False,  # Log SQL queries
}

# Configurações da interface gráfica
GUI_CONFIG = {
    'title': 'Gestor de Vendas - Sistema de Análise',
    'width': 1200,
    'height': 800,
    'theme': 'clam',  # Tema do tkinter
    'font_family': 'Segoe UI',
    'font_size': 10,
}

# Configurações de cores
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#28A745',
    'warning': '#FFC107',
    'danger': '#DC3545',
    'light': '#F8F9FA',
    'dark': '#343A40',
    'white': '#FFFFFF',
    'gray': '#6C757D',
}

# Configurações de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'vendas.log',
}

# Configurações de relatórios
REPORT_CONFIG = {
    'charts_dir': 'charts',
    'reports_dir': 'reports',
    'date_format': '%d/%m/%Y',
    'currency_format': 'R$ {:.2f}',
}

# Diretórios do projeto
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
LOGS_DIR = PROJECT_ROOT / 'logs'
REPORTS_DIR = PROJECT_ROOT / 'reports'
CHARTS_DIR = PROJECT_ROOT / 'charts'

# Criar diretórios se não existirem
for directory in [DATA_DIR, LOGS_DIR, REPORTS_DIR, CHARTS_DIR]:
    directory.mkdir(exist_ok=True)

def get_config() -> Dict[str, Any]:
    """Retorna todas as configurações do sistema."""
    return {
        'database': DATABASE_CONFIG,
        'gui': GUI_CONFIG,
        'colors': COLORS,
        'logging': LOGGING_CONFIG,
        'reports': REPORT_CONFIG,
        'paths': {
            'project_root': PROJECT_ROOT,
            'data_dir': DATA_DIR,
            'logs_dir': LOGS_DIR,
            'reports_dir': REPORTS_DIR,
            'charts_dir': CHARTS_DIR,
        }
    } 