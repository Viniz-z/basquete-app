import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="P-E", layout="centered")

# Estilo personalizado
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Título
st.markdown("<div class='title'>P-E</div>", unsafe_allow_html=True)

# Interface com dois times lado a lado
col1, col2 = st.columns(2)

with col1:
    time1 = st.text_input("", placeholder="Time 1")
    pontos1 = [st.number_input(f"", key=f"t1_q{i+1}", min_value=0, step=1) for i in range(4)]

with col2:
    time2 = st.text_input("", placeholder="Time 2")
    pontos2 = [st.number_input(f"", key=f"t2_q{i+1}", min_value=0, step=1) for i in range(4)]

# Botão de comparar
if st.button("Comparar"):
    if time1 and time2:
        dados = []
        for i in range(4):
            dados.append({"Time": time1, "Quarto": f"Q{i+1}", "Pontos": pontos1[i]})
            dados.append({"Time": time2, "Quarto": f"Q{i+1}", "Pontos": pontos2[i]})
        df = pd.DataFrame(dados)

        fig = px.bar(df, x="Quarto", y="Pontos", color="Time", barmode="group", title=f"{time1} vs {time2}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Insira os nomes dos dois times.")
