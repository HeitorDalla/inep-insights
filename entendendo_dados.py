import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector

# Função para conexão com o banco de dados
def getConnection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='database_projeto_tcs'
    )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

# Cria conexão com o banco de dados MySQL
conn, cursor = getConnection()

# Estudo dos Dados

# Entendendo o dataset
tabelas = [
    "regiao",
    "uf",
    "municipio",
    "tipo_localizacao",
    "escola",
    "saneamento_basico",
    "infraestrutura",
    "corpo_docente",
    "matriculas",
    "materiais"
]

for tabela in tabelas:
    query = f'select * from {tabela}'
    df = pd.read_sql(query, conn)
    st.subheader(f'Tabela: {tabela}')
    st.dataframe(df)
    
    st.write(df.describe())

# Comparações com Gráficos

st.write('Comparativo de agua_potavel e energia_rede_publica para escolas urbanas e rurais')
query1 = '''
SELECT
    tl.descricao AS localizacao,
    AVG(sb.IN_AGUA_POTAVEL) * 100 AS porcentagem_agua_potavel,
    AVG(sb.IN_ENERGIA_REDE_PUBLICA) * 100 AS porcentagem_energia
FROM escola e
JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
JOIN saneamento_basico sb ON e.id = sb.escola_id
GROUP BY tl.descricao
'''
df_localizacao = pd.read_sql(query1, conn)
st.bar_chart(df_localizacao.set_index("localizacao"))
st.write('Resultado: \nComparativo de porcentagens de agua potavel - 10% a menos das pessoas não tem água potável nas zonas rurais, podendo prejudicar na saúde. \nComparativo de energia de rede publica - Diferença de 10% a menos para as zonas rurais.')

st.write("Comparativo dos tipos de águas das zonas urbanas e rurais")
query2 = '''
SELECT 
    tl.descricao AS agua,
    AVG(sb.IN_AGUA_POTAVEL) * 100 AS porcentagem_agua_potavel,
    AVG(sb.IN_AGUA_INEXISTENTE) * 100 AS porcentagem_agua_inexistente,
    AVG(sb.IN_AGUA_POCO_ARTESIANO) * 100 AS porcentagem_agua_artesiana,
    AVG(sb.IN_AGUA_REDE_PUBLICA) * 100 AS porcentagem_agua_publica
FROM escola e
JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
JOIN saneamento_basico sb ON e.id = sb.escola_id
GROUP BY tl.descricao
'''
df_agua = pd.read_sql(query2, conn)
st.bar_chart(df_agua.set_index("agua"))
st.write("Resultado: ")

st.write('Comparativo de rede de esgoto para rural e urbano')
query3 = '''
select
	tl.descricao as esgoto,
    avg(sb.IN_ESGOTO_REDE_PUBLICA) * 100 as porcentagem_esgoto_rede_publica
from escola e
inner join tipo_localizacao tl on e.tp_localizacao_id = tl.id
inner join saneamento_basico sb on e.id = sb.escola_id
group by tl.descricao;
'''
df_esgoto = pd.read_sql(query3, conn)
st.bar_chart(df_esgoto.set_index('esgoto'))
st.write('Resultado = Independente da região, vai ter extratofericamente mais de em áreas urbanas')

st.write("Comparativo de energia entre as áreas urbanas e rural")
query4 = '''
select
	tl.descricao as energia,
    avg(sb.IN_ENERGIA_REDE_PUBLICA) * 100 as porcentagem_energia_rede_publica
from escola e
inner join tipo_localizacao tl on e.tp_localizacao_id = tl.id
inner join saneamento_basico sb on e.id = sb.escola_id
group by tl.descricao;
'''
df_energia = pd.read_sql(query4, conn)
st.bar_chart(df_energia.set_index('energia'))
st.write("Resultado = Pouca diferença de energia de rede publica para redes urbanas e rurais, mas ainda sim, significativo")

st.write("Comparativo de lixo entre as áreas urbanas e rural")
query5 = '''
select
	tl.descricao as lixo,
    avg(sb.IN_LIXO_SERVICO_COLETA) * 100 as porcentagem_lixo_servico_coleta
from escola e
inner join tipo_localizacao tl on e.tp_localizacao_id = tl.id
inner join saneamento_basico sb on e.id = sb.escola_id
group by tl.descricao;	
'''
df_lixo = pd.read_sql(query5, conn)
st.bar_chart(df_lixo.set_index('lixo'))
st.write("Resultado = Grande diferença entre a coleta de lixo entre as áreas urbanas e rural, significando que existe desigualdade em recursos básicos (quem dirá algo tecnológico), impactando diretamente em áreas como infraestrutura, educação e saúde. Significa que o governo não consegue suprir e atender essas áreas, aumentando na contaminação do ar, solo e água, impactando ainda mais em outros fatores. ")

st.write("Comparativo de utilizacao de transporte publico pelas escolas rurais e urbanas")
query6 = '''
select
	tl.descricao as transporte,
    round(avg(i.QT_TRANSP_PUBLICO), 2) as quantidade_transporte_publico
from escola e
inner join tipo_localizacao tl on e.tp_localizacao_id = tl.id
inner join infraestrutura i on i.escola_id = e.id
group by tl.descricao;
'''
df_transporte = pd.read_sql(query6, conn)
st.bar_chart(df_transporte.set_index('transporte'))
st.write("Resultado: ")

conn.close() # fecha conexão com o banco de dados