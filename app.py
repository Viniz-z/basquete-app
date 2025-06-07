import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="P-E: Comparador de Times de Basquete", layout="centered")
st.markdown("""
    <style>
        body { background-color: #0f1117; color: white; }
        .main { background-color: #0f1117; }
        .title { font-size: 3em; font-family: 'Orbitron', sans-serif; color: #00ffe7; text-align: center; margin: 20px 0; }
        .stButton>button { background-color: #1e1e2f; color: white; font-weight: bold; border-radius: 8px; }
        label { font-weight: bold; }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("<div class='title'>P-E: Comparador de Times de Basquete</div>", unsafe_allow_html=True)
st.markdown("### Digite o nome dos dois times para comparar o desempenho em jogos anteriores.")

col1, col2 = st.columns(2)
with col1:
    time1 = st.text_input("🔍 Time 1")
with col2:
    time2 = st.text_input("🔍 Time 2")

@st.cache_data(ttl=600)
def buscar_jogos_basquete(time_nome):
    busca = requests.get(f"https://api.sofascore.com/api/v1/team/search?q={time_nome}")
    st.write("🔍 Resposta da API (busca de time):", busca.status_code)
    try:
        dados = busca.json()
    except Exception as e:
        st.error(f"Erro ao converter JSON: {e}")
        return None

    st.write("📦 JSON retornado da busca:", dados)

    if not dados.get('teams'):
        st.warning(f"❌ Nenhum time encontrado para '{time_nome}'")
        return None

    time_id = dados['teams'][0]['id']
    st.write("🏀 ID do time encontrado:", time_id)

    eventos_response = requests.get(f"https://api.sofascore.com/api/v1/team/{time_id}/events/last/0")
    st.write("🔍 Resposta da API (eventos):", eventos_response.status_code)
    try:
        eventos = eventos_response.json().get("events", [])
    except Exception as e:
        st.error(f"Erro ao converter JSON dos eventos: {e}")
        return None

    st.write(f"🎮 Eventos recebidos para '{time_nome}': {len(eventos)}")
    if not eventos:
        st.warning(f"❌ Sem jogos recentes para '{time_nome}'")
        return None

    resultados = []
    for evento in eventos[:5]:
        eid = evento['id']
        oponente = evento['opponents'][1]['name'] if evento['opponents'][0]['name'].lower() == time_nome.lower() else evento['opponents'][0]['name']
        stats_url = f"https://api.sofascore.com/api/v1/event/{eid}/statistics"
        stats_response = requests.get(stats_url)
        st.write(f"🔍 Resposta da API (stats evento {eid}):", stats_response.status_code)
        try:
            stats = stats_response.json()
        except Exception as e:
            st.error(f"Erro ao converter JSON das estatísticas do evento {eid}: {e}")
            continue

        quarters = {}
        for stat in stats.get("periods", []):
            if "homeScore" in stat:
                quarters[f"Q{stat['number']}"] = stat["homeScore"]["current"]
        resultados.append({
            "oponente": oponente,
            "timestamp": evento['startTimestamp'],
            "quartos": quarters
        })
        time.sleep(1)
    return resultados

def comparar_times(t1, t2):
    jogos1 = buscar_jogos_basquete(t1)
    jogos2 = buscar_jogos_basquete(t2)

    if not jogos1 or not jogos2:
        st.warning("Não foi possível encontrar dados suficientes para ambos os times.")
        return

    df1 = []
    for j in jogos1:
        for q, pts in j['quartos'].items():
            df1.append({"Time": t1, "Jogo vs": j["oponente"], "Quarto": q, "Pontos": pts})
    df2 = []
    for j in jogos2:
        for q, pts in j['quartos'].items():
            df2.append({"Time": t2, "Jogo vs": j["oponente"], "Quarto": q, "Pontos": pts})
    df = pd.DataFrame(df1 + df2)

    st.markdown("### 📊 Gráfico de Pontuação por Quarto")
    fig = px.bar(df, x="Quarto", y="Pontos", color="Time", barmode="group", title=f"Comparação: {t1} vs {t2}")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 📌 Informações Diretas")
    st.write("**Média de pontos por quarto:**")
    media = df.groupby(["Time", "Quarto"])["Pontos"].mean().reset_index()
    st.dataframe(media)

if st.button("🔎 Analisar e Comparar"):
    if time1 and time2:
        comparar_times(time1, time2)
    else:
        st.warning("Digite o nome de ambos os times para realizar a comparação.")
