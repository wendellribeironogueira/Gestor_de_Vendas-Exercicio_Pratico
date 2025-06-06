import json
import banco_dados

# Adicione esta CLASSE Venda
class Venda:
    def __init__(self, nome, preco, quantidade, id=None):
        # O método __init__ é o construtor.
        # 'self' refere-se à instância do objeto que está sendo criada.
        # 'nome', 'preco', 'quantidade' são os parâmetros que passamos ao criar a venda.
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def calcular_faturamento_item(self):
        # Exemplo de método dentro da classe Venda
        # self.preco e self.quantidade acessam os atributos da instância atual
        return self.preco * self.quantidade


    def __str__(self):
        return f ('id: {self.id} |"Produto: {self.nome} | Preço: R${self.preco:.2f} | Quantidade: {self.quantidade}')

    # Método para converter o objeto Venda de volta para um dicionário
    # Isso será crucial para salvar em JSON, pois o módulo json não sabe salvar objetos Venda diretamente
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade
        }
# As funções existentes (calcular_faturamento_total, analisar_produtos_baixo_custo, etc.)
# vêm logo abaixo desta classe.
def calcular_faturamento_total(lista_de_vendas):  # Usei lista_de_vendas no parâmetro para evitar conflito de nomes, boa prática
    print(f'\n--------FATURAMENTO TOTAL E DETALHES POR ITEM---------')
    faturamento_total_acumulado = 0
    for item_da_venda in lista_de_vendas:
        nome_produto = item_da_venda.nome
        preco_produto = item_da_venda.preco
        quantidade_vendida = item_da_venda.quantidade

        faturamento_do_item = preco_produto * quantidade_vendida
        faturamento_total_acumulado += faturamento_do_item

        print(f"O faturamento do {nome_produto} foi de R$ {faturamento_do_item:.2f} reais (Qtd: {quantidade_vendida})")

    print(f'\nFaturamento TOTAL GERAL de todas as vendas: R$ {faturamento_total_acumulado:.2f} reais')


# --- 2. Contar Produtos de Baixo Custo ---
def analisar_produtos_baixo_custo(lista_de_vendas):  # Usei lista_de_vendas no parâmetro
    print(f'\n--------PRODUTOS DE BAIXO CUSTO---------')
    contador_baixo_custo = 0
    for item_de_custo in lista_de_vendas:
        nome_produto_baixo_custo = item_de_custo.nome
        preco_produto_baixo_custo = item_de_custo.preco
        quantidade_vendida_baixo_custo = item_de_custo.quantidade

        if preco_produto_baixo_custo < 20.00:
            contador_baixo_custo += 1
            ### CORREÇÃO AQUI: O print agora está DENTRO do IF ###
            print(
                f'O Produto de Baixo Custo é: {nome_produto_baixo_custo} (R$ {preco_produto_baixo_custo:.2f}) - {quantidade_vendida_baixo_custo} unidades.')

    print(f'\nTotal de {contador_baixo_custo} produtos com preço unitário menor que R$ 20.00.')

# --- 3. Identificar Itens Vendidos Acima da Média ---
def analisar_vendas_acima_da_media(lista_de_vendas):  # Usei lista_de_vendas no parâmetro
    print(f'\n--------ITENS VENDIDOS ACIMA DA MÉDIA---------')
    soma_total_quantidades_vendidas = 0
    for item_quantidade in lista_de_vendas:
        quantidade_vendida_loop = item_quantidade.quantidade
        soma_total_quantidades_vendidas += quantidade_vendida_loop

    numero_total_de_transacoes = len(lista_de_vendas)  # Usa o parâmetro da função

    if numero_total_de_transacoes > 0:
        quantidade_media_por_transacao = soma_total_quantidades_vendidas / numero_total_de_transacoes
        print(f"A quantidade média de itens vendidos por transação é de: {quantidade_media_por_transacao:.2f} unidades.\n")

        print("Produtos com quantidade vendida ACIMA da média:")
        for item_acima_media in lista_de_vendas:
            nome_produto_acima_media = item_acima_media.nome
            quantidade_vendida_acima_media = item_acima_media.quantidade

            if quantidade_vendida_acima_media > quantidade_media_por_transacao:
                print(f"- {nome_produto_acima_media} (Vendeu: {quantidade_vendida_acima_media} unidades)")
    else:
        print("Não há transações para calcular a média e identificar itens acima dela.")

# Dentro de analises_vendas.py (adicione essa função NO FINAL das outras)

# Dentro de analises_vendas.py (modifique esta função)

def adicionar_nova_venda(): # Não precisa mais receber lista_de_vendas como parametro
    print("\n-------- ADICIONAR NOVA VENDA --------")
    nome = input("Digite o nome do produto: ")

    while True:
        try:
            preco_str = input("Digite o preço unitário do produto (ex: 35.50): ")
            preco = float(preco_str)
            if preco <= 0:
                print("O preço deve ser um valor positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida para o preço! Por favor, digite um número (ex: 35.50).")

    while True:
        try:
            quantidade_str = input("Digite a quantidade vendida (apenas números inteiros): ")
            quantidade = int(quantidade_str)
            if quantidade <= 0:
                print("A quantidade deve ser um número inteiro positivo.")
                continue
            break
        except ValueError:
            print("Entrada inválida para a quantidade! Por favor, digite um número inteiro.")

    # Conectar ao banco de dados
    conn = banco_dados.get_db_connection()
    cursor = conn.cursor()

    # Comando SQL para inserir a nova venda
    # Usamos '?' como placeholders para segurança e para lidar com tipos de dados
    cursor.execute("INSERT INTO vendas (nome, preco, quantidade) VALUES (?, ?, ?)",
                   (nome, preco, quantidade)) # Passamos os valores como uma tupla

    conn.commit() # Salva as mudanças no banco de dados
    conn.close() # Fecha a conexão

    print(f"\n✅ Venda de '{nome}' adicionada com sucesso ao banco de dados!")
    # Não precisamos mais adicionar à lista_de_vendas aqui,
    # pois obter_todas_as_vendas() irá carregar tudo do DB quando necessário.

def salvar_vendas(lista_de_vendas):
    try:
        # AGORA A MUDANÇA: converter cada objeto Venda em um dicionário
        dados_para_salvar = []
        for venda_objeto in lista_de_vendas:
            dados_para_salvar.append(venda_objeto.to_dict()) # Chamamos o métodoto_dict() do objeto

        with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as arquivo:
            json.dump(dados_para_salvar, arquivo, indent=4, ensure_ascii=False)
        # print(f"Dados de vendas salvos em '{CAMINHO_ARQUIVO}'.")
    except Exception as e:
        print(f"Erro ao salvar dados de vendas: {e}")

def obter_todas_as_vendas():
    conn = banco_dados.get_db_connection() # Obtém uma conexão com o banco
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, preco, quantidade FROM vendas")
    rows = cursor.fetchall() # Pega todas as linhas retornadas pela consulta

    vendas_do_banco = []
    for row in rows:
        # Cada 'row' é uma tupla (id, nome, preco, quantidade)
        # Criamos um objeto Venda a partir dessa tupla
        venda_objeto = Venda(id=row[0], nome=row[1], preco=row[2], quantidade=row[3])
        vendas_do_banco.append(venda_objeto)

    conn.close() # Sempre feche a conexão após usar

    print(f"Dados de vendas carregados do banco de dados '{banco_dados.NOME_BANCO}'.")
    return vendas_do_banco

# Dentro de analises_vendas.py
# ... (suas funções anteriores)

def editar_venda(lista_de_vendas_atualizada): # Recebe a lista do DB para exibição
    print("\n-------- EDITAR VENDA EXISTENTE --------")
    if not lista_de_vendas_atualizada:
        print("Não há vendas cadastradas para editar.")
        return

    print("\nVendas atuais:")
    for i, venda in enumerate(lista_de_vendas_atualizada):
        # Agora estamos usando o ID real do banco de dados na exibição
        print(f"{i+1}. ID: {venda.id} | Produto: {venda.nome}, Preço: R${venda.preco:.2f}, Quantidade: {venda.quantidade}")

    while True:
        try:
            identificador = input("Digite o NÚMERO (da lista acima) ou o NOME do produto que deseja editar: ").strip()
            venda_encontrada = None
            venda_id_para_editar = None # Variável para armazenar o ID do banco de dados

            if identificador.isdigit():
                num_venda_escolhida = int(identificador) - 1
                if 0 <= num_venda_escolhida < len(lista_de_vendas_atualizada):
                    venda_encontrada = lista_de_vendas_atualizada[num_venda_escolhida]
                    venda_id_para_editar = venda_encontrada.id # Pegamos o ID do DB
            else:
                for venda in lista_de_vendas_atualizada:
                    if venda.nome.lower() == identificador.lower():
                        venda_encontrada = venda
                        venda_id_para_editar = venda.id # Pegamos o ID do DB
                        break

            if venda_encontrada:
                print(f"\n--- Editando: {venda_encontrada.nome} (ID: {venda_encontrada.id}) ---")
                print(f"Preço atual: R${venda_encontrada.preco:.2f}, Quantidade atual: {venda_encontrada.quantidade}")

                novo_preco = venda_encontrada.preco
                nova_quantidade = venda_encontrada.quantidade

                while True:
                    opcao_edicao = input("O que deseja editar? (preco / quantidade / ambos / sair): ").lower().strip()
                    if opcao_edicao == 'preco' or opcao_edicao == 'ambos':
                        while True:
                            try:
                                novo_preco_str = input("Digite o NOVO preço unitário: ")
                                novo_preco = float(novo_preco_str)
                                if novo_preco <= 0:
                                    print("O preço deve ser um valor positivo.")
                                    continue
                                break
                            except ValueError:
                                print("Entrada inválida para o preço! Por favor, digite um número.")

                    if opcao_edicao == 'quantidade' or opcao_edicao == 'ambos':
                        while True:
                            try:
                                nova_quantidade_str = input("Digite a NOVA quantidade vendida: ")
                                nova_quantidade = int(nova_quantidade_str)
                                if nova_quantidade <= 0:
                                    print("A quantidade deve ser um número inteiro positivo.")
                                    continue
                                break
                            except ValueError:
                                print("Entrada inválida para a quantidade! Por favor, digite um número inteiro.")

                    if opcao_edicao == 'sair':
                        print("Edição cancelada.")
                        break
                    elif opcao_edicao not in ['preco', 'quantidade', 'ambos', 'sair']:
                        print("Opção de edição inválida. Use 'preco', 'quantidade', 'ambos' ou 'sair'.")
                    else:
                        # Conectar ao banco e executar o UPDATE
                        conn = banco_dados.get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE vendas SET preco = ?, quantidade = ? WHERE id = ?",
                                       (novo_preco, nova_quantidade, venda_id_para_editar))
                        conn.commit()
                        conn.close()
                        print(f"\n✅ Venda de '{venda_encontrada.nome}' (ID: {venda_encontrada.id}) editada com sucesso!")
                        break # Sai do loop de edição
                break # Sai do loop principal de encontrar venda
            else:
                print("Venda não encontrada com o número ou nome informado. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado durante a edição: {e}. Tente novamente.")


def remover_venda(lista_de_vendas_atualizada): # Recebe a lista do DB para exibição
    print("\n-------- REMOVER VENDA --------")
    if not lista_de_vendas_atualizada:
        print("Não há vendas cadastradas para remover.")
        return

    print("\nVendas atuais:")
    for i, venda in enumerate(lista_de_vendas_atualizada):
        # Agora estamos usando o ID real do banco de dados na exibição
        print(f"{i+1}. ID: {venda.id} | Produto: {venda.nome}, Preço: R${venda.preco:.2f}, Quantidade: {venda.quantidade}")

    while True:
        try:
            identificador = input("Digite o NÚMERO (da lista acima) ou o NOME do produto que deseja remover: ").strip()

            venda_encontrada = None
            venda_id_para_remover = None # Variável para armazenar o ID do banco de dados

            if identificador.isdigit():
                num_venda_escolhida = int(identificador) - 1
                if 0 <= num_venda_escolhida < len(lista_de_vendas_atualizada):
                    venda_encontrada = lista_de_vendas_atualizada[num_venda_escolhida]
                    venda_id_para_remover = venda_encontrada.id # Pegamos o ID do DB
            else:
                for venda in lista_de_vendas_atualizada:
                    if venda.nome.lower() == identificador.lower():
                        venda_encontrada = venda
                        venda_id_para_remover = venda.id # Pegamos o ID do DB
                        break

            if venda_encontrada:
                confirmacao = input(f"Tem certeza que deseja remover a venda de '{venda_encontrada.nome}' (ID: {venda_encontrada.id}) (S/N)? ").strip().lower()
                if confirmacao == 's':
                    # Conectar ao banco e executar o DELETE
                    conn = banco_dados.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM vendas WHERE id = ?", (venda_id_para_remover,))
                    conn.commit()
                    conn.close()
                    print(f"\n✅ Venda de '{venda_encontrada.nome}' (ID: {venda_encontrada.id}) removida com sucesso!")
                else:
                    print("Remoção cancelada.")
                break # Sai do loop principal
            else:
                print("Venda não encontrada com o número ou nome informado. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado durante a remoção: {e}. Tente novamente.")

def listar_todas_vendas(lista_de_vendas):
    print("\n-------- LISTA DE TODAS AS VENDAS --------")
    if not lista_de_vendas:
        print("Não há vendas cadastradas para exibir.")
        return

    for i, venda in enumerate(lista_de_vendas):
        # Usamos f-strings para formatar a saída.
        # {i+1} para mostrar o número da venda começando do 1 (mais amigável para o usuário)
        # {venda['nome']} para o nome do produto
        # {venda['preco']:.2f} para o preço formatado com 2 casas decimais
        # {venda['quantidade']} para a quantidade
        print(f"{i+1}. Produto: {venda.nome} | Preço Unitário: R${venda.preco:.2f} | Quantidade: {venda.quantidade}")
    print("------------------------------------------")

# Dentro de analises_vendas.py

def analisar_vendas_por_produto_unico(lista_de_vendas):
    print("\n-------- ANÁLISE DETALHADA POR PRODUTO --------")
    if not lista_de_vendas:
        print("Não há vendas cadastradas para analisar.")
        return

    # Dicionário para armazenar os totais por produto:
    # Ex: {'Camisa': {'quantidade_total': 25, 'faturamento_total': 875.00}}
    sumario_produtos = {}

    for venda in lista_de_vendas:
        nome_produto = venda.nome
        preco = venda.preco
        quantidade = venda.quantidade
        faturamento_item = preco * quantidade

        # Se o produto ainda não está no sumário, inicializa seus totais
        if nome_produto not in sumario_produtos:
            sumario_produtos[nome_produto] = {
                'quantidade_total': 0,
                'faturamento_total': 0.0
            }

        # Adiciona a quantidade e o faturamento da venda atual aos totais do produto
        sumario_produtos[nome_produto]['quantidade_total'] += quantidade
        sumario_produtos[nome_produto]['faturamento_total'] += faturamento_item

    # Exibir os resultados
    print("\nSumário por Produto:")
    for produto, dados in sumario_produtos.items():
        print(f"- Produto: {produto}")
        print(f"  > Quantidade Total Vendida: {dados['quantidade_total']} unidades")
        print(f"  > Faturamento Total Gerado: R$ {dados['faturamento_total']:.2f}")
        print("-" * 30) # Linha divisória para clareza
    print("---------------------------------------------")