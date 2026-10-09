"""Painel Streamlit para visualizar os dados do ESP32.

Rodar a partir da pasta raiz do projeto:
    streamlit run app/main.py
"""

import sys
from datetime import datetime
from pathlib import Path

# Permite `from app...` mesmo com `streamlit run app/main.py`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from app.services.weather_api import ESP32Client, ESP32Error
from app.utils.config import settings

st.set_page_config(
    page_title="Monitor ESP32",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ Monitor ESP32")
st.caption("Temperatura e umidade lidas pela API do ESP32")

# -----------------------------------------------------------------------------
# Barra lateral
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("Configuração")
    ip = st.text_input("IP do ESP32", value=settings.esp32_ip)
    intervalo = st.slider("Atualizar a cada (segundos)", 2, 30, settings.refresh_s)

    if st.button("Limpar histórico"):
        st.session_state.historico = []

if "historico" not in st.session_state:
    st.session_state.historico = []

client = ESP32Client(ip, settings.timeout_s)


# -----------------------------------------------------------------------------
# Painel que se atualiza sozinho (sem recarregar a página inteira)
# -----------------------------------------------------------------------------
@st.fragment(run_every=intervalo)
def painel():
    historico = st.session_state.historico

    try:
        dados = client.get_dados()
    except ESP32Error as erro:
        st.error(f"Falha ao ler o ESP32: {erro}")
    else:
        historico.append(
            {
                "hora": datetime.now(),
                "temperatura": dados["temperatura"],
                "umidade": dados["umidade"],
            }
        )
        del historico[: -settings.max_pontos]

    if not historico:
        st.info("Ainda sem leituras. Aguardando o ESP32...")
        return

    atual = historico[-1]
    anterior = historico[-2] if len(historico) > 1 else None

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Temperatura",
        f"{atual['temperatura']:.1f} °C",
        None if anterior is None else f"{atual['temperatura'] - anterior['temperatura']:+.1f}",
    )
    col2.metric(
        "Umidade",
        f"{atual['umidade']:.1f} %",
        None if anterior is None else f"{atual['umidade'] - anterior['umidade']:+.1f}",
    )
    col3.metric("Última leitura", atual["hora"].strftime("%H:%M:%S"))

    df = pd.DataFrame(historico).set_index("hora")

    graf1, graf2 = st.columns(2)
    with graf1:
        st.subheader("Temperatura (°C)")
        st.line_chart(df["temperatura"])
    with graf2:
        st.subheader("Umidade (%)")
        st.line_chart(df["umidade"])

    with st.expander("Ver leituras"):
        st.dataframe(df.sort_index(ascending=False))


painel()
