import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Comparador Manual de Times", layout="centered")
st.markdown("<h1 style='text-align: center; color: #00ffe7;'>🏀 Comparador Manual de Times</h1>", unsafe_allow_html=True)

st.markdown("Insira os nomes dos times e os pontos por quarto:")

col1, col2 = st.columns(2)

with col1:
    time1 = st.text_input("Nome do Time 1", "Flamengo")
    q1_1 = st.number_input("Q1 - Time 1", min_value=0, step=1)
    q2_1 = st.number_input("Q2 - Time 1", min_value=0, step=1)
    q3_1 = st.number_input("Q3 - Time 1", min_value=0, step=1)
    q4_1 = st.number_input("Q4 - Time 1", min_value=0, step=1)

with col2:
    time2 = st.text_input("Nome do Time 2", "Botafogo")
    q1_2 = st.number_input("Q1 - Time 2", min_value=0, step=1)
    q2_2 = st.number_input("Q2 - Time 2", min_value=0, step=1)
    q3_2 = st.number_input("Q3 - Time 2", min_value=0, step=1)
    q4_2 = st.number_input("Q4 - Time 2", min_value=0, step=1)

if st.button("🔍 Comparar Times"):
    df = pd.DataFrame([
        {"Time": time1, "Quarto": "Q1", "Pontos": q1_1},
        {"Time": time1, "Quarto": "Q2", "Pontos": q2_1},
        {"Time": time1, "Quarto": "Q3", "Pontos": q3_1},
        {"Time": time1, "Quarto": "Q4", "Pontos": q4_1},
        {"Time": time2, "Quarto": "Q1", "Pontos": q1_2},
        {"Time": time2, "Quarto": "Q2", "Pontos": q2_2},
        {"Time": time2, "Quarto": "Q3", "Pontos": q3_2},
        {"Time": time2, "Quarto": "Q4", "Pontos": q4_2},
    ])

    # Gráfico
    st.markdown("### 📊 Pontos por Quarto")
    fig = px.bar(df, x="Quarto", y="Pontos", color="Time", barmode="group")
    st.plotly_chart(fig)

    # Média (neste caso é só os próprios dados, mas mantemos estrutura)
    media = df.groupby("Time")["Pontos"].mean().reset_index()
    st.markdown("### 🧮 Média de Pontos por Quarto")
    st.dataframe(media)

    # Análise simples
    st.markdown("### 🤖 Insight")
    if q1_1 > q4_1:
        st.write(f"➡️ **{time1}** começa forte e perde força no final.")
    elif q4_1 > q1_1:
        st.write(f"➡️ **{time1}** melhora ao longo do jogo.")
    if q1_2 > q4_2:
        st.write(f"➡️ **{time2}** começa forte e perde força no final.")
    elif q4_2 > q1_2:
        st.write(f"➡️ **{time2}** melhora ao longo do jogo.")
