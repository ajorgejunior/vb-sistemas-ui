import streamlit as st
import requests
from utils import API_URL
from datetime import datetime

@st.cache_data(ttl=3600)
def get_partes_processo(numero_processo):
    try:
        resp = requests.get(f"{API_URL}/processos-brutos?numero={numero_processo}")
        if resp.status_code == 200:
            dados = resp.json().get("dados", [])
            if dados:
                partes = dados[0].get("json_original", {}).get("partes", [])
                principais = []
                for parte in partes:
                    if isinstance(parte, list) and len(parte) > 3:
                        nome = parte[3]
                        if nome and nome not in principais:
                            principais.append(nome)
                        if len(principais) >= 2:
                            break
                return principais
    except:
        return []
    return []

@st.cache_data(ttl=3600)
def get_movimentacoes():
    response = requests.get(f"{API_URL}/movimentacoes/recentes?limit=100")
    response.raise_for_status()
    return response.json()

def mostrar():
    st.title("📌 Últimas Movimentações de Processos")

    if st.button("🔄 Atualizar agora"):
        st.cache_data.clear()
        st.rerun()

    try:
        movimentacoes = get_movimentacoes()
    except requests.exceptions.RequestException as e:
        st.error("Erro ao buscar movimentações.")
        st.text(str(e))
        return

    lidas = set()
    try:
        lidas_resp = requests.get(f"{API_URL}/movimentacoes-lidas/")
        if lidas_resp.status_code == 200:
            lidas = set(lidas_resp.json().get("movimentacoes_lidas", []))
    except:
        pass

    nao_lidas = [m for m in movimentacoes if m["id"] not in lidas]

    st.markdown(f"### 🔔 <span style='color:red; font-size:24px'>{len(nao_lidas)} novas movimentações não lidas</span>", unsafe_allow_html=True)

    if not nao_lidas:
        st.info("Nenhuma movimentação para exibir.")
        return

    itens_por_pagina = 10
    total_paginas = (len(nao_lidas) - 1) // itens_por_pagina + 1
    pagina_atual = st.selectbox("Página", list(range(1, total_paginas + 1)))
    inicio = (pagina_atual - 1) * itens_por_pagina
    fim = inicio + itens_por_pagina
    exibidos = nao_lidas[inicio:fim]

    for mov in exibidos:
        data_formatada = datetime.strptime(mov["data"], "%Y-%m-%d").strftime("%d/%m/%Y")
        processo_numero = mov["processo_numero"]

        principais = get_partes_processo(processo_numero)
        partes_info = f" — 👥 {', '.join(principais)}" if principais else ""

        st.markdown(f'''
<div style='font-size:18px; font-weight:600; margin-top: 20px'>
📂 Processo <span style='color:green'>{processo_numero}</span> —
<span style='color:#008b8b'>{data_formatada}</span>{partes_info}
</div>
''', unsafe_allow_html=True)

        with st.expander("🔍 Ver detalhes da movimentação"):
            st.markdown(f"**📅 Data:** `{data_formatada}`")
            st.markdown(f"**📝 Resumo:** {mov.get('resumo', '-')}")
            st.markdown(f"**📃 Descrição:** {mov.get('descricao', '-')}")

            col1, col2 = st.columns([1, 2])
            if col1.button("✅ Marcar como lida", key=f"lida_{mov['id']}"):
                res = requests.post(f"{API_URL}/movimentacoes-lidas/{mov['id']}")
                if res.status_code == 200:
                    st.rerun()
                else:
                    st.error(f"Erro ao marcar como lida: {res.status_code} - {res.text}")

            if col2.button("📦 Ver detalhes na Digesto", key=f"detalhes_{mov['id']}"):
                st.query_params = {"page": "📦 Processos da Digesto", "numero": processo_numero}
                st.rerun()
