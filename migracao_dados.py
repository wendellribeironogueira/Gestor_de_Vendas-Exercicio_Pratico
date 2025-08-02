"""
Script de migração de dados do sistema antigo para o novo.
"""
import json
import sqlite3
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from config import get_config
from models.database import init_database, get_db_session
from models.venda import Venda

logger = logging.getLogger(__name__)


class MigracaoDados:
    """
    Classe para migrar dados do sistema antigo para o novo.
    """
    
    def __init__(self):
        """Inicializa o sistema de migração."""
        self.config = get_config()
        self.old_db_path = 'vendas.db'  # Banco antigo
        self.old_json_path = 'vendas.json'  # JSON antigo (se existir)
        
    def verificar_dados_antigos(self) -> Dict[str, Any]:
        """
        Verifica quais dados antigos estão disponíveis.
        
        Returns:
            Dict[str, Any]: Informações sobre dados disponíveis
        """
        info = {
            'sqlite_antigo': False,
            'json_antigo': False,
            'vendas_encontradas': 0
        }
        
        # Verificar banco SQLite antigo
        if Path(self.old_db_path).exists():
            try:
                conn = sqlite3.connect(self.old_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vendas'")
                if cursor.fetchone():
                    cursor.execute("SELECT COUNT(*) FROM vendas")
                    count = cursor.fetchone()[0]
                    info['sqlite_antigo'] = True
                    info['vendas_encontradas'] = count
                conn.close()
                logger.info(f"Banco SQLite antigo encontrado com {count} vendas")
            except Exception as e:
                logger.error(f"Erro ao verificar banco antigo: {e}")
        
        # Verificar arquivo JSON antigo
        if Path(self.old_json_path).exists():
            try:
                with open(self.old_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        info['json_antigo'] = True
                        info['vendas_encontradas'] = len(data)
                        logger.info(f"Arquivo JSON antigo encontrado com {len(data)} vendas")
            except Exception as e:
                logger.error(f"Erro ao verificar JSON antigo: {e}")
        
        return info
    
    def migrar_do_sqlite_antigo(self) -> List[Dict[str, Any]]:
        """
        Migra dados do banco SQLite antigo.
        
        Returns:
            List[Dict[str, Any]]: Lista de vendas migradas
        """
        vendas = []
        
        try:
            conn = sqlite3.connect(self.old_db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, nome, preco, quantidade FROM vendas")
            rows = cursor.fetchall()
            
            for row in rows:
                venda = {
                    'id': row[0],
                    'nome': row[1],
                    'preco': float(row[2]),
                    'quantidade': int(row[3]),
                    'data_venda': datetime.now(),
                    'observacoes': f"Migrado do sistema antigo em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                }
                vendas.append(venda)
            
            conn.close()
            logger.info(f"Migradas {len(vendas)} vendas do SQLite antigo")
            
        except Exception as e:
            logger.error(f"Erro ao migrar do SQLite antigo: {e}")
        
        return vendas
    
    def migrar_do_json_antigo(self) -> List[Dict[str, Any]]:
        """
        Migra dados do arquivo JSON antigo.
        
        Returns:
            List[Dict[str, Any]]: Lista de vendas migradas
        """
        vendas = []
        
        try:
            with open(self.old_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for item in data:
                # Adaptar formato antigo para novo
                if isinstance(item, dict):
                    venda = {
                        'nome': item.get('nome', 'Produto Desconhecido'),
                        'preco': float(item.get('preco', 0)),
                        'quantidade': int(item.get('quantidade', 0)),
                        'data_venda': datetime.now(),
                        'observacoes': f"Migrado do JSON antigo em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                    }
                    vendas.append(venda)
            
            logger.info(f"Migradas {len(vendas)} vendas do JSON antigo")
            
        except Exception as e:
            logger.error(f"Erro ao migrar do JSON antigo: {e}")
        
        return vendas
    
    def salvar_no_novo_banco(self, vendas: List[Dict[str, Any]]) -> bool:
        """
        Salva as vendas migradas no novo banco de dados.
        
        Args:
            vendas: Lista de vendas para salvar
            
        Returns:
            bool: True se salvou com sucesso
        """
        try:
            session = get_db_session()
            
            for venda_data in vendas:
                # Remover ID se existir (deixar auto-increment)
                if 'id' in venda_data:
                    del venda_data['id']
                
                venda = Venda(**venda_data)
                session.add(venda)
            
            session.commit()
            session.close()
            
            logger.info(f"Salvas {len(vendas)} vendas no novo banco")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar no novo banco: {e}")
            return False
    
    def executar_migracao(self) -> bool:
        """
        Executa a migração completa.
        
        Returns:
            bool: True se a migração foi bem-sucedida
        """
        logger.info("Iniciando processo de migração...")
        
        # Verificar dados antigos
        info = self.verificar_dados_antigos()
        
        if not info['sqlite_antigo'] and not info['json_antigo']:
            logger.warning("Nenhum dado antigo encontrado para migração")
            return False
        
        # Inicializar novo banco
        try:
            init_database()
            logger.info("Novo banco de dados inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar novo banco: {e}")
            return False
        
        vendas_migradas = []
        
        # Migrar do SQLite antigo
        if info['sqlite_antigo']:
            vendas_sqlite = self.migrar_do_sqlite_antigo()
            vendas_migradas.extend(vendas_sqlite)
        
        # Migrar do JSON antigo
        if info['json_antigo']:
            vendas_json = self.migrar_do_json_antigo()
            vendas_migradas.extend(vendas_json)
        
        # Salvar no novo banco
        if vendas_migradas:
            success = self.salvar_no_novo_banco(vendas_migradas)
            if success:
                logger.info(f"Migração concluída com sucesso! {len(vendas_migradas)} vendas migradas")
                return True
            else:
                logger.error("Erro ao salvar dados migrados")
                return False
        else:
            logger.warning("Nenhuma venda foi migrada")
            return False
    
    def criar_backup(self) -> bool:
        """
        Cria backup dos dados antigos antes da migração.
        
        Returns:
            bool: True se o backup foi criado com sucesso
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup do banco antigo
            if Path(self.old_db_path).exists():
                backup_path = f"backup_vendas_{timestamp}.db"
                import shutil
                shutil.copy2(self.old_db_path, backup_path)
                logger.info(f"Backup do banco criado: {backup_path}")
            
            # Backup do JSON antigo
            if Path(self.old_json_path).exists():
                backup_path = f"backup_vendas_{timestamp}.json"
                import shutil
                shutil.copy2(self.old_json_path, backup_path)
                logger.info(f"Backup do JSON criado: {backup_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return False


def main():
    """
    Função principal do script de migração.
    """
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🔄 Script de Migração de Dados")
    print("=" * 50)
    
    migracao = MigracaoDados()
    
    # Verificar dados disponíveis
    info = migracao.verificar_dados_antigos()
    
    if not info['sqlite_antigo'] and not info['json_antigo']:
        print("❌ Nenhum dado antigo encontrado para migração.")
        print("Certifique-se de que os arquivos 'vendas.db' ou 'vendas.json' existem.")
        return
    
    print(f"📊 Dados encontrados:")
    if info['sqlite_antigo']:
        print(f"   - Banco SQLite: {info['vendas_encontradas']} vendas")
    if info['json_antigo']:
        print(f"   - Arquivo JSON: {info['vendas_encontradas']} vendas")
    
    # Perguntar confirmação
    resposta = input("\nDeseja prosseguir com a migração? (s/N): ").strip().lower()
    if resposta not in ['s', 'sim', 'y', 'yes']:
        print("Migração cancelada.")
        return
    
    # Criar backup
    print("\n📦 Criando backup dos dados antigos...")
    if not migracao.criar_backup():
        print("⚠️  Aviso: Não foi possível criar backup. Continuando mesmo assim...")
    
    # Executar migração
    print("\n🔄 Executando migração...")
    if migracao.executar_migracao():
        print("✅ Migração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Execute 'python main_refatorado.py' para iniciar o novo sistema")
        print("2. Verifique se todos os dados foram migrados corretamente")
        print("3. Teste as funcionalidades do novo sistema")
    else:
        print("❌ Erro durante a migração. Verifique os logs para mais detalhes.")


if __name__ == "__main__":
    main() 