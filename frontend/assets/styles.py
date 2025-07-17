# Importa bibliotecas  
import streamlit as st

# Configurações de estilo (CSS)
st.markdown("""
    <style>
        /* Centraliza horizontalmente título 1 e parágrafo de classe "centered" */
        .h1 {
            text-align: center;
        }
            
        p.centered {
            text-align: center;
        }
        
        /* Define os estilos dos KPIs */
        .kpi-card {
            background-color: white;
            margin: 10px;
            padding: 10px; padding-bottom: 10px;
            border-radius: 10px;
            box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
        }

        .kpi-label {
            text-align: left;
            font-weight: 600;
            font-size: 1.25em;
        }

        .kpi-value {
            text-align: center;
            font-weight: 400;
            font-size: 2em;

        }

        .kpi-delta {
            text-align: center;
            font-weight: 600;
            font-size: 1em;
        }

        .kpi-caption {
            text-align: left;
            font-weight: 600;
            font-size: 1em;
        }

        /* Centraliza horizontalmente os menus de navegação internos */    
        div[role="tablist"] {
                display: flex !important;
                justify-content: space-around !important; 
        }

    </style>
""", 
unsafe_allow_html=True)