import streamlit as st
import requests
from utils import API_URL
from datetime import datetime
from collections import defaultdict

def mostrar():
    st.title("📦 Processos da Digesto")

    numero_param = st.session_state.get("numero_digesto")
    numero_busca = st.text_input("🔍 Buscar por número do processo (opcional):", value=numero_param or "")

    def obter_processos_brutos(numero=None):
        try:
            url = f"{API_URL}/processos-brutos"
            if numero:
                url += f"?numero={numero}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get("dados", [])
            else:
                st.error("Erro ao buscar processos brutos")
                return []
        except Exception as e:
            st.error(f"Erro de conexão com a API: {e}")
            return []

    def obter_todas_movimentacoes():
        try:
            response = requests.get(f"{API_URL}/movimentacoes/recentes?limit=1000")
            if response.status_code == 200:
                movs = response.json()
                agrupado = defaultdict(list)
                for m in movs:
                    agrupado[m["processo_numero"]].append(m)
                return agrupado
        except:
            pass
        return defaultdict(list)

    mostrar_resultados = False

    if st.button("🔎 Buscar") or numero_param:
        processos = obter_processos_brutos(numero_busca.strip())
        mostrar_resultados = True
    else:
        processos = obter_processos_brutos()

    st.session_state.numero_digesto = None

    titulo = "📄 Resultados" if mostrar_resultados else "🕒 Últimos processos cadastrados"
    st.subheader(titulo)

    if not processos:
        st.info("Nenhum processo bruto encontrado.")
        return

    # ⚡ Requisição única para todas as movimentações
    todas_movs_por_processo = obter_todas_movimentacoes()

    for processo in processos[:5]:  # Mostrar apenas os 5 mais recentes
        dados = processo.get("json_original", {})
        numero_processo = processo.get("numero_processo", "-")
        tribunal = dados.get("tribunal") or "-"

        partes_seguras = []
        for parte in dados.get("partes", []):
            if isinstance(parte, list) and len(parte) > 3:
                nome = parte[3]
                if nome and nome not in partes_seguras:
                    partes_seguras.append(nome)
            if len(partes_seguras) >= 3:
                break

        with st.expander(f"📄 {numero_processo} | {tribunal} | {', '.join(partes_seguras)}", expanded=bool(numero_param)):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Classe:** {dados.get('classeNatureza') or '-'}")
                st.markdown(f"**Instância:** {dados.get('instancia') or '-'}")
                st.markdown(f"**Comarca:** {dados.get('comarca') or '-'}")
                st.markdown(f"**Tribunal:** {dados.get('tribunal') or '-'}")
            with col2:
                valor = dados.get('valor')
                valor_formatado = f"R$ {valor:,.2f}" if isinstance(valor, (int, float)) else "-"
                st.markdown(f"**Área:** {dados.get('area') or '-'}")
                st.markdown(f"**Valor da Causa:** {valor_formatado}")
                st.markdown(f"**Atualizado em:** {dados.get('alteradoEm') or '-'}")

            # 🔎 Botão para o site do TJPA
            if "tjpa" in tribunal.lower():
                url_tjpa = f"https://consultas.tjpa.jus.br/consultaunificada/consulta/principal?parametro={numero_processo}"
                st.markdown(
                    f"""
                    <a href="{url_tjpa}" target="_blank" style="
                        text-decoration: none;
                        display: inline-block;
                        padding: 0.5em 1em;
                        background-color: white;
                        color: black;
                        border: 2px solid black;
                        border-radius: 0.5em;
                        font-weight: 600;
                        font-size: 0.9em;
                        margin-top: 0.5em;
                    ">
                        🔎 Ver no site do TJPA
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("**🧾 Movimentações da Digesto (cadastro inicial):**")
            movs = dados.get("movs", [])
            if movs:
                ver_todas_movs = st.checkbox(f"Ver todas ({len(movs)})", key=f"digesto_{processo['id']}")
                exibidas = movs if ver_todas_movs else movs[:5]
                for mov in exibidas:
                    if len(mov) > 2:
                        data, resumo, descricao = mov[0], mov[1], mov[2]
                        try:
                            data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                        except:
                            data_formatada = data
                        st.markdown(f"- `{data_formatada}` **{resumo}** – {descricao}")
            else:
                st.write("Nenhuma movimentação disponível.")

            st.markdown("**🔔 Movimentações recentes (via Webhook):**")
            movs_banco = todas_movs_por_processo.get(numero_processo, [])
            if movs_banco:
                ver_todas_banco = st.checkbox(f"Ver todas ({len(movs_banco)})", key=f"banco_{processo['id']}")
                exibidas = movs_banco if ver_todas_banco else movs_banco[:5]
                for mov in exibidas:
                    data = mov.get("data")
                    try:
                        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
                    except:
                        data_formatada = data
                    resumo = mov.get("resumo", "-")
                    descricao = mov.get("descricao", "-")
                    st.markdown(f"- `{data_formatada}` **{resumo}** – {descricao}")
            else:
                st.write("Nenhuma movimentação encontrada no banco.")

