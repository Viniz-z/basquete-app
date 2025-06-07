import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="P-E", layout="centered")

# Estilo futurista e simples
st.markdown("""
    <style>
        body { background-color: #0f1117; color: white; }
        .title { font-size: 3em; font-family: 'Orbitron', sans-serif; color: #00ffe7; text-align: center; margin: 20px 0; }
        .stTextInput > div > input {
            font-size: 20px;
            height: 50px;
            width: 80px;
            text-align: center;
            background-color: #1e1e2f;
            color: white;
            border-radius: 8px;
        }
        .stButton>button {
            padding: 0.5em 1em;
            font-size: 14px;
            border-radius: 6px;
            background-color: #222;
            color: white;
            margin-top: 20px;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("<div class='title'>P-E</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    time1 = st.text_input("", placeholder="Time 1")
with col2:
    time2 = st.text_input("", placeholder="Time 2")

if st.button("Comparar"):
    st.success(f"Comparando {time1} vs {time2}")
    # Exemplo de dados fictícios
    dados = pd.DataFrame({
        'Quarto': ['Q1', 'Q2', 'Q3', 'Q4'] * 2,
        'Pontos': [20, 25, 18, 22, 23, 21, 19, 24],
        'Time': [time1] * 4 + [time2] * 4
    })

    fig = px.bar(dados, x="Quarto", y="Pontos", color="Time", barmode="group")
    st.plotly_chart(fig, use_container_width=True)
