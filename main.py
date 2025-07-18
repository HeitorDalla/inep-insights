# Importa a função que carrega e trata os dados da etapa de pré-processamento
from src.data.dados_tratados import dados_tratados

# Importa a função que inicializa a conexão com o banco de dados e retorna o cursor
from src.database.inicializar_database import inicializar_database

# Executa a função dados_tratados(dados.csv) que:
# - Carregamos os dados brutos do CSV
# - Realizamos a  limpeza (remoção de nulos, normalização de strings, etc.)
# - Organizamos as colunas que serão usadas para popular o banco
# Resultado: retorna um DataFrame pandas com as colunas tratadas e estruturadas
dados = dados_tratados()

# Inicializa a conexão com o banco de dados MySQL e cria o cursor.
# Essa função:
# - Estabelece a conexão (conn) 
# - Cria um cursor para executar comandos SQL (cursor)
conn, cursor = inicializar_database()