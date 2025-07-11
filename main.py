from modules.data import dados_tratados
from modules.database import inicializar_database

dados = dados_tratados()

conn, cursor = inicializar_database()