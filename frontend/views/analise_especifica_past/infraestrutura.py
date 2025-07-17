# # import pandas as pd
# # import streamlit as st
# # import plotly.express as px

# # # Função para mostrar a tela de infraestrutura
# # def infraestrutura (conn, nome_escola_marta, escola_selecionada):
# #     # Monta e executa SQL para selecionar todos os campos booleanos de infraestrutura
# #     em_inf_df = pd.read_sql(
# #         """
# #         SELECT
# #             sb.IN_PATIO_COBERTO           AS patio_coberto,
# #             sb.IN_BIBLIOTECA              AS biblioteca,
# #             sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
# #             sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
# #             sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
# #             sb.IN_PARQUE_INFANTIL         AS parque_infantil,
# #             sb.IN_SALA_PROFESSOR          AS sala_professor,
# #             sb.IN_COZINHA                 AS cozinha,
# #             sb.IN_REFEITORIO              AS refeitório,
# #             sb.IN_ALMOXARIFADO            AS almoxarifado,
# #             sb.IN_ALIMENTACAO             AS alimentacao
# #         FROM escola e
# #         JOIN infraestrutura sb
# #             ON sb.escola_id = e.id
# #         WHERE e.NO_ENTIDADE = %s
# #         """,
# #         conn,
# #         params=(nome_escola_marta,)  # Substitui %s pelo nome da escola de Marta
# #     )

# #     # Extrai indicadores de infraestrutura da escola selecionada
# #     if escola_selecionada:
# #         # Executa a mesma consulta, mas usando o nome da escola selecionada
# #         es_inf_df = pd.read_sql(
# #             """
# #             SELECT
# #                 sb.IN_PATIO_COBERTO           AS patio_coberto,
# #                 sb.IN_BIBLIOTECA              AS biblioteca,
# #                 sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
# #                 sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
# #                 sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
# #                 sb.IN_PARQUE_INFANTIL         AS parque_infantil,
# #                 sb.IN_SALA_PROFESSOR          AS sala_professor,
# #                 sb.IN_COZINHA                 AS cozinha,
# #                 sb.IN_REFEITORIO              AS refeitório,
# #                 sb.IN_ALMOXARIFADO            AS almoxarifado,
# #                 sb.IN_ALIMENTACAO             AS alimentacao
# #             FROM escola e
# #             JOIN infraestrutura sb
# #                 ON sb.escola_id = e.id
# #             WHERE e.NO_ENTIDADE = %s
# #             """,
# #             conn,
# #             params=(escola_selecionada,)
# #         )
# #     else:
# #         # Se não houver seleção, cria DataFrame vazio com as mesmas colunas
# #         es_inf_df = pd.DataFrame(columns=[
# #             "patio_coberto", "biblioteca", "laboratorio_ciencias",
# #             "laboratorio_informatica", "quadra_esportes", "parque_infantil",
# #             "sala_professor", "cozinha", "refeitório", "almoxarifado", "alimentacao"
# #         ])

# #     # Função auxiliar: converte 0 e 1 em 0.0 e 100.0 respectivamente
# #     def bool_to_pct(flag: int) -> float:
# #         return 100.0 if bool(flag) else 0.0

# #     # Calcula a porcentagem (100%: possui; 0%: não possui) das colunas (infraestruturas) da escola de Marta
# #     if not em_inf_df.empty:
# #         # Busca a primeira linha (índice 0) e converte o valor (booleano) em porcentagem (pct)
# #         em_patio_coberto_pct           = bool_to_pct(em_inf_df.loc[0, "patio_coberto"])
# #         em_biblioteca_pct              = bool_to_pct(em_inf_df.loc[0, "biblioteca"])
# #         em_laboratorio_ciencias_pct    = bool_to_pct(em_inf_df.loc[0, "laboratorio_ciencias"])
# #         em_laboratorio_informatica_pct = bool_to_pct(em_inf_df.loc[0, "laboratorio_informatica"])
# #         em_quadra_esportes_pct         = bool_to_pct(em_inf_df.loc[0, "quadra_esportes"])
# #         em_parque_infantil_pct         = bool_to_pct(em_inf_df.loc[0, "parque_infantil"])
# #         em_sala_professor_pct          = bool_to_pct(em_inf_df.loc[0, "sala_professor"])
# #         em_cozinha_pct                 = bool_to_pct(em_inf_df.loc[0, "cozinha"])
# #         em_refeitorio_pct              = bool_to_pct(em_inf_df.loc[0, "refeitório"])
# #         em_almoxarifado_pct            = bool_to_pct(em_inf_df.loc[0, "almoxarifado"])
# #         em_alimentacao_pct             = bool_to_pct(em_inf_df.loc[0, "alimentacao"])
# #     else:
# #         # Se DataFrame estiver vazio, define todos como 0.0
# #         em_patio_coberto_pct = em_biblioteca_pct = em_laboratorio_ciencias_pct = 0.0
# #         em_laboratorio_informatica_pct = em_quadra_esportes_pct = em_parque_infantil_pct = 0.0
# #         em_sala_professor_pct = em_cozinha_pct = em_refeitorio_pct = em_almoxarifado_pct = em_alimentacao_pct = 0.0

# #     # Calcula a porcentagem (100%: possui; 0%: não possui) das colunas (infraestruturas) da escola selecionada
# #     if not es_inf_df.empty:
# #         # Busca a primeira linha (índice 0) e converte o valor (booleano) em porcentagem (pct)
# #         es_patio_coberto_pct           = bool_to_pct(es_inf_df.loc[0, "patio_coberto"])
# #         es_biblioteca_pct              = bool_to_pct(es_inf_df.loc[0, "biblioteca"])
# #         es_laboratorio_ciencias_pct    = bool_to_pct(es_inf_df.loc[0, "laboratorio_ciencias"])
# #         es_laboratorio_informatica_pct = bool_to_pct(es_inf_df.loc[0, "laboratorio_informatica"])
# #         es_quadra_esportes_pct         = bool_to_pct(es_inf_df.loc[0, "quadra_esportes"])
# #         es_parque_infantil_pct         = bool_to_pct(es_inf_df.loc[0, "parque_infantil"])
# #         es_sala_professor_pct          = bool_to_pct(es_inf_df.loc[0, "sala_professor"])
# #         es_cozinha_pct                 = bool_to_pct(es_inf_df.loc[0, "cozinha"])
# #         es_refeitorio_pct              = bool_to_pct(es_inf_df.loc[0, "refeitório"])
# #         es_almoxarifado_pct            = bool_to_pct(es_inf_df.loc[0, "almoxarifado"])
# #         es_alimentacao_pct             = bool_to_pct(es_inf_df.loc[0, "alimentacao"])
# #     else:
# #         # Se não houver seleção, define todos como 0.0
# #         es_patio_coberto_pct = es_biblioteca_pct = es_laboratorio_ciencias_pct = 0.0
# #         es_laboratorio_informatica_pct = es_quadra_esportes_pct = es_parque_infantil_pct = 0.0
# #         es_sala_professor_pct = es_cozinha_pct = es_refeitorio_pct = es_almoxarifado_pct = es_alimentacao_pct = 0.0

# #     # Cria um layout de duas colunas no Streamlit, atribuídas às variáveis col1 (esquerda) e col2 (direita)
# #     col1, col2 = st.columns(2)

# #     with col1:
# #         st.markdown("""
# #             <h1>Escola de Marta</h1>
# #         """,
# #         unsafe_allow_html=True)
# #         st.markdown(f"""
# #             <p>{nome_escola_marta}</p>
# #         """,
# #         unsafe_allow_html=True)

# #         # Exibe cada KPI como um cartão métrico
# #         st.metric("Laboratório de Informática",    f"{em_laboratorio_informatica_pct:.0f}%", border=True)
# #         st.metric("Laboratório de Ciências",       f"{em_laboratorio_ciencias_pct:.0f}%", border=True)
# #         st.metric("Biblioteca",          f"{em_biblioteca_pct:.0f}%", border=True)
# #         st.metric("Pátio Coberto",       f"{em_patio_coberto_pct:.0f}%", border=True)
# #         st.metric("Parque Infantil",     f"{em_parque_infantil_pct:.0f}%", border=True)
# #         st.metric("Quadra de Esportes",  f"{em_quadra_esportes_pct:.0f}%", border=True)
# #         # st.metric("Sala dos Professores",f"{em_sala_professor_pct:.0f}%", border=True)
# #         st.metric("Cozinha",             f"{em_cozinha_pct:.0f}%", border=True)
# #         st.metric("Refeitório",          f"{em_refeitorio_pct:.0f}%", border=True)
# #         # st.metric("Almoxarifado",        f"{em_almoxarifado_pct:.0f}%", border=True)
# #         # st.metric("Alimentação",         f"{em_alimentacao_pct:.0f}%", border=True)

# #     with col2:
# #         st.markdown("""
# #             <h1>Escola selecionada</h1>
# #         """,
# #         unsafe_allow_html=True)
# #         st.markdown(f"""
# #             <p>{escola_selecionada}</p>
# #         """,
# #         unsafe_allow_html=True)
# #         if escola_selecionada:
# #             # Exibe KPIs para a escola escolhida
# #             st.metric("Laboratório de Informática",    f"{es_laboratorio_informatica_pct:.0f}%", border=True)
# #             st.metric("Laboratório de Ciências",       f"{es_laboratorio_ciencias_pct:.0f}%", border=True)
# #             st.metric("Pátio Coberto",       f"{es_patio_coberto_pct:.0f}%", border=True)
# #             st.metric("Biblioteca",          f"{es_biblioteca_pct:.0f}%", border=True)
# #             st.metric("Parque Infantil",     f"{es_parque_infantil_pct:.0f}%", border=True)
# #             st.metric("Quadra de Esportes",  f"{es_quadra_esportes_pct:.0f}%", border=True)
# #             # st.metric("Sala dos Professores",f"{es_sala_professor_pct:.0f}%", border=True)
# #             st.metric("Cozinha",             f"{es_cozinha_pct:.0f}%", border=True)
# #             st.metric("Refeitório",          f"{es_refeitorio_pct:.0f}%", border=True)
# #             # st.metric("Almoxarifado",        f"{es_almoxarifado_pct:.0f}%", border=True)
# #             # st.metric("Alimentação",         f"{es_alimentacao_pct:.0f}%", border=True)
# #         else:
# #             # Caso não haja escola selecionada, exibe mensagem de orientação
# #             st.write("Por favor, selecione uma escola válida para ver os KPIs.")

# #     # SQL para Marta
# #     em_qt_transporte_df = pd.read_sql("""
# #     SELECT i.QT_TRANSP_PUBLICO AS transporte
# #     FROM escola e
# #     JOIN infraestrutura i
# #         ON i.escola_id = e.id
# #     WHERE e.NO_ENTIDADE = %s
# #     """, conn, params=(nome_escola_marta,))

# #     # SQL para escola selecionada
# #     # es_qt_transporte_df = pd.DataFrame()
# #     if escola_selecionada:
# #         es_qt_tranporte_df = pd.read_sql("""
# #             SELECT i.QT_TRANSP_PUBLICO AS transporte
# #             FROM escola e
# #             JOIN infraestrutura i 
# #                 ON i.escola_id = e.id
# #             WHERE e.NO_ENTIDADE = %s
# #         """, conn, params=(escola_selecionada,))

# #     em_qt_transporte = int(em_qt_transporte_df.loc[0, "transporte"]) if not em_qt_transporte_df.empty else 0
# #     es_qt_transporte = int(es_qt_tranporte_df.loc[0, "transporte"]) if not es_qt_tranporte_df.empty else 0

# #     df_bar = pd.DataFrame({
# #         "escola":     [nome_escola_marta, escola_selecionada or "Nenhuma selecionada"],
# #         "transporte": [em_qt_transporte,  es_qt_transporte]
# #     })

# #     fig = px.bar(
# #         df_bar,
# #         x="escola",
# #         y="transporte",
# #         text="transporte",
# #         title="Comparativo entre escolas ─ Quantidade de transporte",
# #         labels={"escola": "Escola", "transporte": "Qtd. Transporte"}
# #     )

# #     fig.update_yaxes(range=[0, 300])
# #     fig.update_layout(
# #         xaxis_title="Escola",
# #         yaxis_title="Qtd. Transporte",
# #         margin=dict(l=40, r=40, t=60, b=40)
# #     )

# #     st.plotly_chart(fig, use_container_width=True)

# # infraestrutura.py

# import pandas as pd
# import streamlit as st
# import plotly.express as px

# def infraestrutura(conn, nome_escola_marta, df_escolas):
#     # carrega os indicadores de infraestrutura da escola da Marta
#     em_inf = pd.read_sql(
#         """
#         SELECT
#             sb.IN_PATIO_COBERTO           AS patio_coberto,
#             sb.IN_BIBLIOTECA              AS biblioteca,
#             sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
#             sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
#             sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
#             sb.IN_PARQUE_INFANTIL         AS parque_infantil,
#             sb.IN_SALA_PROFESSOR          AS sala_professor,
#             sb.IN_COZINHA                 AS cozinha,
#             sb.IN_REFEITORIO              AS refeitório,
#             sb.IN_ALMOXARIFADO            AS almoxarifado,
#             sb.IN_ALIMENTACAO             AS alimentacao
#         FROM escola e
#         JOIN infraestrutura sb
#             ON sb.escola_id = e.id
#         WHERE e.NO_ENTIDADE = %s
#         """,
#         conn,
#         params=(nome_escola_marta,)
#     )

#     # converte booleanos para percentuais
#     def bool_to_pct(flag):
#         return 100.0 if bool(flag) else 0.0

#     # extrai percentuais da primeira linha (Marta)
#     if not em_inf.empty:
#         em_vals = em_inf.loc[0].apply(bool_to_pct).to_dict()
#     else:
#         em_vals = {col: 0.0 for col in [
#             "patio_coberto", "biblioteca", "laboratorio_ciencias",
#             "laboratorio_informatica", "quadra_esportes", "parque_infantil",
#             "sala_professor", "cozinha", "refeiturio", "almoxarifado", "alimentacao"
#         ]}

#     # carrega indicadores das escolas filtradas
#     if not df_escolas.empty:
#         placeholders = ", ".join(["%s"] * len(df_escolas))
#         sql = f"""
#             SELECT
#                 sb.IN_PATIO_COBERTO           AS patio_coberto,
#                 sb.IN_BIBLIOTECA              AS biblioteca,
#                 sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
#                 sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
#                 sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
#                 sb.IN_PARQUE_INFANTIL         AS parque_infantil,
#                 sb.IN_SALA_PROFESSOR          AS sala_professor,
#                 sb.IN_COZINHA                 AS cozinha,
#                 sb.IN_REFEITORIO              AS refeitório,
#                 sb.IN_ALMOXARIFADO            AS almoxarifado,
#                 sb.IN_ALIMENTACAO             AS alimentacao
#             FROM escola e
#             JOIN infraestrutura sb
#                 ON sb.escola_id = e.id
#             WHERE e.NO_ENTIDADE IN ({placeholders})
#         """
#         params = df_escolas["escola_nome"].tolist()
#         filt_inf = pd.read_sql(sql, conn, params=params)
#         # média dos booleanos vezes 100 para obter percentual agregado
#         avg_vals = (filt_inf.mean() * 100).to_dict()
#     else:
#         avg_vals = {key: 0.0 for key in em_vals.keys()}

#     # consulta quantidade de transporte da Marta
#     em_trans = pd.read_sql(
#         """
#         SELECT i.QT_TRANSP_PUBLICO AS transporte
#         FROM escola e
#         JOIN infraestrutura i
#             ON i.escola_id = e.id
#         WHERE e.NO_ENTIDADE = %s
#         """,
#         conn,
#         params=(nome_escola_marta,)
#     )
#     em_qt = int(em_trans.loc[0, "transporte"]) if not em_trans.empty else 0

#     # consulta quantidade de transporte das escolas filtradas
#     if not df_escolas.empty:
#         placeholders = ", ".join(["%s"] * len(df_escolas))
#         sql_trans = f"""
#             SELECT i.QT_TRANSP_PUBLICO AS transporte
#             FROM escola e
#             JOIN infraestrutura i
#                 ON i.escola_id = e.id
#             WHERE e.NO_ENTIDADE IN ({placeholders})
#         """
#         params_trans = df_escolas["escola_nome"].tolist()
#         filt_trans = pd.read_sql(sql_trans, conn, params=params_trans)
#         # média arredondada para inteiro
#         avg_qt = int(filt_trans["transporte"].mean())
#     else:
#         avg_qt = 0

#     # layout em duas colunas: Marta e filtro
#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("<h2>Escola de Marta</h2>", unsafe_allow_html=True)
#         st.markdown(f"<p>{nome_escola_marta}</p>", unsafe_allow_html=True)
#         # exibe cada KPI de infraestrutura para Marta
#         st.metric("Laboratório de Informática",    f"{em_vals['laboratorio_informatica']:.0f}%", border=True)
#         st.metric("Laboratório de Ciências",       f"{em_vals['laboratorio_ciencias']:.0f}%",      border=True)
#         st.metric("Biblioteca",                   f"{em_vals['biblioteca']:.0f}%",               border=True)
#         st.metric("Pátio Coberto",                f"{em_vals['patio_coberto']:.0f}%",            border=True)
#         st.metric("Parque Infantil",              f"{em_vals['parque_infantil']:.0f}%",          border=True)
#         st.metric("Quadra de Esportes",           f"{em_vals['quadra_esportes']:.0f}%",          border=True)
#         st.metric("Cozinha",                      f"{em_vals['cozinha']:.0f}%",                  border=True)
#         st.metric("Refeitório",                   f"{em_vals['refeitorio']:.0f}%",               border=True)

#     with col2:
#         st.markdown("<h2>Escolas do Filtro</h2>", unsafe_allow_html=True)
#         st.markdown(f"<p>{len(df_escolas)} escolas selecionadas</p>", unsafe_allow_html=True)
#         # exibe cada KPI médio para as escolas filtradas
#         st.metric("Laboratório de Informática",    f"{avg_vals['laboratorio_informatica']:.0f}%", border=True)
#         st.metric("Laboratório de Ciências",       f"{avg_vals['laboratorio_ciencias']:.0f}%",      border=True)
#         st.metric("Biblioteca",                   f"{avg_vals['biblioteca']:.0f}%",               border=True)
#         st.metric("Pátio Coberto",                f"{avg_vals['patio_coberto']:.0f}%",            border=True)
#         st.metric("Parque Infantil",              f"{avg_vals['parque_infantil']:.0f}%",          border=True)
#         st.metric("Quadra de Esportes",           f"{avg_vals['quadra_esportes']:.0f}%",          border=True)
#         st.metric("Cozinha",                      f"{avg_vals['cozinha']:.0f}%",                  border=True)
#         st.metric("Refeitório",                   f"{avg_vals['refeitorio']:.0f}%",               border=True)

#     # prepara DataFrame para gráfico de barra comparativo de transporte
#     df_bar = pd.DataFrame({
#         "escola":     [nome_escola_marta, "Filtro"],
#         "transporte": [em_qt,             avg_qt]
#     })

#     # gera gráfico com Plotly Express
#     fig = px.bar(
#         df_bar,
#         x="escola",
#         y="transporte",
#         text="transporte",
#         title="Comparativo de Transporte Público",
#         labels={"escola": "Escola", "transporte": "Qtd. Transporte"}
#     )

#     # ajustes de layout
#     fig.update_yaxes(range=[0, max(em_qt, avg_qt, 10)])
#     fig.update_layout(margin=dict(l=40, r=40, t=60, b=40))
#     st.plotly_chart(fig, use_container_width=True)

# # Importa bibliotecas necessárias
# import pandas as pd
# import streamlit as st
# import plotly.express as px
# import plotly.graph_objects as go

# # Função para mostrar a tela de infraestrutura
# def infraestrutura(conn, nome_escola_marta, df_escolas):
#     # Busca dados de infraestrutura da escola de Marta
#     em_inf = pd.read_sql(
#         """
#         SELECT
#             sb.IN_PATIO_COBERTO           AS patio_coberto,
#             sb.IN_BIBLIOTECA              AS biblioteca,
#             sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
#             sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
#             sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
#             sb.IN_PARQUE_INFANTIL         AS parque_infantil,
#             sb.IN_SALA_PROFESSOR          AS sala_professor,
#             sb.IN_COZINHA                 AS cozinha,
#             sb.IN_REFEITORIO              AS refeitorio,
#             sb.IN_ALMOXARIFADO            AS almoxarifado,
#             sb.IN_ALIMENTACAO             AS alimentacao
#         FROM escola e
#         JOIN infraestrutura sb
#             ON sb.escola_id = e.id
#         WHERE e.NO_ENTIDADE = %s
#         """,
#         conn,
#         params=(nome_escola_marta,)
#     )

#     # Função auxiliar para converter valores booleanos em texto "Sim" ou "Não"
#     def bool_to_text(flag: int) -> str:
#         return "Sim" if bool(flag) else "Não"

#     # Processa os dados da escola de Marta
#     if not em_inf.empty:
#         # Extrai os valores da primeira linha e converte para texto
#         em_vals = em_inf.loc[0].apply(lambda x: bool_to_text(x)).to_dict()
#     else:
#         # Se não encontrou dados, define todos como "Não"
#         em_vals = {col: "Não" for col in [
#             "patio_coberto", "biblioteca", "laboratorio_ciencias",
#             "laboratorio_informatica", "quadra_esportes", "parque_infantil",
#             "sala_professor", "cozinha", "refeitorio", "almoxarifado", "alimentacao"
#         ]}

#     # Busca dados de infraestrutura das escolas filtradas
#     if not df_escolas.empty:
#         # Cria placeholders dinâmicos para a query baseado no número de escolas
#         placeholders = ", ".join(["%s"] * len(df_escolas))
        
#         # Monta query SQL para buscar dados de todas as escolas filtradas
#         sql = f"""
#             SELECT
#                 e.NO_ENTIDADE,
#                 tl.descricao as localizacao,
#                 sb.IN_PATIO_COBERTO           AS patio_coberto,
#                 sb.IN_BIBLIOTECA              AS biblioteca,
#                 sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
#                 sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
#                 sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
#                 sb.IN_PARQUE_INFANTIL         AS parque_infantil,
#                 sb.IN_SALA_PROFESSOR          AS sala_professor,
#                 sb.IN_COZINHA                 AS cozinha,
#                 sb.IN_REFEITORIO              AS refeitorio,
#                 sb.IN_ALMOXARIFADO            AS almoxarifado,
#                 sb.IN_ALIMENTACAO             AS alimentacao
#             FROM escola e
#             JOIN infraestrutura sb ON sb.escola_id = e.id
#             JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
#             WHERE e.NO_ENTIDADE IN ({placeholders})
#         """
        
#         # Executa a query com os nomes das escolas filtradas
#         params = df_escolas["escola_nome"].tolist()
#         escolas_filtradas_inf = pd.read_sql(sql, conn, params=params)
#     else:
#         # Se não há escolas filtradas, cria DataFrame vazio
#         escolas_filtradas_inf = pd.DataFrame()

#     # Busca dados de transporte da escola de Marta
#     em_trans = pd.read_sql(
#         """
#         SELECT i.QT_TRANSP_PUBLICO AS transporte
#         FROM escola e
#         JOIN infraestrutura i
#             ON i.escola_id = e.id
#         WHERE e.NO_ENTIDADE = %s
#         """,
#         conn,
#         params=(nome_escola_marta,)
#     )
    
#     # Extrai a quantidade de transporte da escola de Marta
#     em_qt_transporte = int(em_trans.loc[0, "transporte"]) if not em_trans.empty else 0

#     # Busca dados de transporte das escolas filtradas
#     if not df_escolas.empty:
#         # Cria placeholders dinâmicos para a query de transporte
#         placeholders = ", ".join(["%s"] * len(df_escolas))
        
#         # Monta query SQL para buscar dados de transporte de todas as escolas filtradas
#         sql_trans = f"""
#             SELECT 
#                 e.NO_ENTIDADE,
#                 tl.descricao as localizacao,
#                 i.QT_TRANSP_PUBLICO AS transporte
#             FROM escola e
#             JOIN infraestrutura i ON i.escola_id = e.id
#             JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
#             WHERE e.NO_ENTIDADE IN ({placeholders})
#         """
        
#         # Executa a query com os nomes das escolas filtradas
#         params_trans = df_escolas["escola_nome"].tolist()
#         escolas_filtradas_trans = pd.read_sql(sql_trans, conn, params=params_trans)
#     else:
#         # Se não há escolas filtradas, cria DataFrame vazio
#         escolas_filtradas_trans = pd.DataFrame()

#     # Cria layout de duas colunas
#     col1, col2 = st.columns(2)

#     # Coluna 1: Dados da escola de Marta
#     with col1:
#         st.markdown("<h2>Escola de Marta</h2>", unsafe_allow_html=True)
#         st.markdown(f"<p>{nome_escola_marta}</p>", unsafe_allow_html=True)
        
#         # Exibe cada KPI de infraestrutura para a escola de Marta
#         st.metric("Laboratório de Informática", em_vals['laboratorio_informatica'], border=True)
#         st.metric("Laboratório de Ciências", em_vals['laboratorio_ciencias'], border=True)
#         st.metric("Biblioteca", em_vals['biblioteca'], border=True)
#         st.metric("Pátio Coberto", em_vals['patio_coberto'], border=True)
#         st.metric("Parque Infantil", em_vals['parque_infantil'], border=True)
#         st.metric("Quadra de Esportes", em_vals['quadra_esportes'], border=True)
#         st.metric("Cozinha", em_vals['cozinha'], border=True)
#         st.metric("Refeitório", em_vals['refeitorio'], border=True)

#     # Coluna 2: Gráficos das escolas filtradas
#     with col2:
#         st.markdown("<h2>Escolas Filtradas</h2>", unsafe_allow_html=True)
        
#         if not escolas_filtradas_inf.empty:
#             st.markdown(f"<p>{len(escolas_filtradas_inf)} escolas selecionadas</p>", unsafe_allow_html=True)
            
#             # Lista dos indicadores de infraestrutura para criar gráficos
#             indicadores_infraestrutura = [
#                 ('laboratorio_informatica', 'Laboratório de Informática'),
#                 ('laboratorio_ciencias', 'Laboratório de Ciências'),
#                 ('biblioteca', 'Biblioteca'),
#                 ('patio_coberto', 'Pátio Coberto'),
#                 ('parque_infantil', 'Parque Infantil'),
#                 ('quadra_esportes', 'Quadra de Esportes'),
#                 ('cozinha', 'Cozinha'),
#                 ('refeitorio', 'Refeitório')
#             ]
            
#             # # Para cada indicador de infraestrutura, cria um gráfico
#             # for campo, titulo in indicadores_infraestrutura:
#             #     # Calcula porcentagem por tipo de localização
#             #     dados_agrupados = escolas_filtradas_inf.groupby('localizacao')[campo].mean().reset_index()
#             #     dados_agrupados[campo] = dados_agrupados[campo] * 100
                
#             #     # Cria gráfico de barras
#             #     fig = px.bar(
#             #         dados_agrupados,
#             #         x='localizacao',
#             #         y=campo,
#             #         title=f'{titulo} (%)',
#             #         labels={'localizacao': 'Localização', campo: '

# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Função para mostrar a tela de infraestrutura
def infraestrutura(conn, nome_escola_marta, df_escolas):
    # Busca dados de infraestrutura da escola de Marta
    em_inf = pd.read_sql(
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
            sb.IN_REFEITORIO              AS refeitorio,
            sb.IN_ALMOXARIFADO            AS almoxarifado,
            sb.IN_ALIMENTACAO             AS alimentacao
        FROM escola e
        JOIN infraestrutura sb
            ON sb.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """,
        conn,
        params=(nome_escola_marta,)
    )

    # Função auxiliar para converter valores booleanos em texto "Sim" ou "Não"
    def bool_to_text(flag: int) -> str:
        return "Sim" if bool(flag) else "Não"

    # Processa os dados da escola de Marta
    if not em_inf.empty:
        # Extrai os valores da primeira linha e converte para texto
        em_vals = em_inf.loc[0].apply(lambda x: bool_to_text(x)).to_dict()
    else:
        # Se não encontrou dados, define todos como "Não"
        em_vals = {col: "Não" for col in [
            "patio_coberto", "biblioteca", "laboratorio_ciencias",
            "laboratorio_informatica", "quadra_esportes", "parque_infantil",
            "sala_professor", "cozinha", "refeitorio", "almoxarifado", "alimentacao"
        ]}

    # Busca dados de infraestrutura das escolas filtradas
    if not df_escolas.empty:
        # Cria placeholders dinâmicos para a query baseado no número de escolas
        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        # Monta query SQL para buscar dados de todas as escolas filtradas
        sql = f"""
            SELECT
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
                sb.IN_PATIO_COBERTO           AS patio_coberto,
                sb.IN_BIBLIOTECA              AS biblioteca,
                sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
                sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
                sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
                sb.IN_PARQUE_INFANTIL         AS parque_infantil,
                sb.IN_SALA_PROFESSOR          AS sala_professor,
                sb.IN_COZINHA                 AS cozinha,
                sb.IN_REFEITORIO              AS refeitorio,
                sb.IN_ALMOXARIFADO            AS almoxarifado,
                sb.IN_ALIMENTACAO             AS alimentacao
            FROM escola e
            JOIN infraestrutura sb ON sb.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        # Executa a query com os nomes das escolas filtradas
        params = df_escolas["escola_nome"].tolist()
        escolas_filtradas_inf = pd.read_sql(sql, conn, params=params)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_inf = pd.DataFrame()

    # Busca dados de transporte da escola de Marta
    em_trans = pd.read_sql(
        """
        SELECT i.QT_TRANSP_PUBLICO AS transporte
        FROM escola e
        JOIN infraestrutura i
            ON i.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """,
        conn,
        params=(nome_escola_marta,)
    )
    
    # Extrai a quantidade de transporte da escola de Marta
    em_qt_transporte = int(em_trans.loc[0, "transporte"]) if not em_trans.empty else 0

    # Busca dados de transporte das escolas filtradas
    if not df_escolas.empty:
        # Cria placeholders dinâmicos para a query de transporte
        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        # Monta query SQL para buscar dados de transporte de todas as escolas filtradas
        sql_trans = f"""
            SELECT 
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
                i.QT_TRANSP_PUBLICO AS transporte
            FROM escola e
            JOIN infraestrutura i ON i.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        # Executa a query com os nomes das escolas filtradas
        params_trans = df_escolas["escola_nome"].tolist()
        escolas_filtradas_trans = pd.read_sql(sql_trans, conn, params=params_trans)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_trans = pd.DataFrame()

    # Cria layout de duas colunas
    col1, col2 = st.columns(2)

    # Coluna 1: Dados da escola de Marta
    with col1:
        st.markdown("<h2>Escola de Marta</h2>", unsafe_allow_html=True)
        st.markdown(f"<p>{nome_escola_marta}</p>", unsafe_allow_html=True)
        
        # Exibe cada KPI de infraestrutura para a escola de Marta
        st.metric("Laboratório de Informática", em_vals['laboratorio_informatica'], border=True)
        st.metric("Laboratório de Ciências", em_vals['laboratorio_ciencias'], border=True)
        st.metric("Biblioteca", em_vals['biblioteca'], border=True)
        st.metric("Pátio Coberto", em_vals['patio_coberto'], border=True)
        st.metric("Parque Infantil", em_vals['parque_infantil'], border=True)
        st.metric("Quadra de Esportes", em_vals['quadra_esportes'], border=True)
        st.metric("Cozinha", em_vals['cozinha'], border=True)
        st.metric("Refeitório", em_vals['refeitorio'], border=True)

    # Coluna 2: Gráficos das escolas filtradas
    with col2:
        st.markdown("<h2>Escolas Filtradas</h2>", unsafe_allow_html=True)
        
        if not escolas_filtradas_inf.empty:
            st.markdown(f"<p>{len(escolas_filtradas_inf)} escolas selecionadas</p>", unsafe_allow_html=True)
            
            # Lista dos indicadores de infraestrutura para criar gráficos
            indicadores_infraestrutura = [
                ('laboratorio_informatica', 'Laboratório de Informática'),
                ('laboratorio_ciencias', 'Laboratório de Ciências'),
                ('biblioteca', 'Biblioteca'),
                ('patio_coberto', 'Pátio Coberto'),
                ('parque_infantil', 'Parque Infantil'),
                ('quadra_esportes', 'Quadra de Esportes'),
                ('cozinha', 'Cozinha'),
                ('refeitorio', 'Refeitório')
            ]
            
            # Para cada indicador de infraestrutura, cria um gráfico
            for campo, titulo in indicadores_infraestrutura:
                # Calcula porcentagem por tipo de localização
                dados_agrupados = escolas_filtradas_inf.groupby('localizacao')[campo].mean().reset_index()
                dados_agrupados[campo] = dados_agrupados[campo] * 100
                
                # Cria gráfico de barras
                fig = px.bar(
                    dados_agrupados,
                    x='localizacao',
                    y=campo,
                    title=f'{titulo} (%)',
                    labels={'localizacao': 'Localização', campo: 'Porcentagem (%)'},
                    color='localizacao',
                    color_discrete_map={'Urbana': '#1f77b4', 'Rural': '#ff7f0e'}
                )
                
                # Ajusta layout do gráfico
                fig.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                # Adiciona valores no topo das barras
                fig.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
                
                # Exibe o gráfico
                st.plotly_chart(fig, use_container_width=True)
                
            # Gráfico de transporte
            if not escolas_filtradas_trans.empty:
                st.markdown("<h3>Transporte Público</h3>", unsafe_allow_html=True)
                
                # Calcula estatísticas de transporte por localização
                transporte_stats = escolas_filtradas_trans.groupby('localizacao')['transporte'].agg(['mean', 'median', 'max']).reset_index()
                transporte_stats.columns = ['localizacao', 'media', 'mediana', 'maximo']
                
                # Gráfico de barras para transporte
                fig_trans = px.bar(
                    transporte_stats,
                    x='localizacao',
                    y='media',
                    title='Quantidade Média de Transporte Público',
                    labels={'localizacao': 'Localização', 'media': 'Quantidade Média'},
                    color='localizacao',
                    color_discrete_map={'Urbana': '#1f77b4', 'Rural': '#ff7f0e'}
                )
                
                fig_trans.update_layout(
                    showlegend=False,
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                fig_trans.update_traces(texttemplate='%{y:.1f}', textposition='outside')
                st.plotly_chart(fig_trans, use_container_width=True)
                
        else:
            # Se não há escolas filtradas, exibe mensagem informativa
            st.markdown("<p>Nenhuma escola selecionada</p>", unsafe_allow_html=True)
            st.write("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")