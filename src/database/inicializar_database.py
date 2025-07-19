# Importações necessárias para inicialização do banco de dados
from src.database.get_connection import get_connection   # Função para estabelecer conexão com o banco
from src.database.create_database import create_database  # Função para criar as tabelas do banco
from src.database.populate_database import populate_database  # Função para popular o banco com dados iniciais


# Inicializa o banco de dados do sistema.
    # Esta função executa o processo completo de inicialização do banco de dados:
    # 1. Estabelece conexão com o banco de dados
    # 2. Cria as tabelas necessárias (se não existirem)
    # 3. Popula o banco com dados iniciais

# Função para inicializar o banco de dados
def inicializar_database ():
    
    conn, cursor = get_connection() # Estabelece conexão com o banco de dados
    create_database(conn, cursor) # Cria as tabelas do banco de dados (caso não existam)
    populate_database(conn, cursor) # Popula o banco com dados iniciais necessários para o funcionamento do sistema

    # Retorna a conexão e cursor para uso posterior 
    return conn, cursor