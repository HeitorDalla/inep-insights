import pandas as pd
import streamlit as st
import plotly.express as px

# Função para mostrar a tela de infraestrutura
def infraestrutura (conn, nome_escola_marta, escola_selecionada):
    # Monta e executa SQL para selecionar todos os campos booleanos de infraestrutura
    em_inf_df = pd.read_sql(
        """
        SELECT
            sb.IN_PATIO_COBERTO           AS patio_coberto,
            sb.IN_BIBLIOTECA              AS biblioteca,
            sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
            sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
            sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
            sb.IN_PARQUE_INFANTIL         AS parque_infantil,
            sb.IN_SALA_PROFESSOR          AS sala_professor,
            sb.IN_COZINHA                 AS cozinha,
            sb.IN_REFEITORIO              AS refeitório,
            sb.IN_ALMOXARIFADO            AS almoxarifado,
            sb.IN_ALIMENTACAO             AS alimentacao
        FROM escola e
        JOIN infraestrutura sb
            ON sb.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """,
        conn,
        params=(nome_escola_marta,)  # Substitui %s pelo nome da escola de Marta
    )

    # Extrai indicadores de infraestrutura da escola selecionada
    if escola_selecionada:
        # Executa a mesma consulta, mas usando o nome da escola selecionada
        es_inf_df = pd.read_sql(
            """
            SELECT
                sb.IN_PATIO_COBERTO           AS patio_coberto,
                sb.IN_BIBLIOTECA              AS biblioteca,
                sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
                sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
                sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
                sb.IN_PARQUE_INFANTIL         AS parque_infantil,
                sb.IN_SALA_PROFESSOR          AS sala_professor,
                sb.IN_COZINHA                 AS cozinha,
                sb.IN_REFEITORIO              AS refeitório,
                sb.IN_ALMOXARIFADO            AS almoxarifado,
                sb.IN_ALIMENTACAO             AS alimentacao
            FROM escola e
            JOIN infraestrutura sb
                ON sb.escola_id = e.id
            WHERE e.NO_ENTIDADE = %s
            """,
            conn,
            params=(escola_selecionada,)
        )
    else:
        # Se não houver seleção, cria DataFrame vazio com as mesmas colunas
        es_inf_df = pd.DataFrame(columns=[
            "patio_coberto", "biblioteca", "laboratorio_ciencias",
            "laboratorio_informatica", "quadra_esportes", "parque_infantil",
            "sala_professor", "cozinha", "refeitório", "almoxarifado", "alimentacao"
        ])

    # Função auxiliar: converte 0 e 1 em 0.0 e 100.0 respectivamente
    def bool_to_pct(flag: int) -> float:
        return 100.0 if bool(flag) else 0.0

    # Calcula a porcentagem (100%: possui; 0%: não possui) das colunas (infraestruturas) da escola de Marta
    if not em_inf_df.empty:
        # Busca a primeira linha (índice 0) e converte o valor (booleano) em porcentagem (pct)
        em_patio_coberto_pct           = bool_to_pct(em_inf_df.loc[0, "patio_coberto"])
        em_biblioteca_pct              = bool_to_pct(em_inf_df.loc[0, "biblioteca"])
        em_laboratorio_ciencias_pct    = bool_to_pct(em_inf_df.loc[0, "laboratorio_ciencias"])
        em_laboratorio_informatica_pct = bool_to_pct(em_inf_df.loc[0, "laboratorio_informatica"])
        em_quadra_esportes_pct         = bool_to_pct(em_inf_df.loc[0, "quadra_esportes"])
        em_parque_infantil_pct         = bool_to_pct(em_inf_df.loc[0, "parque_infantil"])
        em_sala_professor_pct          = bool_to_pct(em_inf_df.loc[0, "sala_professor"])
        em_cozinha_pct                 = bool_to_pct(em_inf_df.loc[0, "cozinha"])
        em_refeitorio_pct              = bool_to_pct(em_inf_df.loc[0, "refeitório"])
        em_almoxarifado_pct            = bool_to_pct(em_inf_df.loc[0, "almoxarifado"])
        em_alimentacao_pct             = bool_to_pct(em_inf_df.loc[0, "alimentacao"])
    else:
        # Se DataFrame estiver vazio, define todos como 0.0
        em_patio_coberto_pct = em_biblioteca_pct = em_laboratorio_ciencias_pct = 0.0
        em_laboratorio_informatica_pct = em_quadra_esportes_pct = em_parque_infantil_pct = 0.0
        em_sala_professor_pct = em_cozinha_pct = em_refeitorio_pct = em_almoxarifado_pct = em_alimentacao_pct = 0.0

    # Calcula a porcentagem (100%: possui; 0%: não possui) das colunas (infraestruturas) da escola selecionada
    if not es_inf_df.empty:
        # Busca a primeira linha (índice 0) e converte o valor (booleano) em porcentagem (pct)
        es_patio_coberto_pct           = bool_to_pct(es_inf_df.loc[0, "patio_coberto"])
        es_biblioteca_pct              = bool_to_pct(es_inf_df.loc[0, "biblioteca"])
        es_laboratorio_ciencias_pct    = bool_to_pct(es_inf_df.loc[0, "laboratorio_ciencias"])
        es_laboratorio_informatica_pct = bool_to_pct(es_inf_df.loc[0, "laboratorio_informatica"])
        es_quadra_esportes_pct         = bool_to_pct(es_inf_df.loc[0, "quadra_esportes"])
        es_parque_infantil_pct         = bool_to_pct(es_inf_df.loc[0, "parque_infantil"])
        es_sala_professor_pct          = bool_to_pct(es_inf_df.loc[0, "sala_professor"])
        es_cozinha_pct                 = bool_to_pct(es_inf_df.loc[0, "cozinha"])
        es_refeitorio_pct              = bool_to_pct(es_inf_df.loc[0, "refeitório"])
        es_almoxarifado_pct            = bool_to_pct(es_inf_df.loc[0, "almoxarifado"])
        es_alimentacao_pct             = bool_to_pct(es_inf_df.loc[0, "alimentacao"])
    else:
        # Se não houver seleção, define todos como 0.0
        es_patio_coberto_pct = es_biblioteca_pct = es_laboratorio_ciencias_pct = 0.0
        es_laboratorio_informatica_pct = es_quadra_esportes_pct = es_parque_infantil_pct = 0.0
        es_sala_professor_pct = es_cozinha_pct = es_refeitorio_pct = es_almoxarifado_pct = es_alimentacao_pct = 0.0

    # Cria um layout de duas colunas no Streamlit, atribuídas às variáveis col1 (esquerda) e col2 (direita)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <h1>Escola de Marta</h1>
        """,
        unsafe_allow_html=True)
        st.markdown(f"""
            <p>{nome_escola_marta}</p>
        """,
        unsafe_allow_html=True)

        # Exibe cada KPI como um cartão métrico
        st.metric("Pátio Coberto",       f"{em_patio_coberto_pct:.0f}%", border=True)
        st.metric("Biblioteca",          f"{em_biblioteca_pct:.0f}%", border=True)
        st.metric("Lab. Ciências",       f"{em_laboratorio_ciencias_pct:.0f}%", border=True)
        st.metric("Lab. Informática",    f"{em_laboratorio_informatica_pct:.0f}%", border=True)
        st.metric("Quadra de Esportes",  f"{em_quadra_esportes_pct:.0f}%", border=True)
        st.metric("Parque Infantil",     f"{em_parque_infantil_pct:.0f}%", border=True)
        st.metric("Sala dos Professores",f"{em_sala_professor_pct:.0f}%", border=True)
        st.metric("Cozinha",             f"{em_cozinha_pct:.0f}%", border=True)
        st.metric("Refeitório",          f"{em_refeitorio_pct:.0f}%", border=True)
        st.metric("Almoxarifado",        f"{em_almoxarifado_pct:.0f}%", border=True)
        st.metric("Alimentação",         f"{em_alimentacao_pct:.0f}%", border=True)

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
            # Exibe KPIs para a escola escolhida
            st.metric("Pátio Coberto",       f"{es_patio_coberto_pct:.0f}%", border=True)
            st.metric("Biblioteca",          f"{es_biblioteca_pct:.0f}%", border=True)
            st.metric("Lab. Ciências",       f"{es_laboratorio_ciencias_pct:.0f}%", border=True)
            st.metric("Lab. Informática",    f"{es_laboratorio_informatica_pct:.0f}%", border=True)
            st.metric("Quadra de Esportes",  f"{es_quadra_esportes_pct:.0f}%", border=True)
            st.metric("Parque Infantil",     f"{es_parque_infantil_pct:.0f}%", border=True)
            st.metric("Sala dos Professores",f"{es_sala_professor_pct:.0f}%", border=True)
            st.metric("Cozinha",             f"{es_cozinha_pct:.0f}%", border=True)
            st.metric("Refeitório",          f"{es_refeitorio_pct:.0f}%", border=True)
            st.metric("Almoxarifado",        f"{es_almoxarifado_pct:.0f}%", border=True)
            st.metric("Alimentação",         f"{es_alimentacao_pct:.0f}%", border=True)
        else:
            # Caso não haja escola selecionada, exibe mensagem de orientação
            st.write("Por favor, selecione uma escola válida para ver os KPIs.")

    # SQL para Marta
    em_qt_transporte_df = pd.read_sql("""
    SELECT i.QT_TRANSP_PUBLICO AS transporte
    FROM escola e
    JOIN infraestrutura i
        ON i.escola_id = e.id
    WHERE e.NO_ENTIDADE = %s
    """, conn, params=(nome_escola_marta,))

    # SQL para escola selecionada
    # es_qt_transporte_df = pd.DataFrame()
    if escola_selecionada:
        es_qt_tranporte_df = pd.read_sql("""
            SELECT i.QT_TRANSP_PUBLICO AS transporte
            FROM escola e
            JOIN infraestrutura i 
                ON i.escola_id = e.id
            WHERE e.NO_ENTIDADE = %s
        """, conn, params=(escola_selecionada,))

    em_qt_transporte = int(em_qt_transporte_df.loc[0, "transporte"]) if not em_qt_transporte_df.empty else 0
    es_qt_transporte = int(es_qt_tranporte_df.loc[0, "transporte"]) if not es_qt_tranporte_df.empty else 0

    df_bar = pd.DataFrame({
        "escola":     [nome_escola_marta, escola_selecionada or "Nenhuma selecionada"],
        "transporte": [em_qt_transporte,  es_qt_transporte]
    })

    fig = px.bar(
        df_bar,
        x="escola",
        y="transporte",
        text="transporte",
        title="Comparativo entre escolas ─ Quantidade de transporte",
        labels={"escola": "Escola", "transporte": "Qtd. Transporte"}
    )

    fig.update_yaxes(range=[0, 300])
    fig.update_layout(
        xaxis_title="Escola",
        yaxis_title="Qtd. Transporte",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)