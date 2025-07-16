from src.data.data import dados
from unidecode import unidecode

# Função para tratar os dados
def dados_tratados ():
    # Carregando os dados
    df = dados()

    # Remove os valores ausentes
    df_limpo = df.dropna()

    # Remove os outliers
    df_limpo = df_limpo[~df_limpo.isin([88888.0]).any(axis=1)]

    # Normalizar as colunas de texto
    colunas_para_normalizar = ['NO_REGIAO', 'NO_UF', 'NO_MUNICIPIO', 'NO_ENTIDADE']
    for coluna in colunas_para_normalizar:
        if coluna in df_limpo.columns:
            df_limpo[coluna] = df_limpo[coluna].astype(str).apply(unidecode)
    
    return df_limpo