# banco_dados.py
import sqlite3

NOME_BANCO = 'vendas.db' # Nome do arquivo do banco de dados SQLite

def get_db_connection():
    """Estabelece e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(NOME_BANCO)
    # Opcional: configurar o row_factory para retornar linhas como dicionários (útil, mas podemos usar objetos Venda)
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela_vendas():
    """Cria a tabela 'vendas' se ela ainda não existir."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # O comando SQL para criar a tabela
    # INTEGER PRIMARY KEY AUTOINCREMENT: ID único, inteiro e gerado automaticamente pelo banco
    # TEXT: para strings (nome)
    # REAL: para números com casas decimais (preço)
    # INTEGER: para números inteiros (quantidade)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conn.commit() # Salva as mudanças no banco de dados
    conn.close() # Fecha a conexão com o banco
    print(f"Tabela 'vendas' verificada/criada no banco de dados '{NOME_BANCO}'.")

# Esta linha garante que a função criar_tabela_vendas seja chamada
# sempre que este módulo for importado ou executado diretamente.
criar_tabela_vendas()