from src.data.data import dados
import pandas as pd
import streamlit as st

df = dados()

for coluna in df.columns:
    st.write(df[coluna].describe())