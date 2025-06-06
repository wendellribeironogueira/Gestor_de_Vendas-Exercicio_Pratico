# 📊 Gestor de Vendas em Python (Com SQLite)

Este é um projeto prático desenvolvido em Python para gerenciar registros de vendas, permitindo operações de adição, listagem, edição e remoção de produtos, além de funcionalidades de análise básica de vendas.

O projeto foi refatorado de um sistema baseado em arquivos JSON para utilizar um **banco de dados SQLite**, demonstrando a integração do Python com SQL para persistência de dados mais robusta e escalável.

## ✨ Funcionalidades

* **Adicionar Venda:** Registra novas vendas com nome do produto, preço unitário e quantidade.
* **Listar Vendas:** Exibe todas as vendas registradas com seus detalhes, incluindo o ID do banco de dados.
* **Editar Venda:** Permite atualizar o preço e/ou a quantidade de uma venda existente.
* **Remover Venda:** Exclui um registro de venda do sistema.
* **Análises de Vendas:**
    * Cálculo do faturamento total.
    * Detalhamento do faturamento por item.
    * Contagem de produtos de baixo custo (preço <= R$50,00).
    * Identificação de itens vendidos acima da média de quantidade.
    * Análise detalhada por produto (total vendido, faturamento).

## 🚀 Tecnologias Utilizadas

* **Python 3.x:** Linguagem de programação principal.
* **SQLite3:** Módulo padrão do Python para interagir com bancos de dados SQLite (banco de dados embutido baseado em arquivo).
* **JSON (para migração):** Utilizado temporariamente para a migração de dados de um formato anterior para o banco de dados.

## 📁 Estrutura do Projeto
gestor-de-vendas/
├── main.py
├── analises_vendas.py
├── banco_dados.py
├── vendas.db      (Gerado após a primeira execução)
├── vendas.json    (Opcional: arquivo de dados JSON antigo, para migração)
└── migrar_dados.py (Opcional: script para migração de dados do JSON para o DB)
└── README.md

## ⚙️ Como Executar o Projeto

### Pré-requisitos

* Python 3.x instalado.

### Passos

1.  **Clone o repositório** (ou baixe os arquivos diretamente) para o seu ambiente local:
    ```bash
    git clone [https://github.com/SEU_USUARIO/gestor-de-vendas.git](https://github.com/SEU_USUARIO/gestor-de-vendas.git)
    cd gestor-de-vendas
    ```
2.  **Crie o banco de dados (primeira execução):**
    Ao executar `main.py` pela primeira vez, o arquivo `vendas.db` será criado automaticamente na mesma pasta, junto com a tabela `vendas`.
    ```bash
    python main.py
    ```
3.  **Migrar dados existentes (opcional):**
    Se você possuir um arquivo `vendas.json` com dados de vendas da versão anterior do projeto e desejar importá-los para o `vendas.db`, execute o script de migração **uma única vez**:
    ```bash
    python migrar_dados.py
    ```
    *Obs: Após a migração, você pode apagar ou ignorar `migrar_dados.py`.*

4.  **Executar o Gestor de Vendas:**
    Inicie o programa principal para interagir com o sistema através do menu:
    ```bash
    python main.py
    ```

## 🤝 Contribuições

Contribuições são bem-vindas! Se você tiver sugestões, melhorias ou encontrar bugs, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📝 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.