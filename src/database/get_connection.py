import mysql.connector

# Função para fazer a conexão com o banco de dados
def get_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='database_projeto_tcs'
    )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor