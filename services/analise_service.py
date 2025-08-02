"""
Serviço de análises de vendas.
"""
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
import logging
from models.venda import Venda
from models.database import get_db_session

logger = logging.getLogger(__name__)


class AnaliseService:
    """
    Serviço para análises de vendas.
    
    Esta classe encapsula toda a lógica de análise de dados
    de vendas, incluindo cálculos estatísticos e relatórios.
    """
    
    def __init__(self):
        """Inicializa o serviço de análises."""
        self.session = None
    
    def __enter__(self):
        """Context manager entry."""
        self.session = get_db_session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.session:
            self.session.close()
    
    def calcular_faturamento_total(self) -> Dict[str, Any]:
        """
        Calcula o faturamento total e detalhes por item.
        
        Returns:
            Dict[str, Any]: Dados do faturamento
        """
        try:
            vendas = Venda.listar_todas(self.session)
            
            if not vendas:
                return {
                    'faturamento_total': 0.0,
                    'itens': [],
                    'total_itens': 0
                }
            
            faturamento_total = 0.0
            itens_detalhados = []
            
            for venda in vendas:
                faturamento_item = venda.calcular_faturamento()
                faturamento_total += faturamento_item
                
                itens_detalhados.append({
                    'id': venda.id,
                    'nome': venda.nome,
                    'preco': venda.preco,
                    'quantidade': venda.quantidade,
                    'faturamento': faturamento_item,
                    'data': venda.data_venda
                })
            
            return {
                'faturamento_total': faturamento_total,
                'itens': itens_detalhados,
                'total_itens': len(itens_detalhados)
            }
        except Exception as e:
            logger.error(f"Erro ao calcular faturamento: {e}")
            return {'faturamento_total': 0.0, 'itens': [], 'total_itens': 0}
    
    def analisar_produtos_baixo_custo(self, limite_preco: float = 20.0) -> Dict[str, Any]:
        """
        Analisa produtos de baixo custo.
        
        Args:
            limite_preco: Preço limite para considerar baixo custo
            
        Returns:
            Dict[str, Any]: Análise de produtos de baixo custo
        """
        try:
            vendas = Venda.listar_todas(self.session)
            
            produtos_baixo_custo = []
            for venda in vendas:
                if venda.preco < limite_preco:
                    produtos_baixo_custo.append({
                        'id': venda.id,
                        'nome': venda.nome,
                        'preco': venda.preco,
                        'quantidade': venda.quantidade,
                        'faturamento': venda.calcular_faturamento(),
                        'data': venda.data_venda
                    })
            
            return {
                'limite_preco': limite_preco,
                'produtos': produtos_baixo_custo,
                'total_produtos': len(produtos_baixo_custo),
                'faturamento_total': sum(p['faturamento'] for p in produtos_baixo_custo)
            }
        except Exception as e:
            logger.error(f"Erro ao analisar produtos de baixo custo: {e}")
            return {'limite_preco': limite_preco, 'produtos': [], 'total_produtos': 0, 'faturamento_total': 0.0}
    
    def analisar_vendas_acima_da_media(self) -> Dict[str, Any]:
        """
        Identifica itens vendidos acima da média.
        
        Returns:
            Dict[str, Any]: Análise de vendas acima da média
        """
        try:
            vendas = Venda.listar_todas(self.session)
            
            if not vendas:
                return {
                    'quantidade_media': 0.0,
                    'itens_acima_media': [],
                    'total_itens_acima_media': 0
                }
            
            # Calcula a média de quantidade vendida
            total_quantidade = sum(v.quantidade for v in vendas)
            quantidade_media = total_quantidade / len(vendas)
            
            # Identifica itens acima da média
            itens_acima_media = []
            for venda in vendas:
                if venda.quantidade > quantidade_media:
                    itens_acima_media.append({
                        'id': venda.id,
                        'nome': venda.nome,
                        'quantidade': venda.quantidade,
                        'quantidade_media': quantidade_media,
                        'diferenca': venda.quantidade - quantidade_media,
                        'faturamento': venda.calcular_faturamento(),
                        'data': venda.data_venda
                    })
            
            return {
                'quantidade_media': quantidade_media,
                'itens_acima_media': itens_acima_media,
                'total_itens_acima_media': len(itens_acima_media),
                'total_vendas': len(vendas)
            }
        except Exception as e:
            logger.error(f"Erro ao analisar vendas acima da média: {e}")
            return {'quantidade_media': 0.0, 'itens_acima_media': [], 'total_itens_acima_media': 0, 'total_vendas': 0}
    
    def analisar_vendas_por_produto(self) -> Dict[str, Any]:
        """
        Analisa vendas agrupadas por produto.
        
        Returns:
            Dict[str, Any]: Análise detalhada por produto
        """
        try:
            vendas = Venda.listar_todas(self.session)
            
            if not vendas:
                return {'produtos': {}, 'total_produtos': 0}
            
            # Agrupa vendas por produto
            produtos_agrupados = defaultdict(lambda: {
                'quantidade_total': 0,
                'faturamento_total': 0.0,
                'preco_medio': 0.0,
                'vendas': []
            })
            
            for venda in vendas:
                produto = produtos_agrupados[venda.nome]
                produto['quantidade_total'] += venda.quantidade
                produto['faturamento_total'] += venda.calcular_faturamento()
                produto['vendas'].append({
                    'id': venda.id,
                    'preco': venda.preco,
                    'quantidade': venda.quantidade,
                    'data': venda.data_venda
                })
            
            # Calcula preço médio por produto
            for produto_nome, dados in produtos_agrupados.items():
                if dados['vendas']:
                    dados['preco_medio'] = sum(v['preco'] for v in dados['vendas']) / len(dados['vendas'])
            
            return {
                'produtos': dict(produtos_agrupados),
                'total_produtos': len(produtos_agrupados)
            }
        except Exception as e:
            logger.error(f"Erro ao analisar vendas por produto: {e}")
            return {'produtos': {}, 'total_produtos': 0}
    
    def obter_estatisticas_gerais(self) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais das vendas.
        
        Returns:
            Dict[str, Any]: Estatísticas completas
        """
        try:
            vendas = Venda.listar_todas(self.session)
            
            if not vendas:
                return {
                    'total_vendas': 0,
                    'faturamento_total': 0.0,
                    'quantidade_total': 0,
                    'preco_medio': 0.0,
                    'quantidade_media': 0.0,
                    'produto_mais_vendido': None,
                    'produto_maior_faturamento': None
                }
            
            # Estatísticas básicas
            faturamento_total = sum(v.calcular_faturamento() for v in vendas)
            quantidade_total = sum(v.quantidade for v in vendas)
            preco_medio = sum(v.preco for v in vendas) / len(vendas)
            quantidade_media = quantidade_total / len(vendas)
            
            # Análise por produto
            produtos_agrupados = defaultdict(lambda: {'quantidade': 0, 'faturamento': 0.0})
            
            for venda in vendas:
                produtos_agrupados[venda.nome]['quantidade'] += venda.quantidade
                produtos_agrupados[venda.nome]['faturamento'] += venda.calcular_faturamento()
            
            # Produto mais vendido
            produto_mais_vendido = max(produtos_agrupados.items(), 
                                     key=lambda x: x[1]['quantidade'])
            
            # Produto com maior faturamento
            produto_maior_faturamento = max(produtos_agrupados.items(), 
                                          key=lambda x: x[1]['faturamento'])
            
            return {
                'total_vendas': len(vendas),
                'faturamento_total': faturamento_total,
                'quantidade_total': quantidade_total,
                'preco_medio': preco_medio,
                'quantidade_media': quantidade_media,
                'produto_mais_vendido': {
                    'nome': produto_mais_vendido[0],
                    'quantidade': produto_mais_vendido[1]['quantidade']
                },
                'produto_maior_faturamento': {
                    'nome': produto_maior_faturamento[0],
                    'faturamento': produto_maior_faturamento[1]['faturamento']
                }
            }
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas gerais: {e}")
            return {}
    
    def buscar_tendencias(self) -> Dict[str, Any]:
        """
        Identifica tendências nas vendas.
        
        Returns:
            Dict[str, Any]: Análise de tendências
        """
        try:
            vendas = Venda.listar_todas(self.session)
            
            if len(vendas) < 2:
                return {
                    'tendencia_preco': 'insuficiente_dados',
                    'tendencia_quantidade': 'insuficiente_dados',
                    'crescimento_faturamento': 0.0
                }
            
            # Ordena vendas por data
            vendas_ordenadas = sorted(vendas, key=lambda x: x.data_venda)
            
            # Analisa tendência de preços
            precos = [v.preco for v in vendas_ordenadas]
            tendencia_preco = 'crescente' if precos[-1] > precos[0] else 'decrescente' if precos[-1] < precos[0] else 'estavel'
            
            # Analisa tendência de quantidades
            quantidades = [v.quantidade for v in vendas_ordenadas]
            tendencia_quantidade = 'crescente' if quantidades[-1] > quantidades[0] else 'decrescente' if quantidades[-1] < quantidades[0] else 'estavel'
            
            # Calcula crescimento do faturamento
            faturamento_inicial = vendas_ordenadas[0].calcular_faturamento()
            faturamento_final = vendas_ordenadas[-1].calcular_faturamento()
            
            if faturamento_inicial > 0:
                crescimento_faturamento = ((faturamento_final - faturamento_inicial) / faturamento_inicial) * 100
            else:
                crescimento_faturamento = 0.0
            
            return {
                'tendencia_preco': tendencia_preco,
                'tendencia_quantidade': tendencia_quantidade,
                'crescimento_faturamento': crescimento_faturamento,
                'periodo_analisado': {
                    'inicio': vendas_ordenadas[0].data_venda,
                    'fim': vendas_ordenadas[-1].data_venda
                }
            }
        except Exception as e:
            logger.error(f"Erro ao buscar tendências: {e}")
            return {} 