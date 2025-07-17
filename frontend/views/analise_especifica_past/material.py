import pandas as pd
import streamlit as st
from frontend.views.graficos import grafico_barras_comparativo, grafico_radar, grafico_donut_multimidia

# Função para mostrar a tela de materiais
def material (conn, nome_escola_marta, escola_selecionada):
    # Consulta para obter dados de materiais da escola de Marta
    em_mat_df = pd.read_sql(
        """
        SELECT
            m.IN_MATERIAL_PED_CIENTIFICO AS material_cientifico,
            m.IN_MATERIAL_PED_ARTISTICAS AS material_artistico,
            m.IN_MATERIAL_PED_DESPORTIVA AS material_esportivo,
            m.IN_INTERNET AS internet,
            m.QT_EQUIP_MULTIMIDIA AS equipamentos_multimidia
        FROM escola e
        JOIN materiais m ON m.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """,
        conn,
        params=(nome_escola_marta,)
    )

    # Consulta para a escola selecionada
    if escola_selecionada:
        es_mat_df = pd.read_sql(
            """
            SELECT
                m.IN_MATERIAL_PED_CIENTIFICO AS material_cientifico,
                m.IN_MATERIAL_PED_ARTISTICAS AS material_artistico,
                m.IN_MATERIAL_PED_DESPORTIVA AS material_esportivo,
                m.IN_INTERNET AS internet,
                m.QT_EQUIP_MULTIMIDIA AS equipamentos_multimidia
            FROM escola e
            JOIN materiais m ON m.escola_id = e.id
            WHERE e.NO_ENTIDADE = %s
            """,
            conn,
            params=(escola_selecionada,)
        )
    else:
        es_mat_df = pd.DataFrame(columns=[
            "material_cientifico", "material_artistico", "material_esportivo",
            "internet", "equipamentos_multimidia"
        ])

    # Função auxiliar para converter booleanos em porcentagem
    def bool_to_pct(flag: int) -> float:
        return 100.0 if bool(flag) else 0.0

    # Processamento dos dados da escola de Marta
    if not em_mat_df.empty:
        em_material_cientifico_pct = bool_to_pct(em_mat_df.loc[0, "material_cientifico"])
        em_material_artistico_pct = bool_to_pct(em_mat_df.loc[0, "material_artistico"])
        em_material_esportivo_pct = bool_to_pct(em_mat_df.loc[0, "material_esportivo"])
        em_internet_pct = bool_to_pct(em_mat_df.loc[0, "internet"])
        em_equipamentos_multimidia = int(em_mat_df.loc[0, "equipamentos_multimidia"])
    else:
        em_material_cientifico_pct = em_material_artistico_pct = em_material_esportivo_pct = 0.0
        em_internet_pct = 0.0
        em_equipamentos_multimidia = 0

    # Processamento dos dados da escola selecionada
    if not es_mat_df.empty:
        es_material_cientifico_pct = bool_to_pct(es_mat_df.loc[0, "material_cientifico"])
        es_material_artistico_pct = bool_to_pct(es_mat_df.loc[0, "material_artistico"])
        es_material_esportivo_pct = bool_to_pct(es_mat_df.loc[0, "material_esportivo"])
        es_internet_pct = bool_to_pct(es_mat_df.loc[0, "internet"])
        es_equipamentos_multimidia = int(es_mat_df.loc[0, "equipamentos_multimidia"])
    else:
        es_material_cientifico_pct = es_material_artistico_pct = es_material_esportivo_pct = 0.0
        es_internet_pct = 0.0
        es_equipamentos_multimidia = 0

    # Layout da página
    st.markdown("""
        <style>
            h1, h2, h3, p {
                text-align: center;
            }
            .metric-card {
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .highlight {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # Título e introdução
    st.markdown("""
        <h1>Materiais Pedagógicos e Tecnológicos</h1>
        <p>Comparativo de recursos disponíveis para ensino e aprendizagem</p>
    """, unsafe_allow_html=True)

    # Layout de duas colunas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h2>Escola de Marta</h2>
                <p>{nome_escola_marta}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.metric("Material Científico", f"{em_material_cientifico_pct:.0f}%", border=True)
        st.metric("Material Artístico", f"{em_material_artistico_pct:.0f}%", border=True)
        st.metric("Material Esportivo", f"{em_material_esportivo_pct:.0f}%", border=True)
        st.metric("Acesso à Internet", f"{em_internet_pct:.0f}%", border=True)
        st.metric("Equip. Multimídia", em_equipamentos_multimidia, border=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h2>Escola Selecionada</h2>
                <p>{escola_selecionada if escola_selecionada else "Nenhuma escola selecionada"}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if escola_selecionada:
            st.metric("Material Científico", f"{es_material_cientifico_pct:.0f}%", border=True)
            st.metric("Material Artístico", f"{es_material_artistico_pct:.0f}%", border=True)
            st.metric("Material Esportivo", f"{es_material_esportivo_pct:.0f}%", border=True)
            st.metric("Acesso à Internet", f"{es_internet_pct:.0f}%", border=True)
            st.metric("Equip. Multimídia", es_equipamentos_multimidia, border=True)
        else:
            st.warning("Selecione uma escola para comparar")

    # Seção de gráficos interativos
    st.markdown("---")
    st.markdown("<h2>Análise Visual Comparativa</h2>", unsafe_allow_html=True)

    if escola_selecionada and not es_mat_df.empty and not em_mat_df.empty:
        categorias = ['Material Científico', 'Material Artístico', 'Material Esportivo', 'Internet']
        valores_em = [em_material_cientifico_pct, em_material_artistico_pct, em_material_esportivo_pct, em_internet_pct]
        valores_es = [es_material_cientifico_pct, es_material_artistico_pct, es_material_esportivo_pct, es_internet_pct]

        # Gráfico de Barras
        st.plotly_chart(grafico_barras_comparativo(categorias, valores_em, valores_es), use_container_width=True)

        # Gráfico de Radar
        st.plotly_chart(grafico_radar(categorias, valores_em, valores_es), use_container_width=True)

        # Gráfico Donut
        st.plotly_chart(grafico_donut_multimidia(em_equipamentos_multimidia, es_equipamentos_multimidia), use_container_width=True)


    # Seção de recomendações (apenas para a escola de Marta)
    st.markdown("---")
    st.markdown("""
        <h2>Recomendações para a Escola de Marta</h2>
        <div class="highlight">
            <h3>Prioridades de Investimento</h3>
            <ul>
                <li><strong>Conexão com a Internet:</strong> Fundamental para acesso a conteúdos digitais e plataformas educacionais.</li>
                <li><strong>Equipamentos Multimídia:</strong> Projetores e computadores para aulas mais dinâmicas.</li>
                <li><strong>Kits Científicos Básicos:</strong> Para aulas práticas de ciências mesmo com infraestrutura limitada.</li>
                <li><strong>Parcerias com ONGs:</strong> Buscar organizações que doem materiais pedagógicos para escolas rurais.</li>
            </ul>
            
            <h3>Estratégias com Recursos Existentes</h3>
            <ul>
                <li>Utilizar materiais recicláveis para atividades artísticas e científicas.</li>
                <li>Implementar um sistema de empréstimo de livros e materiais entre professores.</li>
                <li>Buscar formações sobre ensino com recursos limitados para a equipe docente.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)