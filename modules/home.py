import streamlit as st
import requests
import re
from utils import API_URL
from datetime import datetime
from collections import defaultdict

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

    # Obtém ids de movimentações lidas
    lidas = set()
    try:
        lidas_resp = requests.get(f"{API_URL}/movimentacoes-lidas/")
        if lidas_resp.status_code == 200:
            lidas = set(lidas_resp.json().get("movimentacoes_lidas", []))
    except:
        pass

    # Agrupar movimentações por processo
    agrupados = defaultdict(list)
    for mov in movimentacoes:
        agrupados[mov["processo_numero"]].append(mov)

    for processo_numero, movs in agrupados.items():
        principais = get_partes_processo(processo_numero)
        partes_info = f" — 👥 {', '.join(principais)}" if principais else ""

        total = len(movs)
        nao_lidas = [m for m in movs if m["id"] not in lidas]
        qtd_nao_lidas = len(nao_lidas)

        if qtd_nao_lidas == 0:
            continue  # Oculta processos sem movimentações não lidas

        cor_balao = "#ff4d4d"

        st.markdown(f"""
<div style='display: flex; justify-content: space-between; align-items: center; border: 1px solid #ccc; padding: 10px; border-radius: 10px; margin-top: 10px'>
  <div>
    <div style='font-size: 18px; font-weight: 600'>📂 {processo_numero}</div>
    <div style='color: #555; font-size: 15px'>{partes_info}</div>
  </div>
  <div style='text-align: right'>
    <div style='background-color: {cor_balao}; color: white; padding: 5px 10px; border-radius: 20px; font-size: 14px'>
      {qtd_nao_lidas}/{total}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        with st.expander("🔍 Ver movimentações não lidas"):
            for mov in sorted(nao_lidas, key=lambda m: m["data"], reverse=True):
                data_formatada = datetime.strptime(mov["data"], "%Y-%m-%d").strftime("%d/%m/%Y")
                st.markdown(f"<div style='color:red'><b>{data_formatada}</b> — {mov.get('descricao') or '-'}</div>", unsafe_allow_html=True)

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

            st.markdown("---")
            if st.button("✅ Marcar todas como lidas", key=f"marcar_todas_{processo_numero}"):
                

                uuid_regex = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[1-5][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$", re.I)
                ids = [mov["id"] for mov in nao_lidas if isinstance(mov["id"], str) and uuid_regex.match(mov["id"])]

                res = requests.post(f"{API_URL}/movimentacoes-lidas-em-lote", json={"ids": [mov["id"] for mov in nao_lidas],"usuario_id": "default"})
                if res.status_code == 200:
                    st.success("Todas as movimentações foram marcadas como lidas.")
                    st.rerun()
                else:
                    st.error(f"Erro ao marcar como lidas: {res.status_code} - {res.text}")

