import streamlit as st
import requests
from utils import API_URL

def mostrar_formulario_edicao(processo):
    st.subheader(f"✏️ Editar Processo nº {processo.get('numero_processo')}")

    # Campos de texto
    instancia = st.text_input("Instância", value=processo.get("instancia", ""), key=f"instancia_{processo['id']}")
    jurisdicao = st.text_input("Jurisdição", value=processo.get("jurisdicao", ""), key=f"jurisdicao_{processo['id']}")
    orgao_julgador = st.text_input("Órgão Julgador", value=processo.get("orgao_julgador", ""), key=f"orgao_{processo['id']}")
    competencia = st.text_input("Competência", value=processo.get("competencia", ""), key=f"competencia_{processo['id']}")
    classe = st.text_input("Classe", value=processo.get("classe", ""), key=f"classe_{processo['id']}")
    assunto = st.text_input("Assunto", value=processo.get("assunto", ""), key=f"assunto_{processo['id']}")
    exequente = st.text_input("Exequente", value=processo.get("exequente", ""), key=f"exequente_{processo['id']}")
    executado = st.text_input("Executado", value=processo.get("executado", ""), key=f"executado_{processo['id']}")
    
    # Lista de advogados (como texto separado por vírgulas)
    advogados_texto = ", ".join(processo.get("advogados", []))
    advogados_input = st.text_input("Advogados (separados por vírgula)", value=advogados_texto, key=f"advogados_{processo['id']}")
    advogados_lista = [adv.strip() for adv in advogados_input.split(",") if adv.strip()]

    # Valor da causa
    valor_causa = st.number_input("Valor da Causa (R$)", value=float(processo.get("valor_causa", 0)), key=f"valor_{processo['id']}")

    # Gratuidade
    gratuidade = st.checkbox("Gratuidade", value=processo.get("gratuidade", False), key=f"gratuidade_{processo['id']}")

    if st.button("💾 Salvar Alterações", key=f"salvar_{processo['id']}"):
        payload = {
            "instancia": instancia,
            "jurisdicao": jurisdicao,
            "orgao_julgador": orgao_julgador,
            "competencia": competencia,
            "classe": classe,
            "assunto": assunto,
            "exequente": exequente,
            "executado": executado,
            "advogados": advogados_lista,
            "valor_causa": valor_causa,
            "gratuidade": gratuidade
        }

        response = requests.put(f"{API_URL}/processos/{processo['id']}", json=payload)
        if response.status_code == 200:
            st.success("Processo atualizado com sucesso!")
            st.session_state.processo_editando = None
        else:
            st.error("Erro ao atualizar processo.")

