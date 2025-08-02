"""
Janela principal da interface gráfica.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from config import get_config
from services.venda_service import VendaService
from services.analise_service import AnaliseService
from services.relatorio_service import RelatorioService
from models.venda import Venda
from .dialogs import VendaDialog, ConfirmDialog, MessageDialog

logger = logging.getLogger(__name__)


class MainWindow:
    """
    Janela principal da aplicação.
    
    Esta classe gerencia a interface gráfica principal,
    incluindo menus, painéis e interações com o usuário.
    """
    
    def __init__(self):
        """Inicializa a janela principal."""
        self.config = get_config()
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.load_data()
    
    def setup_window(self):
        """Configura a janela principal."""
        self.root.title(self.config['gui']['title'])
        self.root.geometry(f"{self.config['gui']['width']}x{self.config['gui']['height']}")
        self.root.configure(bg=self.config['colors']['light'])
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.config['gui']['width'] // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.config['gui']['height'] // 2)
        self.root.geometry(f"{self.config['gui']['width']}x{self.config['gui']['height']}+{x}+{y}")
        
        # Configurar ícone (se disponível)
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass
    
    def setup_styles(self):
        """Configura os estilos da interface."""
        style = ttk.Style()
        style.theme_use(self.config['gui']['theme'])
        
        # Configurar cores
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.config['colors']['primary'])
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground=self.config['colors']['dark'])
        
        style.configure('Success.TLabel',
                       foreground=self.config['colors']['success'])
        
        style.configure('Warning.TLabel',
                       foreground=self.config['colors']['warning'])
        
        style.configure('Danger.TLabel',
                       foreground=self.config['colors']['danger'])
        
        # Configurar botões
        style.configure('Primary.TButton',
                       background=self.config['colors']['primary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background=self.config['colors']['success'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure('Danger.TButton',
                       background=self.config['colors']['danger'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
    
    def create_widgets(self):
        """Cria todos os widgets da interface."""
        self.create_menu()
        self.create_main_frame()
        self.create_sidebar()
        self.create_content_area()
        self.create_status_bar()
    
    def create_menu(self):
        """Cria a barra de menu."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Nova Venda", command=self.nova_venda)
        file_menu.add_separator()
        file_menu.add_command(label="Gerar Relatório", command=self.gerar_relatorio)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.sair)
        
        # Menu Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        edit_menu.add_command(label="Editar Venda", command=self.editar_venda)
        edit_menu.add_command(label="Remover Venda", command=self.remover_venda)
        
        # Menu Análise
        analysis_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Análise", menu=analysis_menu)
        analysis_menu.add_command(label="Faturamento Total", command=self.analisar_faturamento)
        analysis_menu.add_command(label="Produtos Baixo Custo", command=self.analisar_baixo_custo)
        analysis_menu.add_command(label="Vendas Acima da Média", command=self.analisar_acima_media)
        analysis_menu.add_command(label="Análise por Produto", command=self.analisar_por_produto)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.mostrar_sobre)
    
    def create_main_frame(self):
        """Cria o frame principal."""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_sidebar(self):
        """Cria a barra lateral."""
        self.sidebar = ttk.Frame(self.main_frame, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Título da sidebar
        ttk.Label(self.sidebar, text="📊 Gestor de Vendas", 
                 style='Title.TLabel').pack(pady=(0, 20))
        
        # Botões de ação
        ttk.Button(self.sidebar, text="➕ Nova Venda", 
                  style='Primary.TButton',
                  command=self.nova_venda).pack(fill=tk.X, pady=5)
        
        ttk.Button(self.sidebar, text="📝 Editar Venda", 
                  style='Success.TButton',
                  command=self.editar_venda).pack(fill=tk.X, pady=5)
        
        ttk.Button(self.sidebar, text="🗑️ Remover Venda", 
                  style='Danger.TButton',
                  command=self.remover_venda).pack(fill=tk.X, pady=5)
        
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Botões de análise
        ttk.Label(self.sidebar, text="📈 Análises", 
                 style='Header.TLabel').pack(pady=(0, 10))
        
        ttk.Button(self.sidebar, text="💰 Faturamento", 
                  command=self.analisar_faturamento).pack(fill=tk.X, pady=2)
        
        ttk.Button(self.sidebar, text="🛍️ Baixo Custo", 
                  command=self.analisar_baixo_custo).pack(fill=tk.X, pady=2)
        
        ttk.Button(self.sidebar, text="📊 Acima da Média", 
                  command=self.analisar_acima_media).pack(fill=tk.X, pady=2)
        
        ttk.Button(self.sidebar, text="📋 Por Produto", 
                  command=self.analisar_por_produto).pack(fill=tk.X, pady=2)
        
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Botões de relatório
        ttk.Label(self.sidebar, text="📄 Relatórios", 
                 style='Header.TLabel').pack(pady=(0, 10))
        
        ttk.Button(self.sidebar, text="📊 Relatório Completo", 
                  command=self.gerar_relatorio).pack(fill=tk.X, pady=2)
        
        # Estatísticas rápidas
        self.create_quick_stats()
    
    def create_quick_stats(self):
        """Cria painel de estatísticas rápidas."""
        ttk.Separator(self.sidebar, orient='horizontal').pack(fill=tk.X, pady=10)
        
        ttk.Label(self.sidebar, text="📈 Estatísticas Rápidas", 
                 style='Header.TLabel').pack(pady=(0, 10))
        
        self.stats_frame = ttk.Frame(self.sidebar)
        self.stats_frame.pack(fill=tk.X)
        
        # Labels para estatísticas
        self.total_vendas_label = ttk.Label(self.stats_frame, text="Total: 0")
        self.total_vendas_label.pack(anchor=tk.W)
        
        self.faturamento_label = ttk.Label(self.stats_frame, text="Faturamento: R$ 0,00")
        self.faturamento_label.pack(anchor=tk.W)
        
        self.quantidade_label = ttk.Label(self.stats_frame, text="Quantidade: 0")
        self.quantidade_label.pack(anchor=tk.W)
    
    def create_content_area(self):
        """Cria a área de conteúdo principal."""
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título da área de conteúdo
        self.content_title = ttk.Label(self.content_frame, text="Lista de Vendas", 
                                      style='Title.TLabel')
        self.content_title.pack(pady=(0, 10))
        
        # Frame para controles
        controls_frame = ttk.Frame(self.content_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Campo de busca
        ttk.Label(controls_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 10))
        self.search_var.trace('w', self.on_search)
        
        # Botão de atualizar
        ttk.Button(controls_frame, text="🔄 Atualizar", 
                  command=self.load_data).pack(side=tk.RIGHT)
        
        # Treeview para lista de vendas
        self.create_vendas_treeview()
    
    def create_vendas_treeview(self):
        """Cria a tabela de vendas."""
        # Frame para a tabela
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        columns = ('ID', 'Produto', 'Preço', 'Quantidade', 'Faturamento', 'Data')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                 yscrollcommand=v_scrollbar.set,
                                 xscrollcommand=h_scrollbar.set)
        
        # Configurar colunas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Produto', text='Produto')
        self.tree.heading('Preço', text='Preço (R$)')
        self.tree.heading('Quantidade', text='Quantidade')
        self.tree.heading('Faturamento', text='Faturamento (R$)')
        self.tree.heading('Data', text='Data')
        
        # Configurar larguras das colunas
        self.tree.column('ID', width=50, minwidth=50)
        self.tree.column('Produto', width=200, minwidth=150)
        self.tree.column('Preço', width=100, minwidth=80)
        self.tree.column('Quantidade', width=100, minwidth=80)
        self.tree.column('Faturamento', width=120, minwidth=100)
        self.tree.column('Data', width=120, minwidth=100)
        
        # Configurar scrollbars
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Posicionar widgets
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configurar grid weights
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind de eventos
        self.tree.bind('<Double-1>', self.on_venda_double_click)
        self.tree.bind('<Delete>', self.remover_venda)
    
    def create_status_bar(self):
        """Cria a barra de status."""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Pronto")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        self.time_label = ttk.Label(self.status_bar, text="")
        self.time_label.pack(side=tk.RIGHT, padx=5)
        
        self.update_time()
    
    def update_time(self):
        """Atualiza o horário na barra de status."""
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def load_data(self):
        """Carrega os dados das vendas."""
        try:
            with VendaService() as service:
                vendas = service.listar_todas()
                self.update_vendas_treeview(vendas)
                self.update_quick_stats(service.obter_estatisticas())
                self.status_label.config(text=f"Carregadas {len(vendas)} vendas")
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
    
    def update_vendas_treeview(self, vendas: List[Venda]):
        """Atualiza a tabela de vendas."""
        # Limpar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Inserir dados
        for venda in vendas:
            self.tree.insert('', 'end', values=(
                venda.id,
                venda.nome,
                f"R$ {venda.preco:.2f}",
                venda.quantidade,
                f"R$ {venda.calcular_faturamento():.2f}",
                venda.data_venda.strftime("%d/%m/%Y %H:%M") if venda.data_venda else ""
            ))
    
    def update_quick_stats(self, stats: Dict[str, Any]):
        """Atualiza as estatísticas rápidas."""
        self.total_vendas_label.config(text=f"Total: {stats.get('total_vendas', 0)}")
        self.faturamento_label.config(text=f"Faturamento: R$ {stats.get('faturamento_total', 0):.2f}")
        self.quantidade_label.config(text=f"Quantidade: {stats.get('quantidade_total', 0)}")
    
    def on_search(self, *args):
        """Filtra as vendas baseado na busca."""
        search_term = self.search_var.get().lower()
        
        try:
            with VendaService() as service:
                if search_term:
                    vendas = service.buscar_por_nome(search_term)
                else:
                    vendas = service.listar_todas()
                
                self.update_vendas_treeview(vendas)
                self.status_label.config(text=f"Encontradas {len(vendas)} vendas")
        except Exception as e:
            logger.error(f"Erro na busca: {e}")
    
    def on_venda_double_click(self, event):
        """Abre diálogo de edição ao dar duplo clique."""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            venda_id = item['values'][0]
            self.editar_venda_por_id(venda_id)
    
    def nova_venda(self):
        """Abre diálogo para nova venda."""
        dialog = VendaDialog(self.root, title="Nova Venda")
        if dialog.result:
            try:
                with VendaService() as service:
                    service.criar_venda(**dialog.result)
                    self.load_data()
                    messagebox.showinfo("Sucesso", "Venda criada com sucesso!")
            except Exception as e:
                logger.error(f"Erro ao criar venda: {e}")
                messagebox.showerror("Erro", f"Erro ao criar venda: {e}")
    
    def editar_venda(self):
        """Abre diálogo para editar venda selecionada."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma venda para editar.")
            return
        
        item = self.tree.item(selection[0])
        venda_id = item['values'][0]
        self.editar_venda_por_id(venda_id)
    
    def editar_venda_por_id(self, venda_id: int):
        """Edita uma venda específica."""
        try:
            with VendaService() as service:
                venda = service.buscar_venda(venda_id)
                if not venda:
                    messagebox.showerror("Erro", "Venda não encontrada.")
                    return
                
                dialog = VendaDialog(self.root, title="Editar Venda", venda=venda)
                if dialog.result:
                    service.atualizar_venda(venda_id, **dialog.result)
                    self.load_data()
                    messagebox.showinfo("Sucesso", "Venda atualizada com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao editar venda: {e}")
            messagebox.showerror("Erro", f"Erro ao editar venda: {e}")
    
    def remover_venda(self, event=None):
        """Remove a venda selecionada."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma venda para remover.")
            return
        
        item = self.tree.item(selection[0])
        venda_id = item['values'][0]
        venda_nome = item['values'][1]
        
        dialog = ConfirmDialog(self.root, 
                             f"Tem certeza que deseja remover a venda '{venda_nome}'?")
        if dialog.result:
            try:
                with VendaService() as service:
                    service.deletar_venda(venda_id)
                    self.load_data()
                    messagebox.showinfo("Sucesso", "Venda removida com sucesso!")
            except Exception as e:
                logger.error(f"Erro ao remover venda: {e}")
                messagebox.showerror("Erro", f"Erro ao remover venda: {e}")
    
    def analisar_faturamento(self):
        """Analisa o faturamento total."""
        try:
            with AnaliseService() as service:
                dados = service.calcular_faturamento_total()
                self.mostrar_analise_faturamento(dados)
        except Exception as e:
            logger.error(f"Erro ao analisar faturamento: {e}")
            messagebox.showerror("Erro", f"Erro ao analisar faturamento: {e}")
    
    def analisar_baixo_custo(self):
        """Analisa produtos de baixo custo."""
        try:
            with AnaliseService() as service:
                dados = service.analisar_produtos_baixo_custo()
                self.mostrar_analise_baixo_custo(dados)
        except Exception as e:
            logger.error(f"Erro ao analisar baixo custo: {e}")
            messagebox.showerror("Erro", f"Erro ao analisar baixo custo: {e}")
    
    def analisar_acima_media(self):
        """Analisa vendas acima da média."""
        try:
            with AnaliseService() as service:
                dados = service.analisar_vendas_acima_da_media()
                self.mostrar_analise_acima_media(dados)
        except Exception as e:
            logger.error(f"Erro ao analisar acima da média: {e}")
            messagebox.showerror("Erro", f"Erro ao analisar acima da média: {e}")
    
    def analisar_por_produto(self):
        """Analisa vendas por produto."""
        try:
            with AnaliseService() as service:
                dados = service.analisar_vendas_por_produto()
                self.mostrar_analise_por_produto(dados)
        except Exception as e:
            logger.error(f"Erro ao analisar por produto: {e}")
            messagebox.showerror("Erro", f"Erro ao analisar por produto: {e}")
    
    def gerar_relatorio(self):
        """Gera relatório completo."""
        try:
            with AnaliseService() as analise_service:
                with VendaService() as venda_service:
                    estatisticas = venda_service.obter_estatisticas()
                    faturamento = analise_service.calcular_faturamento_total()
                    baixo_custo = analise_service.analisar_produtos_baixo_custo()
                    acima_media = analise_service.analisar_vendas_acima_da_media()
            
            relatorio_service = RelatorioService()
            relatorio_path = relatorio_service.gerar_relatorio_completo(
                estatisticas, faturamento, baixo_custo, acima_media
            )
            
            if relatorio_path:
                messagebox.showinfo("Sucesso", f"Relatório gerado com sucesso!\nArquivo: {relatorio_path}")
            else:
                messagebox.showerror("Erro", "Erro ao gerar relatório.")
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")
    
    def mostrar_analise_faturamento(self, dados: Dict[str, Any]):
        """Mostra análise de faturamento."""
        mensagem = f"""
📊 Análise de Faturamento

💰 Faturamento Total: R$ {dados.get('faturamento_total', 0):.2f}
📦 Total de Itens: {dados.get('total_itens', 0)}

Detalhes por Item:
"""
        for item in dados.get('itens', []):
            mensagem += f"• {item['nome']}: R$ {item['faturamento']:.2f} ({item['quantidade']} un.)\n"
        
        MessageDialog(self.root, "Análise de Faturamento", mensagem)
    
    def mostrar_analise_baixo_custo(self, dados: Dict[str, Any]):
        """Mostra análise de produtos de baixo custo."""
        mensagem = f"""
🛍️ Análise de Produtos de Baixo Custo

💰 Limite de Preço: R$ {dados.get('limite_preco', 0):.2f}
📦 Total de Produtos: {dados.get('total_produtos', 0)}
💵 Faturamento Total: R$ {dados.get('faturamento_total', 0):.2f}

Produtos Encontrados:
"""
        for produto in dados.get('produtos', []):
            mensagem += f"• {produto['nome']}: R$ {produto['preco']:.2f} ({produto['quantidade']} un.)\n"
        
        MessageDialog(self.root, "Produtos de Baixo Custo", mensagem)
    
    def mostrar_analise_acima_media(self, dados: Dict[str, Any]):
        """Mostra análise de vendas acima da média."""
        mensagem = f"""
📊 Análise de Vendas Acima da Média

📈 Quantidade Média: {dados.get('quantidade_media', 0):.1f}
📦 Itens Acima da Média: {dados.get('total_itens_acima_media', 0)}
📋 Total de Vendas: {dados.get('total_vendas', 0)}

Itens Acima da Média:
"""
        for item in dados.get('itens_acima_media', []):
            mensagem += f"• {item['nome']}: {item['quantidade']} un. (+{item['diferenca']:.1f})\n"
        
        MessageDialog(self.root, "Vendas Acima da Média", mensagem)
    
    def mostrar_analise_por_produto(self, dados: Dict[str, Any]):
        """Mostra análise por produto."""
        mensagem = f"""
📋 Análise por Produto

📦 Total de Produtos: {dados.get('total_produtos', 0)}

Detalhes por Produto:
"""
        for produto, info in dados.get('produtos', {}).items():
            mensagem += f"""
• {produto}:
  - Quantidade Total: {info['quantidade_total']}
  - Faturamento Total: R$ {info['faturamento_total']:.2f}
  - Preço Médio: R$ {info['preco_medio']:.2f}
"""
        
        MessageDialog(self.root, "Análise por Produto", mensagem)
    
    def mostrar_sobre(self):
        """Mostra informações sobre o sistema."""
        mensagem = """
📊 Gestor de Vendas - Sistema de Análise

Versão: 2.0
Desenvolvido com Python e Tkinter

Funcionalidades:
• Gerenciamento completo de vendas
• Análises estatísticas avançadas
• Geração de relatórios e gráficos
• Interface gráfica moderna

Tecnologias:
• Python 3.x
• SQLAlchemy (ORM)
• Tkinter (Interface)
• Matplotlib (Gráficos)
• Pandas (Análise de dados)
"""
        MessageDialog(self.root, "Sobre", mensagem)
    
    def sair(self):
        """Sai da aplicação."""
        if messagebox.askokcancel("Sair", "Tem certeza que deseja sair?"):
            self.root.quit()
    
    def run(self):
        """Executa a aplicação."""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Erro na aplicação: {e}")
            messagebox.showerror("Erro", f"Erro na aplicação: {e}") 