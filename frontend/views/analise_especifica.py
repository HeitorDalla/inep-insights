# Importar bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Importando Páginas de visualização
from frontend.views.analise_especifica_past.saneamento_basico import saneamento_basico
from frontend.views.analise_especifica_past.corpo_docente import corpo_docente
from frontend.views.analise_especifica_past.infraestrutura import infraestrutura
from frontend.views.analise_especifica_past.material import material
from frontend.views.analise_especifica_past.matricula import matricula

# Função para mostrar a página de análise específica
def show_analise_especifica_page(conn):
    # SQL Query para ler as regiões únicas do banco de dados
    regiao_df = pd.read_sql("""
        SELECT DISTINCT NO_REGIAO 
        FROM regiao 
        ORDER BY NO_REGIAO ASC
        """, conn)
    
    # Selectbox na sidebar para o usuário selecionar a região
    regiao_selecionada = st.sidebar.selectbox(
        "Selecione a região:",
        options=regiao_df["NO_REGIAO"]
    )

    # SQL Query para ler as UFs únicas baseadas na região selecionada
    uf_df = pd.read_sql(
        """
        SELECT DISTINCT uf.NO_UF
        FROM uf
        JOIN regiao ON uf.regiao_id = regiao.id
        WHERE regiao.NO_REGIAO = %s
        ORDER BY uf.NO_UF ASC
        """, conn, params=(regiao_selecionada,)
    )

    # Selectbox na sidebar para o usuário selecionar a UF
    uf_selecionada = st.sidebar.selectbox(
        "Selecione a UF:",
        options=uf_df["NO_UF"]
    )

    # SQL Query para ler os municípios únicos baseados na UF selecionada
    municipio_df = pd.read_sql(
        """
        SELECT DISTINCT municipio.NO_MUNICIPIO
        FROM municipio
        JOIN uf ON municipio.uf_id = uf.id
        WHERE uf.NO_UF = %s
        ORDER BY municipio.NO_MUNICIPIO ASC
        """, conn, params=(uf_selecionada,)
    )

    # Selectbox na sidebar para o usuário selecionar o município
    municipio_selecionado = st.sidebar.selectbox(
        "Selecione o município:",
        options=municipio_df["NO_MUNICIPIO"]
    )

    # SQL Query para buscar os tipos de localização disponíveis (Urbana e Rural)
    tipo_localizacao_df = pd.read_sql("""
        SELECT id, descricao 
        FROM tipo_localizacao 
        ORDER BY descricao ASC
    """, conn)

    # Converte as opções de localização em uma lista
    tipo_localizacao_list = tipo_localizacao_df["descricao"].tolist()
    
    # Multiselect na sidebar para o usuário escolher os tipos de localização
    # Por padrão, todas as opções estão selecionadas
    tipo_localizacao_selecionada = st.sidebar.multiselect(
        "Selecione o(s) tipo(s) de localização:",
        options=tipo_localizacao_list,
        default=tipo_localizacao_list
    )

    # SQL Query para buscar escolas baseadas em todos os filtros aplicados
    # Verifica se o usuário escolheu pelo menos um tipo de localização
    if tipo_localizacao_selecionada:
        # Cria placeholders dinâmicos para a query SQL baseado no número de tipos selecionados
        # Exemplo: se 2 tipos selecionados, cria "%s, %s"
        placeholders = ", ".join(["%s"] * len(tipo_localizacao_selecionada))

        # Monta a query SQL com placeholders dinâmicos
        sql = f"""
            SELECT
                e.id               AS escola_id,
                e.NO_ENTIDADE      AS escola_nome,
                tl.descricao       AS localizacao
            FROM escola e
            JOIN municipio m           ON e.municipio_id       = m.id
            JOIN uf u                  ON m.uf_id              = u.id
            JOIN regiao r              ON u.regiao_id          = r.id
            JOIN tipo_localizacao tl   ON e.tp_localizacao_id  = tl.id
            WHERE r.NO_REGIAO    = %s
            AND u.NO_UF         = %s
            AND m.NO_MUNICIPIO  = %s
            AND tl.descricao    IN ({placeholders})
            ORDER BY e.NO_ENTIDADE ASC
        """
        
        # Constrói a lista de parâmetros para a query
        # Começa com os filtros fixos (região, UF, município) e adiciona os tipos de localização
        params = [regiao_selecionada, uf_selecionada, municipio_selecionado] + tipo_localizacao_selecionada
        
        # Executa a query e obtém o DataFrame com as escolas filtradas
        df_escolas = pd.read_sql(sql, conn, params=params)
    else:
        # Se nenhum tipo de localização foi selecionado, cria DataFrame vazio
        df_escolas = pd.DataFrame(columns=["escola_id", "escola_nome", "localizacao"])

    # # Verifica se encontrou escolas com os filtros aplicados
    # if not df_escolas.empty:
    #     # Exibe informação sobre quantas escolas foram encontradas
    #     st.sidebar.write(f"**{len(df_escolas)} escolas encontradas**")
        
    #     # Mostra a distribuição por tipo de localização
    #     distribuicao = df_escolas['localizacao'].value_counts()
    #     for tipo, qtd in distribuicao.items():
    #         st.sidebar.write(f"• {tipo}: {qtd} escolas")
    # else:
    #     # Se não encontrou escolas, exibe mensagem de alerta
    #     st.sidebar.write("**Nenhuma escola encontrada** com os filtros selecionados! Por favor, selecione ao menos um tipo de localização.")

    # Aplica estilo CSS às abas de navegação
    st.markdown("""
        <style>
            div[role="tablist"] {
                display: flex !important;
                justify-content: space-around !important; 
            }
        </style>
    """,
    unsafe_allow_html=True)

    # Configuração do menu de navegação com abas internas
    tab_saneamento_basico, tab_infraestrutura, tab_material, tab_corpo_docente, tab_matricula = st.tabs([
        "💦 Saneamento Básico",
        "🏫 Infraestrutura", 
        "📒 Material",
        "👩🏻 Corpo Docente",
        "🧑🏻‍🎓 Matrícula"
    ])

    # Nome da escola da persona Marta (escola de referência para comparação)
    nome_escola_marta = "TRABALHO E SABER ESCOLA MUNICIPAL DO CAMPO"

    # Conteúdo da aba "Saneamento Básico"
    with tab_saneamento_basico:
        # Passa a conexão, nome da escola de Marta e o DataFrame com escolas filtradas
        saneamento_basico(conn, nome_escola_marta, df_escolas)

    # Conteúdo da aba "Infraestrutura"
    with tab_infraestrutura:
        # Passa a conexão, nome da escola de Marta e o DataFrame com escolas filtradas
        infraestrutura(conn, nome_escola_marta, df_escolas)

    # Conteúdo da aba "Material"
    with tab_material:
        # Mantém a implementação original (não alterada nesta versão)
        material(conn, nome_escola_marta, df_escolas)

    # Conteúdo da aba "Corpo Docente"
    with tab_corpo_docente:
        # Mantém a implementação original (não alterada nesta versão)
        corpo_docente(conn, nome_escola_marta, df_escolas)

    # Conteúdo da aba "Matrícula"
    with tab_matricula:
        # Mantém a implementação original (não alterada nesta versão)
        matricula(conn, nome_escola_marta)