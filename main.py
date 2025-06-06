# main.py

import analises_vendas # Mantenha esta linha
import banco_dados

def exibir_menu():
    print("\n=== Menu de Análise de Vendas ===")
    print("1. Adicionar Nova Venda")
    print("2. Calcular Faturamento Total e Detalhes por Item")
    print("3. Contar Produtos de Baixo Custo")
    print("4. Identificar Itens Vendidos Acima da Média")
    print("5. Listar Todas as Vendas")
    print("6. Editar Venda Existente")
    print("7. Remover Venda")
    print("8. Análise Detalhada por Produto")
    print("9. Sair")

def main():
    banco_dados.criar_tabela_vendas()

    while True:
        exibir_menu()
        try: # O try-except aqui é bom para capturar erros inesperados no loop principal
            escolha = input("Digite sua opção: ")

            # CORREÇÃO AQUI: 'opcao' mudou para 'escolha'
            if escolha == '1':
                analises_vendas.adicionar_nova_venda()
            elif escolha == '2':
                analises_vendas.calcular_faturamento_total(analises_vendas.obter_todas_as_vendas())
            elif escolha == '3':
                analises_vendas.analisar_produtos_baixo_custo(analises_vendas.obter_todas_as_vendas())
            elif escolha == '4':
                analises_vendas.analisar_vendas_acima_da_media(analises_vendas.obter_todas_as_vendas())
            elif escolha == '5':
                analises_vendas.listar_todas_vendas(analises_vendas.obter_todas_as_vendas())
            elif escolha == '6':
                analises_vendas.editar_venda(analises_vendas.obter_todas_as_vendas())
            elif escolha == '7':
                analises_vendas.remover_venda(analises_vendas.obter_todas_as_vendas())
            elif escolha == '8':
                analises_vendas.analisar_vendas_por_produto_unico(analises_vendas.obter_todas_as_vendas())
            elif escolha == '9':
                print("Saindo do programa. Até mais!")
                break
            else:
                print("Opção inválida. Por favor, escolha um número de 1 a 9.")
        except Exception as e:
            # Captura qualquer outro erro que possa ocorrer dentro do bloco try
            print(f"Ocorreu um erro inesperado: {e}")
            print("Por favor, tente novamente.")


if __name__ == '__main__':
    main()