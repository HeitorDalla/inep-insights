import pandas as pd
import streamlit as st

# Função para mostrar a tela de Saneamento Básico
def saneamento_basico (conn, nome_escola_marta, escola_selecionada):
    # Executa uma query SQL e retorna um DataFrame
    em_df = pd.read_sql("""
        SELECT
            sb.IN_AGUA_POTAVEL         AS agua_potavel,
            sb.IN_AGUA_REDE_PUBLICA    AS agua_rede_publica,
            sb.IN_AGUA_POCO_ARTESIANO  AS agua_poco_artesiano,
            sb.IN_AGUA_INEXISTENTE     AS agua_inexistente,
            sb.IN_ESGOTO_REDE_PUBLICA  AS esgoto_rede_publica,
            sb.IN_ESGOTO_INEXISTENTE   AS esgoto_inexistente,
            sb.IN_ENERGIA_REDE_PUBLICA AS energia_rede_publica,
            sb.IN_ENERGIA_INEXISTENTE  AS energia_inexistente,
            sb.IN_LIXO_SERVICO_COLETA  AS lixo_servico_coleta
        FROM escola e
        JOIN saneamento_basico sb 
            ON sb.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
    """, conn, params=(nome_escola_marta,))
    # SELECT: seleciona todos os indicadores booleanos de saneamento e renomeia cada coluna para algo mais legível 
    
    # JOIN: liga a tabela "escola" (e) à tabela saneamento_basico (sb) via escola.id

    # WHERE … = %s: filtra apenas pela escola cujo nome é igual ao nome da variável "nome_escola_marta"

    # params=(nome_escola_marta,): passa o nome da variável "nome_escola_marta" como parâmetro para a query SQL

    if escola_selecionada:
    # Se o usuário já tiver escolhido uma escola via sidebar, executa a mesma query acima, mas passando o nome da escola selecionada, e guarda o resultado em outro DataFrame.
        es_df = pd.read_sql("""
            SELECT
                sb.IN_AGUA_POTAVEL         AS agua_potavel,
                sb.IN_AGUA_REDE_PUBLICA    AS agua_rede_publica,
                sb.IN_AGUA_POCO_ARTESIANO  AS agua_poco_artesiano,
                sb.IN_AGUA_INEXISTENTE     AS agua_inexistente,
                sb.IN_ESGOTO_REDE_PUBLICA  AS esgoto_rede_publica,
                sb.IN_ESGOTO_INEXISTENTE   AS esgoto_inexistente,
                sb.IN_ENERGIA_REDE_PUBLICA AS energia_rede_publica,
                sb.IN_ENERGIA_INEXISTENTE  AS energia_inexistente,
                sb.IN_LIXO_SERVICO_COLETA  AS lixo_servico_coleta
            FROM escola e
            JOIN saneamento_basico sb 
                ON sb.escola_id = e.id
            WHERE e.NO_ENTIDADE = %s
        """, conn, params=(escola_selecionada,))
    else:
        # Caso contrário, cria um DataFrame vazio com as mesmas colunas, para evitar erros posteriores ao tentar acessar índices inexistentes.
        es_df = pd.DataFrame(columns=[
            "agua_potavel", "agua_rede_publica", "agua_poco_artesiano", "agua_inexistente",
            "esgoto_rede_publica", "esgoto_inexistente",
            "energia_rede_publica", "energia_inexistente",
            "lixo_servico_coleta"
        ])

    # Função auxiliar que recebe um valor 0 ou 1 e devolve 0.0 ou 100.0 respectivamente
    def bool_to_pct(flag: int) -> float:
        # Primeiro converte para bool (0 → False; 1 → True), depois escolhe o percentual correspondente (True → 100.0; False → 0.0)
        return 100.0 if bool(flag) else 0.0

    if not em_df.empty:
        # Verifica se "em_df" não está vazio): se não estiver, extrai cada um dos campos na primeira linha (loc[0, "..."])

        # Para os indicadores de “inexistente” (água, esgoto e energia), inverte-se o valor com (1 - <flag>) para mostrar a disponibilidade

        # Passa tudo pela função "bool_to_pct" para obter 0.0 ou 100.0
        em_agua_potavel_pct        = bool_to_pct(em_df.loc[0, "agua_potavel"])
        em_agua_rede_publica_pct   = bool_to_pct(em_df.loc[0, "agua_rede_publica"])
        em_agua_poco_artesiano_pct = bool_to_pct(em_df.loc[0, "agua_poco_artesiano"])
        em_agua_inexistente_pct    = bool_to_pct(1 - em_df.loc[0, "agua_inexistente"])
        em_esgoto_rede_publica_pct = bool_to_pct(em_df.loc[0, "esgoto_rede_publica"])
        em_esgoto_inexistente_pct  = bool_to_pct(1 - em_df.loc[0, "esgoto_inexistente"])
        em_energia_rede_publica_pct= bool_to_pct(em_df.loc[0, "energia_rede_publica"])
        em_energia_inexistente_pct = bool_to_pct(1 - em_df.loc[0, "energia_inexistente"])
        em_lixo_servico_coleta_pct = bool_to_pct(em_df.loc[0, "lixo_servico_coleta"])
    else:
        # Se "em_df" estiver vazio, atribui 0.0 a todas as variáveis de percentuais de Marta
        em_agua_potavel_pct = em_agua_rede_publica_pct = em_agua_poco_artesiano_pct = 0.0
        em_agua_inexistente_pct = em_esgoto_rede_publica_pct = em_esgoto_inexistente_pct = 0.0
        em_energia_rede_publica_pct = em_energia_inexistente_pct = em_lixo_servico_coleta_pct = 0.0
    
    # Idêntico ao bloco anterior, mas para a escola selecionada
    if not es_df.empty:
        es_agua_potavel_pct        = bool_to_pct(es_df.loc[0, "agua_potavel"])
        es_agua_rede_publica_pct   = bool_to_pct(es_df.loc[0, "agua_rede_publica"])
        es_agua_poco_artesiano_pct = bool_to_pct(es_df.loc[0, "agua_poco_artesiano"])
        es_agua_inexistente_pct    = bool_to_pct(1 - es_df.loc[0, "agua_inexistente"])
        es_esgoto_rede_publica_pct = bool_to_pct(es_df.loc[0, "esgoto_rede_publica"])
        es_esgoto_inexistente_pct  = bool_to_pct(1 - es_df.loc[0, "esgoto_inexistente"])
        es_energia_rede_publica_pct= bool_to_pct(es_df.loc[0, "energia_rede_publica"])
        es_energia_inexistente_pct = bool_to_pct(1 - es_df.loc[0, "energia_inexistente"])
        es_lixo_servico_coleta_pct = bool_to_pct(es_df.loc[0, "lixo_servico_coleta"])
    else:
        es_agua_potavel_pct = es_agua_rede_publica_pct = es_agua_poco_artesiano_pct = 0.0
        es_agua_inexistente_pct = es_esgoto_rede_publica_pct = es_esgoto_inexistente_pct = 0.0
        es_energia_rede_publica_pct = es_energia_inexistente_pct = es_lixo_servico_coleta_pct = 0.0

    # Cria um layout de duas colunas iguais no Streamlit, atribuídas às variáveis col1 (esquerda) e col2 (direita)
    col1, col2 = st.columns(2)

    # Injeta CSS p/ centralizar <h1/> e <p/> (mover para assets/style.py)
    st.markdown("""
        <style>
            h1, p {
                text-align: center;
            }       
        </style>
    """, unsafe_allow_html=True)

    # st.metric: para cada indicador, exibe um cartão com rótulo e valor formatado (:.0f)
    with col1:
        st.markdown("""
            <h1>Escola de Marta</h1>
        """,
        unsafe_allow_html=True)
        st.markdown(f"""
            <p>{nome_escola_marta}</p>
        """,
        unsafe_allow_html=True)
        st.metric("Água Potável",             f"{em_agua_potavel_pct:.0f}%", border=True)
        st.metric("Água Rede Pública",        f"{em_agua_rede_publica_pct:.0f}%", border=True)
        st.metric("Poço Artesiano",           f"{em_agua_poco_artesiano_pct:.0f}%", border=True)
        st.metric("Esgoto Disponível",        f"{em_esgoto_inexistente_pct:.0f}%", border=True)
        st.metric("Esgoto Rede Pública",      f"{em_esgoto_rede_publica_pct:.0f}%", border=True)
        st.metric("Energia Disponível",       f"{em_energia_inexistente_pct:.0f}%", border=True)
        st.metric("Energia Rede Pública",     f"{em_energia_rede_publica_pct:.0f}%", border=True)
        st.metric("Coleta de Lixo",           f"{em_lixo_servico_coleta_pct:.0f}%", border=True)

    with col2:
        st.markdown("""
            <h1>Escola selecionada</h1>
        """,
        unsafe_allow_html=True)
        st.markdown(f"""
            <p>{escola_selecionada}</p>
        """,
        unsafe_allow_html=True)
        if escola_selecionada:
            st.metric("Água Potável",         f"{es_agua_potavel_pct:.0f}%", border=True)
            st.metric("Água Rede Pública",    f"{es_agua_rede_publica_pct:.0f}%", border=True)
            st.metric("Poço Artesiano",       f"{es_agua_poco_artesiano_pct:.0f}%", border=True)
            st.metric("Esgoto Disponível",    f"{es_esgoto_inexistente_pct:.0f}%", border=True)
            st.metric("Esgoto Rede Pública",  f"{es_esgoto_rede_publica_pct:.0f}%", border=True)
            st.metric("Energia Disponível",   f"{es_energia_inexistente_pct:.0f}%", border=True)
            st.metric("Energia Rede Pública", f"{es_energia_rede_publica_pct:.0f}%", border=True)
            st.metric("Coleta de Lixo",       f"{es_lixo_servico_coleta_pct:.0f}%", border=True)
        else:
            st.write("Por favor, selecione uma escola válida.")