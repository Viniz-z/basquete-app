import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="P-E", layout="centered")

# Estilo personalizado
st.markdown("""
    <style>
        body { background-color: #0f1117; color: white; }
        .main { background-color: #0f1117; }
        .title { font-size: 3em; font-family: 'Orbitron', sans-serif; color: #00ffe7; text-align: center; margin: 20px 0; }
        .stTextInput input { text-align: center; font-weight: bold; font-size: 18px; border-radius: 8px; }
        .stNumberInput input { width: 60px; text-align: center; padding: 3px; }
        .stButton>button { background-color: #1e1e2f; color: white; font-weight: bold; border-radius: 6px; font-size: 14px; padding: 3px 8px; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Título
st.markdown("<div class='title'>P-E</div>", unsafe_allow_html=True)

# Times e inputs lado a lado
col1, col2 = st.columns(2)

with col1:
    time1 = st.text_input("", placeholder="Time 1")
    pontos1 = [st.number_input("", key=f"p1_q{i}", min_value=0, step=1) for i in range(4)]

with col2:
    time2 = st.text_input("", placeholder="Time 2")
    pontos2 = [st.number_input("", key=f"p2_q{i}", min_value=0, step=1) for i in range(4)]

# Botão central pequeno
_, cbtn, _ = st.columns([3, 1, 3])
with cbtn:
    if st.button("Comparar"):
        if time1 and time2:
            df = pd.DataFrame({
                "Quarto": [f"Q{i+1}" for i in range(4)] * 2,
                "Pontos": pontos1 + pontos2,
                "Time": [time1] * 4 + [time2] * 4
            })
            fig = px.bar(df, x="Quarto", y="Pontos", color="Time", barmode="group")
            st.plotly_chart(fig, use_container_width=True)
