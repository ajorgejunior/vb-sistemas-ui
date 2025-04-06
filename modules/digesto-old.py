import streamlit as st
import requests
from utils import API_URL
from datetime import datetime

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

    if st.button("🔎 Buscar") or numero_param:
        processos = obter_processos_brutos(numero_busca.strip())
    else:
        processos = obter_processos_brutos()

    st.session_state.numero_digesto = None

    if not processos:
        st.info("Nenhum processo bruto encontrado.")
    else:
        for processo in processos:
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

                st.markdown("**👥 Partes:**")
                todas_partes = []
                for parte in dados.get("partes", []):
                    if isinstance(parte, list) and len(parte) > 8:
                        tipo = parte[8].title()
                        nome = parte[3]
                        partes_str = f"- {tipo}: **{nome}**"
                        advogados = parte[9] if len(parte) > 9 else []
                        for adv in advogados:
                            nome_adv = adv[1] if len(adv) > 1 else "-"
                            partes_str += f"\n  - 👨‍⚖️ Advogado: {nome_adv}"
                        todas_partes.append(partes_str)

                for p in todas_partes:
                    st.markdown(p)

                st.markdown("**🧾 Últimas movimentações:**")
                movs = dados.get("movs", [])
                if movs:
                    ver_todas_movs = st.checkbox(f"Ver todas as movimentações ({len(movs)})", key=processo['id'])
                    exibidas = movs if ver_todas_movs else movs[:5]
                    for mov in exibidas:
                        if len(mov) > 2:
                            data, resumo, descricao = mov[0], mov[1], mov[2]
                            st.markdown(f"- `{data}` **{resumo}** – {descricao}")
                else:
                    st.write("Nenhuma movimentação disponível.")

                anexos = dados.get("anexos", [])
                if anexos:
                    st.markdown("**📌 Anexos:**")
                    anexos_filtrados = []
                    for anexo in anexos:
                        if isinstance(anexo, list) and len(anexo) > 6:
                            titulo = anexo[6] or "Documento"
                            link = anexo[1] if len(anexo) > 1 else "#"
                            data = anexo[3][:10] if len(anexo) > 3 and anexo[3] else "-"
                            anexos_filtrados.append(f"- [{titulo} - {data}]({link})")

                    ver_todos_anexos = st.checkbox(f"Ver todos os anexos ({len(anexos_filtrados)})", key=f"anexos_{processo['id']}")
                    exibidos = anexos_filtrados if ver_todos_anexos else anexos_filtrados[:5]
                    for doc in exibidos:
                        st.markdown(doc)