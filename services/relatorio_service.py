"""
Serviço de geração de relatórios e gráficos.
"""
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
from pathlib import Path
from config import get_config

logger = logging.getLogger(__name__)


class RelatorioService:
    """
    Serviço para geração de relatórios e gráficos.
    
    Esta classe encapsula toda a lógica de geração de relatórios,
    gráficos e exportação de dados.
    """
    
    def __init__(self):
        """Inicializa o serviço de relatórios."""
        self.config = get_config()
        self.charts_dir = Path(self.config['paths']['charts_dir'])
        self.reports_dir = Path(self.config['paths']['reports_dir'])
        
        # Configurar estilo dos gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def gerar_grafico_faturamento(self, dados_faturamento: Dict[str, Any]) -> str:
        """
        Gera gráfico de faturamento por produto.
        
        Args:
            dados_faturamento: Dados do faturamento
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            if not dados_faturamento['itens']:
                logger.warning("Nenhum dado de faturamento para gerar gráfico")
                return ""
            
            # Criar DataFrame
            df = pd.DataFrame(dados_faturamento['itens'])
            
            # Criar gráfico
            plt.figure(figsize=(12, 8))
            
            # Gráfico de barras do faturamento por produto
            plt.subplot(2, 2, 1)
            faturamento_por_produto = df.groupby('nome')['faturamento'].sum().sort_values(ascending=True)
            faturamento_por_produto.plot(kind='barh', color='skyblue')
            plt.title('Faturamento por Produto')
            plt.xlabel('Faturamento (R$)')
            plt.ylabel('Produto')
            
            # Gráfico de pizza da distribuição
            plt.subplot(2, 2, 2)
            plt.pie(faturamento_por_produto.values, labels=faturamento_por_produto.index, autopct='%1.1f%%')
            plt.title('Distribuição do Faturamento')
            
            # Gráfico de linha temporal
            plt.subplot(2, 2, 3)
            df['data'] = pd.to_datetime(df['data'])
            df_temporal = df.groupby(df['data'].dt.date)['faturamento'].sum()
            df_temporal.plot(kind='line', marker='o')
            plt.title('Faturamento ao Longo do Tempo')
            plt.xlabel('Data')
            plt.ylabel('Faturamento (R$)')
            plt.xticks(rotation=45)
            
            # Gráfico de quantidade vs preço
            plt.subplot(2, 2, 4)
            plt.scatter(df['preco'], df['quantidade'], alpha=0.6, s=df['faturamento']/10)
            plt.xlabel('Preço (R$)')
            plt.ylabel('Quantidade')
            plt.title('Relação Preço vs Quantidade')
            
            plt.tight_layout()
            
            # Salvar gráfico
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"faturamento_{timestamp}.png"
            filepath = self.charts_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Gráfico de faturamento gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de faturamento: {e}")
            return ""
    
    def gerar_grafico_produtos_baixo_custo(self, dados_baixo_custo: Dict[str, Any]) -> str:
        """
        Gera gráfico de produtos de baixo custo.
        
        Args:
            dados_baixo_custo: Dados dos produtos de baixo custo
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            if not dados_baixo_custo['produtos']:
                logger.warning("Nenhum produto de baixo custo para gerar gráfico")
                return ""
            
            df = pd.DataFrame(dados_baixo_custo['produtos'])
            
            plt.figure(figsize=(12, 8))
            
            # Gráfico de barras dos produtos
            plt.subplot(2, 2, 1)
            df_sorted = df.sort_values('faturamento', ascending=True)
            plt.barh(df_sorted['nome'], df_sorted['faturamento'], color='lightcoral')
            plt.title(f'Produtos de Baixo Custo (≤ R${dados_baixo_custo["limite_preco"]:.2f})')
            plt.xlabel('Faturamento (R$)')
            
            # Gráfico de preços
            plt.subplot(2, 2, 2)
            plt.hist(df['preco'], bins=10, color='lightgreen', alpha=0.7)
            plt.axvline(dados_baixo_custo['limite_preco'], color='red', linestyle='--', 
                       label=f'Limite: R${dados_baixo_custo["limite_preco"]:.2f}')
            plt.title('Distribuição de Preços')
            plt.xlabel('Preço (R$)')
            plt.ylabel('Frequência')
            plt.legend()
            
            # Gráfico de quantidade vs preço
            plt.subplot(2, 2, 3)
            plt.scatter(df['preco'], df['quantidade'], alpha=0.6, s=50)
            plt.xlabel('Preço (R$)')
            plt.ylabel('Quantidade')
            plt.title('Quantidade vs Preço')
            
            # Gráfico de pizza do faturamento
            plt.subplot(2, 2, 4)
            faturamento_total = dados_baixo_custo['faturamento_total']
            outros = dados_baixo_custo.get('faturamento_outros', 0)
            if outros > 0:
                plt.pie([faturamento_total, outros], 
                       labels=['Baixo Custo', 'Outros'], 
                       autopct='%1.1f%%', colors=['lightcoral', 'lightblue'])
                plt.title('Proporção do Faturamento')
            
            plt.tight_layout()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"baixo_custo_{timestamp}.png"
            filepath = self.charts_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Gráfico de produtos de baixo custo gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de produtos de baixo custo: {e}")
            return ""
    
    def gerar_grafico_vendas_acima_media(self, dados_acima_media: Dict[str, Any]) -> str:
        """
        Gera gráfico de vendas acima da média.
        
        Args:
            dados_acima_media: Dados das vendas acima da média
            
        Returns:
            str: Caminho do arquivo gerado
        """
        try:
            if not dados_acima_media['itens_acima_media']:
                logger.warning("Nenhum item acima da média para gerar gráfico")
                return ""
            
            df = pd.DataFrame(dados_acima_media['itens_acima_media'])
            
            plt.figure(figsize=(12, 8))
            
            # Gráfico de barras das quantidades
            plt.subplot(2, 2, 1)
            df_sorted = df.sort_values('quantidade', ascending=True)
            bars = plt.barh(df_sorted['nome'], df_sorted['quantidade'], color='gold')
            plt.axvline(dados_acima_media['quantidade_media'], color='red', linestyle='--', 
                       label=f'Média: {dados_acima_media["quantidade_media"]:.1f}')
            plt.title('Quantidade Vendida vs Média')
            plt.xlabel('Quantidade')
            plt.legend()
            
            # Gráfico de diferença da média
            plt.subplot(2, 2, 2)
            df_sorted = df.sort_values('diferenca', ascending=True)
            plt.barh(df_sorted['nome'], df_sorted['diferenca'], color='orange')
            plt.title('Diferença da Média')
            plt.xlabel('Quantidade Acima da Média')
            
            # Gráfico de dispersão
            plt.subplot(2, 2, 3)
            plt.scatter(df['quantidade'], df['faturamento'], alpha=0.6, s=50)
            plt.xlabel('Quantidade')
            plt.ylabel('Faturamento (R$)')
            plt.title('Quantidade vs Faturamento')
            
            # Gráfico de pizza
            plt.subplot(2, 2, 4)
            total_acima = dados_acima_media['total_itens_acima_media']
            total_geral = dados_acima_media['total_vendas']
            total_abaixo = total_geral - total_acima
            plt.pie([total_acima, total_abaixo], 
                   labels=['Acima da Média', 'Abaixo da Média'], 
                   autopct='%1.1f%%', colors=['gold', 'lightgray'])
            plt.title('Distribuição vs Média')
            
            plt.tight_layout()
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"acima_media_{timestamp}.png"
            filepath = self.charts_dir / filename
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Gráfico de vendas acima da média gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de vendas acima da média: {e}")
            return ""
    
    def gerar_relatorio_completo(self, estatisticas: Dict[str, Any], 
                                faturamento: Dict[str, Any],
                                baixo_custo: Dict[str, Any],
                                acima_media: Dict[str, Any]) -> str:
        """
        Gera um relatório completo em HTML.
        
        Args:
            estatisticas: Estatísticas gerais
            faturamento: Dados de faturamento
            baixo_custo: Dados de produtos de baixo custo
            acima_media: Dados de vendas acima da média
            
        Returns:
            str: Caminho do arquivo HTML gerado
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"relatorio_completo_{timestamp}.html"
            filepath = self.reports_dir / filename
            
            # Gerar gráficos
            grafico_faturamento = self.gerar_grafico_faturamento(faturamento)
            grafico_baixo_custo = self.gerar_grafico_produtos_baixo_custo(baixo_custo)
            grafico_acima_media = self.gerar_grafico_vendas_acima_media(acima_media)
            
            # Criar HTML
            html_content = self._criar_html_relatorio(
                estatisticas, faturamento, baixo_custo, acima_media,
                grafico_faturamento, grafico_baixo_custo, grafico_acima_media
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Relatório completo gerado: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório completo: {e}")
            return ""
    
    def _criar_html_relatorio(self, estatisticas: Dict[str, Any],
                             faturamento: Dict[str, Any],
                             baixo_custo: Dict[str, Any],
                             acima_media: Dict[str, Any],
                             grafico_faturamento: str,
                             grafico_baixo_custo: str,
                             grafico_acima_media: str) -> str:
        """
        Cria o conteúdo HTML do relatório.
        """
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório de Vendas - {datetime.now().strftime("%d/%m/%Y %H:%M")}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
                .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }}
                .stat-value {{ font-size: 24px; font-weight: bold; color: #2E86AB; }}
                .stat-label {{ color: #6c757d; margin-top: 5px; }}
                .chart-container {{ text-align: center; margin: 20px 0; }}
                .chart-container img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                .success {{ color: #28a745; }}
                .warning {{ color: #ffc107; }}
                .danger {{ color: #dc3545; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Relatório de Vendas</h1>
                <p>Gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M")}</p>
            </div>
            
            <div class="section">
                <h2>📈 Estatísticas Gerais</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{estatisticas.get('total_vendas', 0)}</div>
                        <div class="stat-label">Total de Vendas</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">R$ {estatisticas.get('faturamento_total', 0):.2f}</div>
                        <div class="stat-label">Faturamento Total</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{estatisticas.get('quantidade_total', 0)}</div>
                        <div class="stat-label">Quantidade Total</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">R$ {estatisticas.get('preco_medio', 0):.2f}</div>
                        <div class="stat-label">Preço Médio</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>💰 Análise de Faturamento</h2>
                <p><strong>Faturamento Total:</strong> R$ {faturamento.get('faturamento_total', 0):.2f}</p>
                <p><strong>Total de Itens:</strong> {faturamento.get('total_itens', 0)}</p>
                
                {self._criar_tabela_faturamento(faturamento)}
                
                {f'<div class="chart-container"><img src="{grafico_faturamento}" alt="Gráfico de Faturamento"></div>' if grafico_faturamento else ''}
            </div>
            
            <div class="section">
                <h2>🛍️ Produtos de Baixo Custo</h2>
                <p><strong>Limite de Preço:</strong> R$ {baixo_custo.get('limite_preco', 0):.2f}</p>
                <p><strong>Total de Produtos:</strong> {baixo_custo.get('total_produtos', 0)}</p>
                <p><strong>Faturamento Total:</strong> R$ {baixo_custo.get('faturamento_total', 0):.2f}</p>
                
                {self._criar_tabela_baixo_custo(baixo_custo)}
                
                {f'<div class="chart-container"><img src="{grafico_baixo_custo}" alt="Gráfico de Produtos de Baixo Custo"></div>' if grafico_baixo_custo else ''}
            </div>
            
            <div class="section">
                <h2>📊 Vendas Acima da Média</h2>
                <p><strong>Quantidade Média:</strong> {acima_media.get('quantidade_media', 0):.1f}</p>
                <p><strong>Itens Acima da Média:</strong> {acima_media.get('total_itens_acima_media', 0)}</p>
                <p><strong>Total de Vendas:</strong> {acima_media.get('total_vendas', 0)}</p>
                
                {self._criar_tabela_acima_media(acima_media)}
                
                {f'<div class="chart-container"><img src="{grafico_acima_media}" alt="Gráfico de Vendas Acima da Média"></div>' if grafico_acima_media else ''}
            </div>
        </body>
        </html>
        """
        return html
    
    def _criar_tabela_faturamento(self, faturamento: Dict[str, Any]) -> str:
        """Cria tabela HTML para dados de faturamento."""
        if not faturamento.get('itens'):
            return "<p>Nenhum dado de faturamento disponível.</p>"
        
        html = """
        <table>
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Preço</th>
                    <th>Quantidade</th>
                    <th>Faturamento</th>
                    <th>Data</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for item in faturamento['itens']:
            html += f"""
                <tr>
                    <td>{item['nome']}</td>
                    <td>R$ {item['preco']:.2f}</td>
                    <td>{item['quantidade']}</td>
                    <td>R$ {item['faturamento']:.2f}</td>
                    <td>{item['data'].strftime('%d/%m/%Y') if hasattr(item['data'], 'strftime') else str(item['data'])}</td>
                </tr>
            """
        
        html += "</tbody></table>"
        return html
    
    def _criar_tabela_baixo_custo(self, baixo_custo: Dict[str, Any]) -> str:
        """Cria tabela HTML para produtos de baixo custo."""
        if not baixo_custo.get('produtos'):
            return "<p>Nenhum produto de baixo custo encontrado.</p>"
        
        html = """
        <table>
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Preço</th>
                    <th>Quantidade</th>
                    <th>Faturamento</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for produto in baixo_custo['produtos']:
            html += f"""
                <tr>
                    <td>{produto['nome']}</td>
                    <td>R$ {produto['preco']:.2f}</td>
                    <td>{produto['quantidade']}</td>
                    <td>R$ {produto['faturamento']:.2f}</td>
                </tr>
            """
        
        html += "</tbody></table>"
        return html
    
    def _criar_tabela_acima_media(self, acima_media: Dict[str, Any]) -> str:
        """Cria tabela HTML para vendas acima da média."""
        if not acima_media.get('itens_acima_media'):
            return "<p>Nenhum item vendido acima da média.</p>"
        
        html = """
        <table>
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Quantidade</th>
                    <th>Média</th>
                    <th>Diferença</th>
                    <th>Faturamento</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for item in acima_media['itens_acima_media']:
            html += f"""
                <tr>
                    <td>{item['nome']}</td>
                    <td>{item['quantidade']}</td>
                    <td>{item['quantidade_media']:.1f}</td>
                    <td class="success">+{item['diferenca']:.1f}</td>
                    <td>R$ {item['faturamento']:.2f}</td>
                </tr>
            """
        
        html += "</tbody></table>"
        return html 