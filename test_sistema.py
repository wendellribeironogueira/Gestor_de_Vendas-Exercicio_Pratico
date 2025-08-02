"""
Script de teste para verificar o funcionamento do sistema refatorado.
"""
import sys
import logging
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa se todos os imports estão funcionando."""
    print("🔍 Testando imports...")
    
    try:
        from config import get_config
        print("✅ config.py - OK")
    except Exception as e:
        print(f"❌ config.py - Erro: {e}")
        return False
    
    try:
        from models.venda import Venda
        print("✅ models.venda - OK")
    except Exception as e:
        print(f"❌ models.venda - Erro: {e}")
        return False
    
    try:
        from models.database import DatabaseManager
        print("✅ models.database - OK")
    except Exception as e:
        print(f"❌ models.database - Erro: {e}")
        return False
    
    try:
        from services.venda_service import VendaService
        print("✅ services.venda_service - OK")
    except Exception as e:
        print(f"❌ services.venda_service - Erro: {e}")
        return False
    
    try:
        from services.analise_service import AnaliseService
        print("✅ services.analise_service - OK")
    except Exception as e:
        print(f"❌ services.analise_service - Erro: {e}")
        return False
    
    try:
        from services.relatorio_service import RelatorioService
        print("✅ services.relatorio_service - OK")
    except Exception as e:
        print(f"❌ services.relatorio_service - Erro: {e}")
        return False
    
    try:
        from gui.main_window import MainWindow
        print("✅ gui.main_window - OK")
    except Exception as e:
        print(f"❌ gui.main_window - Erro: {e}")
        return False
    
    return True


def test_database():
    """Testa o banco de dados."""
    print("\n🗄️  Testando banco de dados...")
    
    try:
        from models.database import init_database, get_db_session
        from models.venda import Venda
        
        # Inicializar banco
        init_database()
        print("✅ Banco inicializado - OK")
        
        # Testar sessão
        session = get_db_session()
        print("✅ Sessão criada - OK")
        
        # Testar criação de venda
        venda = Venda(
            nome="Produto Teste",
            preco=10.50,
            quantidade=5,
            observacoes="Venda de teste"
        )
        session.add(venda)
        session.commit()
        print("✅ Venda criada - OK")
        
        # Testar busca
        vendas = session.query(Venda).all()
        print(f"✅ Busca realizada - {len(vendas)} vendas encontradas")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False


def test_services():
    """Testa os serviços."""
    print("\n🔧 Testando serviços...")
    
    try:
        from services.venda_service import VendaService
        from services.analise_service import AnaliseService
        
        # Testar VendaService
        with VendaService() as service:
            # Criar venda
            venda = service.criar_venda(
                nome="Produto Serviço",
                preco=25.00,
                quantidade=3,
                observacoes="Teste de serviço"
            )
            print("✅ VendaService.criar_venda - OK")
            
            # Listar vendas
            vendas = service.listar_todas()
            print(f"✅ VendaService.listar_todas - {len(vendas)} vendas")
            
            # Estatísticas
            stats = service.obter_estatisticas()
            print("✅ VendaService.obter_estatisticas - OK")
        
        # Testar AnaliseService
        with AnaliseService() as analise:
            faturamento = analise.calcular_faturamento_total()
            print("✅ AnaliseService.calcular_faturamento_total - OK")
            
            baixo_custo = analise.analisar_produtos_baixo_custo()
            print("✅ AnaliseService.analisar_produtos_baixo_custo - OK")
            
            acima_media = analise.analisar_vendas_acima_da_media()
            print("✅ AnaliseService.analisar_vendas_acima_da_media - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos serviços: {e}")
        return False


def test_gui():
    """Testa a interface gráfica (sem abrir janela)."""
    print("\n🖥️  Testando interface gráfica...")
    
    try:
        import tkinter as tk
        from gui.dialogs import VendaDialog, ConfirmDialog, MessageDialog
        
        # Criar root temporário
        root = tk.Tk()
        root.withdraw()  # Esconder janela
        
        # Testar criação de diálogos (sem mostrar)
        print("✅ Tkinter disponível - OK")
        print("✅ Diálogos importados - OK")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erro na interface gráfica: {e}")
        return False


def test_dependencies():
    """Testa as dependências externas."""
    print("\n📦 Testando dependências...")
    
    dependencies = [
        ('sqlalchemy', 'SQLAlchemy'),
        ('matplotlib', 'Matplotlib'),
        ('seaborn', 'Seaborn'),
        ('pandas', 'Pandas'),
        ('PIL', 'Pillow')
    ]
    
    all_ok = True
    
    for package, name in dependencies:
        try:
            __import__(package)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"❌ {name} - Não encontrado")
            all_ok = False
    
    return all_ok


def test_config():
    """Testa as configurações."""
    print("\n⚙️  Testando configurações...")
    
    try:
        from config import get_config
        
        config = get_config()
        
        # Verificar se todas as seções existem
        required_sections = ['database', 'gui', 'colors', 'logging', 'reports', 'paths']
        
        for section in required_sections:
            if section in config:
                print(f"✅ {section} - OK")
            else:
                print(f"❌ {section} - Faltando")
                return False
        
        # Verificar diretórios
        paths = config['paths']
        for path_name, path_obj in paths.items():
            if isinstance(path_obj, Path):
                print(f"✅ {path_name} - {path_obj}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nas configurações: {e}")
        return False


def main():
    """Função principal de teste."""
    print("🧪 Teste do Sistema de Gestão de Vendas Refatorado")
    print("=" * 60)
    
    tests = [
        ("Dependências", test_dependencies),
        ("Configurações", test_config),
        ("Imports", test_imports),
        ("Banco de Dados", test_database),
        ("Serviços", test_services),
        ("Interface Gráfica", test_gui)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado em {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O sistema está funcionando corretamente.")
        print("\n📋 Para executar o sistema:")
        print("python main_refatorado.py")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        print("\n💡 Dicas:")
        print("- Instale as dependências: pip install -r requirements.txt")
        print("- Verifique se todos os arquivos estão presentes")
        print("- Consulte os logs para mais detalhes")


if __name__ == "__main__":
    main() 