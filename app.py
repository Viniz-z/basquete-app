import streamlit as st import requests import pandas as pd import plotly.graph_objects as go import time

st.set_page_config(page_title="P-E: Comparador de Times", layout="centered") st.markdown(""" <style> body { background-color: #0f1117; color: white; } .main { background-color: #0f1117; } .title { font-size: 3em; font-family: 'Orbitron', sans-serif; color: #00ffe7; text-align: center; margin: 20px 0; } .stButton>button { background-color: #1e1e2f; color: white; font-weight: bold; border-radius: 8px; } label { font-weight: bold; color: #ffffff; } </style> <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet"> """, unsafe_allow_html=True)

st.markdown("<div class='title'>P-E: Comparador de Times de Basquete</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2) with col1: time1 = st.text_input("🏀 Time 1") with col2: time2 = st.text_input("🏀 Time 2")

@st.cache_data(ttl=600) def buscar_jogos_basquete(time_nome): busca = requests.get(f"https://api.sofascore.com/api/v1/team/search?q={time_nome}") dados = busca.json() if not dados.get('teams'): return None time_id = dados['teams'][0]['id'] eventos = requests.get(f"https://api.sofascore.com/api/v1/team/{time_id}/events/last/0").json().get("events", []) resultados = [] for evento in eventos[:5]: eid = evento['id'] oponente = evento['opponents'][1]['name'] if evento['opponents'][0]['name'].lower() == time_nome.lower() else evento['opponents'][0]['name'] stats_url = f"https://api.sofascore.com/api/v1/event/{eid}/statistics" stats = requests.get(stats_url).json() quarters = {} for stat in stats.get("periods", []): if "homeScore" in stat: quarters[f"Q{stat['number']}"] = stat["homeScore"]["current"] resultados.append({ "oponente": oponente, "timestamp": evento['startTimestamp'], "quartos": quarters }) time.sleep(1) return resultados

def gerar_grafico(df): fig = go.Figure() times = df['Time'].unique() for time in times: df_time = df[df['Time'] == time] fig.add_trace(go.Scatter( x=df_time['Quarto'], y=df_time['Pontos'], mode='lines+markers', name=time, line=dict(shape='spline'), )) fig.update_layout( title="Comparativo de Pontos por Quarto", template="plotly_dark", xaxis_title="Quarto", yaxis_title="Pontos", legend=dict(x=0.8, y=1.2) ) return fig

def comparar_times(t1, t2): jogos1 = buscar_jogos_basquete(t1) jogos2 = buscar_jogos_basquete(t2)

if not jogos1 or not jogos2:
    st.warning("Dados insuficientes para ambos os times.")
    return

df1, df2 = [], []
for j in jogos1:
    for q, pts in j['quartos'].items():
        df1.append({"Time": t1, "Jogo vs": j["oponente"], "Quarto": q, "Pontos": pts})
for j in jogos2:
    for q, pts in j['quartos'].items():
        df2.append({"Time": t2, "Jogo vs": j["oponente"], "Quarto": q, "Pontos": pts})
df = pd.DataFrame(df1 + df2)

st.plotly_chart(gerar_grafico(df), use_container_width=True)

st.markdown("### 📌 Médias por Quarto")
media = df.groupby(["Time", "Quarto"])["Pontos"].mean().reset_index()
st.dataframe(media)

if st.button("🔎 Comparar Times"): if time1 and time2: comparar_times(time1, time2) else: st.warning("Preencha os nomes dos dois times para comparar.")

