"""
Diálogos personalizados para a interface gráfica.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any
from datetime import datetime
from models.venda import Venda


class VendaDialog:
    """
    Diálogo para criar/editar vendas.
    """
    
    def __init__(self, parent, title: str, venda: Optional[Venda] = None):
        """
        Inicializa o diálogo.
        
        Args:
            parent: Widget pai
            title: Título da janela
            venda: Venda para editar (None para nova venda)
        """
        self.parent = parent
        self.title = title
        self.venda = venda
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Centralizar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        self.load_data()
        
        # Aguardar resultado
        self.dialog.wait_window()
    
    def create_widgets(self):
        """Cria os widgets do diálogo."""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text=self.title, 
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 20))
        
        # Formulário
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Nome do produto
        ttk.Label(form_frame, text="Nome do Produto:").pack(anchor=tk.W)
        self.nome_var = tk.StringVar()
        self.nome_entry = ttk.Entry(form_frame, textvariable=self.nome_var, width=40)
        self.nome_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Preço
        ttk.Label(form_frame, text="Preço Unitário (R$):").pack(anchor=tk.W)
        self.preco_var = tk.StringVar()
        self.preco_entry = ttk.Entry(form_frame, textvariable=self.preco_var, width=40)
        self.preco_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Quantidade
        ttk.Label(form_frame, text="Quantidade:").pack(anchor=tk.W)
        self.quantidade_var = tk.StringVar()
        self.quantidade_entry = ttk.Entry(form_frame, textvariable=self.quantidade_var, width=40)
        self.quantidade_entry.pack(fill=tk.X, pady=(5, 10))
        
        # Observações
        ttk.Label(form_frame, text="Observações (opcional):").pack(anchor=tk.W)
        self.observacoes_text = tk.Text(form_frame, height=3, width=40)
        self.observacoes_text.pack(fill=tk.X, pady=(5, 10))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Salvar", 
                  command=self.save, style='Success.TButton').pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancelar", 
                  command=self.cancel).pack(side=tk.RIGHT)
        
        # Foco no primeiro campo
        self.nome_entry.focus()
        
        # Bind Enter para salvar
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def load_data(self):
        """Carrega dados da venda para edição."""
        if self.venda:
            self.nome_var.set(self.venda.nome)
            self.preco_var.set(str(self.venda.preco))
            self.quantidade_var.set(str(self.venda.quantidade))
            if self.venda.observacoes:
                self.observacoes_text.insert('1.0', self.venda.observacoes)
    
    def validate_input(self) -> bool:
        """Valida os dados de entrada."""
        nome = self.nome_var.get().strip()
        preco_str = self.preco_var.get().strip()
        quantidade_str = self.quantidade_var.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome do produto é obrigatório.")
            self.nome_entry.focus()
            return False
        
        try:
            preco = float(preco_str)
            if preco <= 0:
                raise ValueError("Preço deve ser maior que zero")
        except ValueError as e:
            messagebox.showerror("Erro", f"Preço inválido: {e}")
            self.preco_entry.focus()
            return False
        
        try:
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
        except ValueError as e:
            messagebox.showerror("Erro", f"Quantidade inválida: {e}")
            self.quantidade_entry.focus()
            return False
        
        return True
    
    def save(self):
        """Salva os dados do formulário."""
        if not self.validate_input():
            return
        
        observacoes = self.observacoes_text.get('1.0', tk.END).strip()
        
        self.result = {
            'nome': self.nome_var.get().strip(),
            'preco': float(self.preco_var.get().strip()),
            'quantidade': int(self.quantidade_var.get().strip()),
            'observacoes': observacoes if observacoes else None
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela a operação."""
        self.result = None
        self.dialog.destroy()


class ConfirmDialog:
    """
    Diálogo de confirmação.
    """
    
    def __init__(self, parent, message: str, title: str = "Confirmação"):
        """
        Inicializa o diálogo de confirmação.
        
        Args:
            parent: Widget pai
            message: Mensagem de confirmação
            title: Título da janela
        """
        self.parent = parent
        self.message = message
        self.title = title
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        
        # Centralizar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Aguardar resultado
        self.dialog.wait_window()
    
    def create_widgets(self):
        """Cria os widgets do diálogo."""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ícone de aviso
        ttk.Label(main_frame, text="⚠️", font=('Segoe UI', 24)).pack(pady=(0, 10))
        
        # Mensagem
        ttk.Label(main_frame, text=self.message, 
                 wraplength=350, justify=tk.CENTER).pack(pady=(0, 20))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Sim", 
                  command=self.confirm, style='Danger.TButton').pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Não", 
                  command=self.cancel).pack(side=tk.RIGHT)
        
        # Bind teclas
        self.dialog.bind('<Return>', lambda e: self.confirm())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def confirm(self):
        """Confirma a ação."""
        self.result = True
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela a ação."""
        self.result = False
        self.dialog.destroy()


class MessageDialog:
    """
    Diálogo para exibir mensagens.
    """
    
    def __init__(self, parent, title: str, message: str):
        """
        Inicializa o diálogo de mensagem.
        
        Args:
            parent: Widget pai
            title: Título da janela
            message: Mensagem a ser exibida
        """
        self.parent = parent
        self.title = title
        self.message = message
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x400")
        self.dialog.resizable(True, True)
        
        # Centralizar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Aguardar fechamento
        self.dialog.wait_window()
    
    def create_widgets(self):
        """Cria os widgets do diálogo."""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text=self.title, 
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 10))
        
        # Área de texto com scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, 
                                  yscrollcommand=scrollbar.set,
                                  font=('Consolas', 10))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.text_widget.yview)
        
        # Inserir mensagem
        self.text_widget.insert('1.0', self.message)
        self.text_widget.config(state=tk.DISABLED)
        
        # Botão OK
        ttk.Button(main_frame, text="OK", 
                  command=self.dialog.destroy).pack()
        
        # Bind teclas
        self.dialog.bind('<Return>', lambda e: self.dialog.destroy())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())


class AnaliseDialog:
    """
    Diálogo para exibir análises com gráficos.
    """
    
    def __init__(self, parent, title: str, dados: Dict[str, Any], 
                 grafico_path: Optional[str] = None):
        """
        Inicializa o diálogo de análise.
        
        Args:
            parent: Widget pai
            title: Título da janela
            dados: Dados da análise
            grafico_path: Caminho para o gráfico (opcional)
        """
        self.parent = parent
        self.title = title
        self.dados = dados
        self.grafico_path = grafico_path
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("800x600")
        self.dialog.resizable(True, True)
        
        # Centralizar diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        
        # Aguardar fechamento
        self.dialog.wait_window()
    
    def create_widgets(self):
        """Cria os widgets do diálogo."""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text=self.title, 
                 font=('Segoe UI', 14, 'bold')).pack(pady=(0, 10))
        
        # Notebook para abas
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba de dados
        dados_frame = ttk.Frame(notebook)
        notebook.add(dados_frame, text="Dados")
        
        # Área de texto para dados
        text_frame = ttk.Frame(dados_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, 
                                  yscrollcommand=scrollbar.set,
                                  font=('Consolas', 10))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.text_widget.yview)
        
        # Inserir dados formatados
        dados_texto = self.formatar_dados()
        self.text_widget.insert('1.0', dados_texto)
        self.text_widget.config(state=tk.DISABLED)
        
        # Aba de gráfico (se disponível)
        if self.grafico_path:
            grafico_frame = ttk.Frame(notebook)
            notebook.add(grafico_frame, text="Gráfico")
            
            try:
                from PIL import Image, ImageTk
                image = Image.open(self.grafico_path)
                # Redimensionar se necessário
                image.thumbnail((700, 500))
                photo = ImageTk.PhotoImage(image)
                
                label = ttk.Label(grafico_frame, image=photo)
                label.image = photo  # Manter referência
                label.pack(pady=20)
                
            except Exception as e:
                ttk.Label(grafico_frame, 
                         text=f"Erro ao carregar gráfico: {e}").pack(pady=20)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Fechar", 
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # Bind teclas
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
    
    def formatar_dados(self) -> str:
        """Formata os dados para exibição."""
        # Implementação básica - pode ser expandida
        return str(self.dados) 