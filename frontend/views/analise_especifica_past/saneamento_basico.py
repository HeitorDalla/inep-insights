# # Importa bibliotecas 
# import pandas as pd
# import streamlit as st

# # Função para carregar os estilos
# def load_css(caminho_arquivo):
#     with open(caminho_arquivo, "r", encoding="utf-8") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # Carrega CSS centralizado
# load_css("frontend/assets/css/style.css")

# # Função para mostrar a tela de Saneamento Básico
# def saneamento_basico (conn, nome_escola_marta, escola_selecionada):
#     # Executa uma query SQL e retorna um DataFrame
#     em_df = pd.read_sql("""
#         SELECT
#             sb.IN_AGUA_POTAVEL         AS agua_potavel,
#             sb.IN_AGUA_REDE_PUBLICA    AS agua_rede_publica,
#             sb.IN_AGUA_POCO_ARTESIANO  AS agua_poco_artesiano,
#             sb.IN_AGUA_INEXISTENTE     AS agua_inexistente,
#             sb.IN_ESGOTO_REDE_PUBLICA  AS esgoto_rede_publica,
#             sb.IN_ESGOTO_INEXISTENTE   AS esgoto_inexistente,
#             sb.IN_ENERGIA_REDE_PUBLICA AS energia_rede_publica,
#             sb.IN_ENERGIA_INEXISTENTE  AS energia_inexistente,
#             sb.IN_LIXO_SERVICO_COLETA  AS lixo_servico_coleta
#         FROM escola e
#         JOIN saneamento_basico sb 
#             ON sb.escola_id = e.id
#         WHERE e.NO_ENTIDADE = %s
#     """, conn, params=(nome_escola_marta,))
#     # SELECT: seleciona todos os indicadores booleanos de saneamento e renomeia cada coluna para algo mais legível 
    
#     # JOIN: liga a tabela "escola" (e) à tabela saneamento_basico (sb) via escola.id

#     # WHERE … = %s: filtra apenas pela escola cujo nome é igual ao nome da variável "nome_escola_marta"

#     # params=(nome_escola_marta,): passa o nome da variável "nome_escola_marta" como parâmetro para a query SQL

#     if escola_selecionada:
#     # Se o usuário já tiver escolhido uma escola via sidebar, executa a mesma query acima, mas passando o nome da escola selecionada, e guarda o resultado em outro DataFrame.
#         es_df = pd.read_sql("""
#             SELECT
#                 sb.IN_AGUA_POTAVEL         AS agua_potavel,
#                 sb.IN_AGUA_REDE_PUBLICA    AS agua_rede_publica,
#                 sb.IN_AGUA_POCO_ARTESIANO  AS agua_poco_artesiano,
#                 sb.IN_AGUA_INEXISTENTE     AS agua_inexistente,
#                 sb.IN_ESGOTO_REDE_PUBLICA  AS esgoto_rede_publica,
#                 sb.IN_ESGOTO_INEXISTENTE   AS esgoto_inexistente,
#                 sb.IN_ENERGIA_REDE_PUBLICA AS energia_rede_publica,
#                 sb.IN_ENERGIA_INEXISTENTE  AS energia_inexistente,
#                 sb.IN_LIXO_SERVICO_COLETA  AS lixo_servico_coleta
#             FROM escola e
#             JOIN saneamento_basico sb 
#                 ON sb.escola_id = e.id
#             WHERE e.NO_ENTIDADE = %s
#         """, conn, params=(escola_selecionada,))
#     else:
#         # Caso contrário, cria um DataFrame vazio com as mesmas colunas, para evitar erros posteriores ao tentar acessar índices inexistentes.
#         es_df = pd.DataFrame(columns=[
#             "agua_potavel", "agua_rede_publica", "agua_poco_artesiano", "agua_inexistente",
#             "esgoto_rede_publica", "esgoto_inexistente",
#             "energia_rede_publica", "energia_inexistente",
#             "lixo_servico_coleta"
#         ])

#     # Função auxiliar que recebe um valor 0 ou 1 e devolve 0.0 ou 100.0 respectivamente
#     def bool_to_pct(flag: int) -> float:
#         # Primeiro converte para bool (0 → False; 1 → True), depois escolhe o percentual correspondente (True → 100.0; False → 0.0)
#         return 100.0 if bool(flag) else 0.0

#     if not em_df.empty:
#         # Verifica se "em_df" não está vazio): se não estiver, extrai cada um dos campos na primeira linha (loc[0, "..."])

#         # Para os indicadores de “inexistente” (água, esgoto e energia), inverte-se o valor com (1 - <flag>) para mostrar a disponibilidade

#         # Passa tudo pela função "bool_to_pct" para obter 0.0 ou 100.0
#         em_agua_potavel_pct        = bool_to_pct(em_df.loc[0, "agua_potavel"])
#         em_agua_rede_publica_pct   = bool_to_pct(em_df.loc[0, "agua_rede_publica"])
#         em_agua_poco_artesiano_pct = bool_to_pct(em_df.loc[0, "agua_poco_artesiano"])
#         em_agua_inexistente_pct    = bool_to_pct(1 - em_df.loc[0, "agua_inexistente"])
#         em_esgoto_rede_publica_pct = bool_to_pct(em_df.loc[0, "esgoto_rede_publica"])
#         em_esgoto_inexistente_pct  = bool_to_pct(1 - em_df.loc[0, "esgoto_inexistente"])
#         em_energia_rede_publica_pct= bool_to_pct(em_df.loc[0, "energia_rede_publica"])
#         em_energia_inexistente_pct = bool_to_pct(1 - em_df.loc[0, "energia_inexistente"])
#         em_lixo_servico_coleta_pct = bool_to_pct(em_df.loc[0, "lixo_servico_coleta"])
#     else:
#         # Se "em_df" estiver vazio, atribui 0.0 a todas as variáveis de percentuais de Marta
#         em_agua_potavel_pct = em_agua_rede_publica_pct = em_agua_poco_artesiano_pct = 0.0
#         em_agua_inexistente_pct = em_esgoto_rede_publica_pct = em_esgoto_inexistente_pct = 0.0
#         em_energia_rede_publica_pct = em_energia_inexistente_pct = em_lixo_servico_coleta_pct = 0.0
    
#     # Idêntico ao bloco anterior, mas para a escola selecionada
#     if not es_df.empty:
#         es_agua_potavel_pct        = bool_to_pct(es_df.loc[0, "agua_potavel"])
#         es_agua_rede_publica_pct   = bool_to_pct(es_df.loc[0, "agua_rede_publica"])
#         es_agua_poco_artesiano_pct = bool_to_pct(es_df.loc[0, "agua_poco_artesiano"])
#         es_agua_inexistente_pct    = bool_to_pct(1 - es_df.loc[0, "agua_inexistente"])
#         es_esgoto_rede_publica_pct = bool_to_pct(es_df.loc[0, "esgoto_rede_publica"])
#         es_esgoto_inexistente_pct  = bool_to_pct(1 - es_df.loc[0, "esgoto_inexistente"])
#         es_energia_rede_publica_pct= bool_to_pct(es_df.loc[0, "energia_rede_publica"])
#         es_energia_inexistente_pct = bool_to_pct(1 - es_df.loc[0, "energia_inexistente"])
#         es_lixo_servico_coleta_pct = bool_to_pct(es_df.loc[0, "lixo_servico_coleta"])
#     else:
#         es_agua_potavel_pct = es_agua_rede_publica_pct = es_agua_poco_artesiano_pct = 0.0
#         es_agua_inexistente_pct = es_esgoto_rede_publica_pct = es_esgoto_inexistente_pct = 0.0
#         es_energia_rede_publica_pct = es_energia_inexistente_pct = es_lixo_servico_coleta_pct = 0.0

#     # Cria um layout de duas colunas iguais no Streamlit, atribuídas às variáveis col1 (esquerda) e col2 (direita)
#     col1, col2 = st.columns(2)

#     # st.metric: para cada indicador, exibe um cartão com rótulo e valor formatado (:.0f)
#     with col1:
#         st.markdown("""
#             <h1 class="h1-title-anal_espc">Escola de Marta</h1>
#         """,
#         unsafe_allow_html=True)
#         st.markdown(f"""
#             <p class="p-title-anal_espc">{nome_escola_marta}</p>
#         """,
#         unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Água potável</div>
#                 <div class="kpi-value">{em_agua_potavel_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#         """, unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Água de rede pública</div>
#                 <div class="kpi-value">{em_agua_rede_publica_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#         """, unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Esgoto disponível</div>
#                 <div class="kpi-value">{em_esgoto_inexistente_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#         """, unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Esgoto de rede pública</div>
#                 <div class="kpi-value">{em_esgoto_rede_publica_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#         """, unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Energia disponível</div>
#                 <div class="kpi-value">{em_energia_inexistente_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#         """, unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Energia de rede pública</div>
#                 <div class="kpi-value">{em_energia_rede_publica_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#         """, unsafe_allow_html=True)
#         st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Coleta de lixo</div>
#                 <div class="kpi-value">{em_lixo_servico_coleta_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#         """, unsafe_allow_html=True)
#         # st.metric("Água Potável",             f"{em_agua_potavel_pct:.0f}%", border=True)
#         # st.metric("Água Rede Pública",        f"{em_agua_rede_publica_pct:.0f}%", border=True)
#         # st.metric("Poço Artesiano",           f"{em_agua_poco_artesiano_pct:.0f}%", border=True)
#         # st.metric("Esgoto Disponível",        f"{em_esgoto_inexistente_pct:.0f}%", border=True)
#         # st.metric("Esgoto Rede Pública",      f"{em_esgoto_rede_publica_pct:.0f}%", border=True)
#         # st.metric("Energia Disponível",       f"{em_energia_inexistente_pct:.0f}%", border=True)
#         # st.metric("Energia Rede Pública",     f"{em_energia_rede_publica_pct:.0f}%", border=True)
#         # st.metric("Coleta de Lixo",           f"{em_lixo_servico_coleta_pct:.0f}%", border=True)

#     with col2:
#         st.markdown("""
#             <h1 class="h1-title-anal_espc">Escola selecionada</h1>
#         """,
#         unsafe_allow_html=True)
#         st.markdown(f"""
#             <p class="p-title-anal_espc">{escola_selecionada}</p>
#         """,
#         unsafe_allow_html=True)
#         if escola_selecionada:
#             st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Água potável</div>
#                 <div class="kpi-value">{es_agua_potavel_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#             """, unsafe_allow_html=True)
#             st.markdown(f"""
#             <div class="kpi-card">
#                 <div class="kpi-label">Água de rede pública</div>
#                 <div class="kpi-value">{es_agua_rede_publica_pct:.0f}%</div>
#                 <div class="kpi-delta"></div>
#                 <div class="kpi-caption"></div>
#             </div>
#             """, unsafe_allow_html=True)
#             st.markdown(f"""
#                 <div class="kpi-card">
#                     <div class="kpi-label">Esgoto disponível</div>
#                     <div class="kpi-value">{es_esgoto_inexistente_pct:.0f}%</div>
#                     <div class="kpi-delta"></div>
#                     <div class="kpi-caption"></div>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.markdown(f"""
#                 <div class="kpi-card">
#                     <div class="kpi-label">Esgoto de rede pública</div>
#                     <div class="kpi-value">{es_esgoto_rede_publica_pct:.0f}%</div>
#                     <div class="kpi-delta"></div>
#                     <div class="kpi-caption"></div>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.markdown(f"""
#                 <div class="kpi-card">
#                     <div class="kpi-label">Energia disponível</div>
#                     <div class="kpi-value">{es_energia_inexistente_pct:.0f}%</div>
#                     <div class="kpi-delta"></div>
#                     <div class="kpi-caption"></div>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.markdown(f"""
#                 <div class="kpi-card">
#                     <div class="kpi-label">Energia de rede pública</div>
#                     <div class="kpi-value">{es_energia_rede_publica_pct:.0f}%</div>
#                     <div class="kpi-delta"></div>
#                     <div class="kpi-caption"></div>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.markdown(f"""
#                 <div class="kpi-card">
#                     <div class="kpi-label">Coleta de lixo</div>
#                     <div class="kpi-value">{es_lixo_servico_coleta_pct:.0f}%</div>
#                     <div class="kpi-delta"></div>
#                     <div class="kpi-caption"></div>
#                 </div>
#             """, unsafe_allow_html=True)
#             # st.metric("Água Potável",         f"{es_agua_potavel_pct:.0f}%", border=True)
#             # st.metric("Água Rede Pública",    f"{es_agua_rede_publica_pct:.0f}%", border=True)
#             # # st.metric("Poço Artesiano",       f"{es_agua_poco_artesiano_pct:.0f}%", border=True)
#             # st.metric("Esgoto Disponível",    f"{es_esgoto_inexistente_pct:.0f}%", border=True)
#             # st.metric("Esgoto Rede Pública",  f"{es_esgoto_rede_publica_pct:.0f}%", border=True)
#             # st.metric("Energia Disponível",   f"{es_energia_inexistente_pct:.0f}%", border=True)
#             # st.metric("Energia Rede Pública", f"{es_energia_rede_publica_pct:.0f}%", border=True)
#             # st.metric("Coleta de Lixo",       f"{es_lixo_servico_coleta_pct:.0f}%", border=True)
#         else:
#             st.write("Por favor, selecione uma escola válida.")

# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Função para carregar os estilos CSS
def load_css(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega CSS centralizado
load_css("frontend/assets/css/style.css")

# Função para mostrar a tela de Saneamento Básico
def saneamento_basico(conn, nome_escola_marta, df_escolas):
    # Busca dados de saneamento básico da escola de Marta
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

    # Função auxiliar para converter valores booleanos em texto "Sim" ou "Não"
    def bool_to_text(flag: int) -> str:
        return "Sim" if bool(flag) else "Não"

    # Processa os dados da escola de Marta
    if not em_df.empty:
        # Extrai os valores da primeira linha e converte para texto
        em_agua_potavel        = bool_to_text(em_df.loc[0, "agua_potavel"])
        em_agua_rede_publica   = bool_to_text(em_df.loc[0, "agua_rede_publica"])
        em_agua_poco_artesiano = bool_to_text(em_df.loc[0, "agua_poco_artesiano"])
        # Para campos "inexistente", inverte o valor (se inexistente=1, mostra "Não disponível")
        em_agua_inexistente    = bool_to_text(1 - em_df.loc[0, "agua_inexistente"])
        em_esgoto_rede_publica = bool_to_text(em_df.loc[0, "esgoto_rede_publica"])
        em_esgoto_inexistente  = bool_to_text(1 - em_df.loc[0, "esgoto_inexistente"])
        em_energia_rede_publica= bool_to_text(em_df.loc[0, "energia_rede_publica"])
        em_energia_inexistente = bool_to_text(1 - em_df.loc[0, "energia_inexistente"])
        em_lixo_servico_coleta = bool_to_text(em_df.loc[0, "lixo_servico_coleta"])
    else:
        # Se não encontrou dados, define todos como "Não"
        em_agua_potavel = em_agua_rede_publica = em_agua_poco_artesiano = "Não"
        em_agua_inexistente = em_esgoto_rede_publica = em_esgoto_inexistente = "Não"
        em_energia_rede_publica = em_energia_inexistente = em_lixo_servico_coleta = "Não"

    # Busca dados de saneamento básico das escolas filtradas
    if not df_escolas.empty:
        # Cria placeholders dinâmicos para a query baseado no número de escolas
        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        # Monta query SQL para buscar dados de todas as escolas filtradas
        sql = f"""
            SELECT
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
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
            JOIN saneamento_basico sb ON sb.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        # Executa a query com os nomes das escolas filtradas
        params = df_escolas["escola_nome"].tolist()
        escolas_filtradas_df = pd.read_sql(sql, conn, params=params)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_df = pd.DataFrame()

    # Cria layout de duas colunas
    col1, col2 = st.columns(2)

    # Coluna 1: Dados da escola de Marta
    with col1:
        st.markdown("""
            <h1 class="h1-title-anal_espc">Escola de Marta</h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <p class="p-title-anal_espc">{nome_escola_marta}</p>
        """, unsafe_allow_html=True)
        
        # Exibe cada KPI da escola de Marta usando HTML customizado
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Água potável</div>
                <div class="kpi-value">{em_agua_potavel}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Água de rede pública</div>
                <div class="kpi-value">{em_agua_rede_publica}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Esgoto disponível</div>
                <div class="kpi-value">{em_esgoto_inexistente}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Esgoto de rede pública</div>
                <div class="kpi-value">{em_esgoto_rede_publica}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Energia disponível</div>
                <div class="kpi-value">{em_energia_inexistente}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Energia de rede pública</div>
                <div class="kpi-value">{em_energia_rede_publica}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Coleta de lixo</div>
                <div class="kpi-value">{em_lixo_servico_coleta}</div>
            </div>
        """, unsafe_allow_html=True)

    # Coluna 2: Gráficos das escolas filtradas
    with col2:
        st.markdown("""
            <h1 class="h1-title-anal_espc">Escolas Filtradas</h1>
        """, unsafe_allow_html=True)
        
        if not escolas_filtradas_df.empty:
            st.markdown(f"""
                <p class="p-title-anal_espc">{len(escolas_filtradas_df)} escolas selecionadas</p>
            """, unsafe_allow_html=True)
            
            # Lista dos indicadores para criar gráficos
            indicadores = [
                ('agua_potavel', 'Água Potável'),
                ('agua_rede_publica', 'Água de Rede Pública'),
                ('esgoto_rede_publica', 'Esgoto de Rede Pública'),
                ('energia_rede_publica', 'Energia de Rede Pública'),
                ('lixo_servico_coleta', 'Coleta de Lixo')
            ]
            
            # Para cada indicador, cria um gráfico
            for campo, titulo in indicadores:
                # Calcula porcentagem por tipo de localização
                if campo in ['agua_inexistente', 'esgoto_inexistente', 'energia_inexistente']:
                    # Para campos "inexistente", inverte o valor (1 - valor)
                    dados_agrupados = escolas_filtradas_df.groupby('localizacao')[campo].apply(
                        lambda x: (1 - x).mean() * 100
                    ).reset_index()
                else:
                    # Para outros campos, calcula média normal
                    dados_agrupados = escolas_filtradas_df.groupby('localizacao')[campo].mean().reset_index()
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
        else:
            # Se não há escolas filtradas, exibe mensagem informativa
            st.markdown("""
                <p class="p-title-anal_espc">Nenhuma escola selecionada</p>
            """, unsafe_allow_html=True)
            
            st.write("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")