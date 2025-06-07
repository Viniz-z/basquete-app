import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="P-E", layout="centered")

# Estilo personalizado
st.markdown("""
    <style>
        body, .main { background-color: #0f1117; color: white; }
        .title {
            font-size: 3.5em;
            font-family: 'Orbitron', sans-serif;
            color: #00ffe7;
            text-align: center;
            margin-top: 30px;
            margin-bottom: 10px;
        }
        .stNumberInput > div > input {
            width: 55px;
            height: 38px;
            text-align: center;
            font-size: 16px;
            background-color: #1e1e2f;
            border: none;
            border-radius: 8px;
            color: white;
        }
        .stTextInput > div > input {
            text-align: center;
            font-size: 16px;
            border-radius: 8px;
            background-color: #1e1e2f;
            color: white;
        }
        label, h3, h2, h1, .block-container > div > div > div > div > p {
            display: none !important;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Título
st.markdown("<div class='title'>P-E</div>", unsafe_allow_html=True)

# Entrada de nomes dos times
col1, col2 = st.columns(2)
with col1:
    time1 = st.text_input("", "Time 1")
with col2:
    time2 = st.text_input("", "Time 2")

quartos = ["Q1", "Q2", "Q3", "Q4"]
data = []

# Inputs para os pontos
for q in quartos:
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col1:
        p1 = st.number_input("", min_value=0, max_value=50, step=1, key=f"{q}_1")
    with col2:
        st.markdown(f"<p style='text-align:center; font-size:18px; color:#00ffe7'>{q}</p>", unsafe_allow_html=True)
    with col3:
        p2 = st.number_input("", min_value=0, max_value=50, step=1, key=f"{q}_2")
    data.append({"Quarto": q, "Time": time1, "Pontos": p1})
    data.append({"Quarto": q, "Time": time2, "Pontos": p2})

# Gráfico
df = pd.DataFrame(data)
fig = px.bar(df, x="Quarto", y="Pontos", color="Time", barmode="group")
st.plotly_chart(fig, use_container_width=True)
