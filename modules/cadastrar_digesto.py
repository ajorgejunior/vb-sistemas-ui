import streamlit as st
import requests
from utils import API_URL
import json
import io

def mostrar():
    st.title("📥 Cadastrar Processo via API Digesto")

    if "processo_digesto" not in st.session_state:
        st.session_state.processo_digesto = None

    numero = st.text_input("Digite o número do processo (ex: 0800486-19.2021.8.14.9000)")

    if st.button("🔍 Buscar na Digesto"):
        if not numero.strip():
            st.warning("Digite um número de processo válido.")
            return

        with st.spinner("Consultando API da Digesto..."):
            try:
                response = requests.post(f"{API_URL}/buscar-digesto/", json={"numero_processo": numero})
                if response.status_code == 200:
                    st.session_state.processo_digesto = response.json()
                    st.success("Processo encontrado!")
                else:
                    st.session_state.processo_digesto = None
                    st.error("Não foi possível consultar o processo na Digesto.")
                    st.text(response.text)
            except Exception as e:
                st.session_state.processo_digesto = None
                st.error(f"Erro ao consultar API: {e}")

    # Se já temos um processo salvo na sessão, exibir os dados e botão para cadastrar
    if st.session_state.processo_digesto:
        processo_data = st.session_state.processo_digesto

        # Pré-processar dados com segurança
        numero = processo_data.get("numero", "-")
        classe = processo_data.get("classeNatureza") or "-"
        area = processo_data.get("area") or "-"
        tribunal = processo_data.get("tribunal") or "-"
        comarca = processo_data.get("comarca") or "-"
        valor = processo_data.get("valor")
        valor_formatado = f"R$ {valor:,.2f}" if isinstance(valor, (int, float)) else "-"

        partes_principais = []
        for parte in processo_data.get("partes", []):
            if isinstance(parte, list) and len(parte) > 8 and parte[8] in ["EXEQUENTE", "EXECUTADO", "IMPETRANTE", "IMPETRADO"]:
                partes_principais.append((parte[8], parte[3]))

        anexos_processados = []
        for anexo in processo_data.get("anexos", []):
            if isinstance(anexo, list) and len(anexo) > 6:
                titulo = anexo[6] or "Documento"
                link = anexo[1]
                data = anexo[3][:10] if anexo[3] else "-"
                anexos_processados.append((titulo, link, data))

        with st.expander("📄 Visualizar dados do processo", expanded=True):
            st.markdown(f"**Número:** `{numero}`")
            st.markdown(f"**Classe:** {classe}")
            st.markdown(f"**Área:** {area}")
            st.markdown(f"**Tribunal:** {tribunal}")
            st.markdown(f"**Comarca:** {comarca}")
            st.markdown(f"**Valor da causa:** {valor_formatado}")

            st.markdown("**👥 Partes principais:**")
            for tipo, nome in partes_principais:
                st.markdown(f"- {tipo}: **{nome}**")

            st.markdown("**📎 Anexos:**")
            for titulo, link, data in anexos_processados:
                st.markdown(f"- [{titulo} - {data}]({link})")

        if st.button("✅ Cadastrar no sistema"):
            with st.spinner("Enviando para a API do sistema..."):
                fake_file = io.StringIO(json.dumps(processo_data))
                upload = requests.post(
                    f"{API_URL}/upload-json-bruto/",
                    files={"json_file": ("processo.json", fake_file, "application/json")}
                )
                if upload.status_code == 200:
                    resultado = upload.json()
                    if "já existe" in resultado.get("mensagem", "").lower():
                        st.warning("⚠️ O processo já está cadastrado no sistema.")
                    else:
                        st.success("✅ Processo cadastrado com sucesso!")
                    st.session_state.processo_digesto = None  # Limpa da sessão
                else:
                    st.error("Erro ao cadastrar processo.")
                    st.text(upload.text)
