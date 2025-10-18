import streamlit as st
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Cadastro de Impostos", page_icon="🟪", layout="centered")

# Senha fixa
PASSWORD = "minhasenha123"

# Inicializa estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔒 Esconde a barra lateral com CSS se não estiver logado
if not st.session_state.logged_in:
    hide_sidebar = """
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

# Se não estiver logado, pede senha
if not st.session_state.logged_in:
    st.title("Acesso Restrito")
    senha = st.text_input("Digite a senha:", type="password")
    if st.button("Entrar"):
        if senha == PASSWORD:
            st.session_state.logged_in = True
            st.success("Acesso liberado! Agora você pode navegar pelas páginas.")
            st.rerun()
        else:
            st.error("Senha incorreta.")
else:
    # 🔒 Conteúdo protegido
    st.image('teste.svg', width=400)

    FILE_PATH = "impostos.csv"

    def load_data():
        if os.path.exists(FILE_PATH):
            return pd.read_csv(FILE_PATH)
        else:
            return pd.DataFrame(columns=[
                "codigo_conta", "nome_imposto", "data_envio", "competencia",
                "valor", "mora", "tx_expediente", "atualizacao", "multa", "juros",
                "desconto", "total", "vencimento", "texto_lacto", "data_pagamento", "banco"
            ])

    def save_data(df):
        df.to_csv(FILE_PATH, index=False, sep=",", encoding="utf-8")

    data = load_data()

    codigo_conta = {
        "1 - 2300390": "2300390",
        "2 - 2300391": "2300391",
        "3 - 2300393": "2300393",
        "4 - 2300394": "2300394",
        "5 - 2300395": "2300395",
        "6 - 2300396": "2300396",
        "7 - 2300397": "2300397",
        "8 - 2360020": "2360020",
        "9 - 2360022": "2360022",
        "10 - 2360023": "2360023",
        "11 - 2360024": "2360024",
        "12 - 2360028": "2360028",
        "13 - 1280349": "1280349",
        "14 - 6102005": "6102005",
        "15 - 6114000": "6114000"
    }

    nomes_impostos = [
        "IPI a recolher", "ISS retido", "GNRE ANTECIPADO", "Taxas", "Parcelamento CP",
        "ICMS a recolher", "ICMS ST", "Outros impostos", "Cofins a recolher", "PIS a recolher",
        "ISS prestado", "ICMS PROPRIO", "ICMS FECAP PROPRIO", "ICMS ST INTERNO", "ICMS FECAP ST",
        "ICMS ST", "ICMS ANTECIPADO", "GUIA PARCELAMENTO", "TAXA VIGILANCIA", "ISS RETIDO",
        "TAXA FISCALIZAÇÃO", "ICMS FECAP", "GARE ICMS", "GARE ICMS ST INTERNO", "TAXA",
        "GUIA MIT", "ICMS", "ICMS FECP Antecipado", "ICMS DIFAL", "FECAP PROPRIO", "FECAP ST",
        "PARCELAMENTO"
    ]

    competencias = [f"{str(m).zfill(2)}/2025" for m in range(1, 13)]

    bancos_originais = [
        "Banco do Brasil", "Bradesco", "Bradesco/1061002", "Bradesco/1061052",
        "Outros", "Itaú"
    ]
    bancos_filtrados = [b for b in bancos_originais if not b.startswith("Bradesco/")]

    menu = st.sidebar.selectbox("Menu", ["Cadastrar Imposto"])

    if menu == "Cadastrar Imposto":
        st.title("Cadastro de Imposto")

        codigo_conta_sel = st.selectbox("Código do Imposto / Conta", list(codigo_conta.keys()))
        nome_imposto = st.selectbox("Nome do Imposto", nomes_impostos)
        data_envio = st.date_input("Data de Envio", format="DD/MM/YYYY")
        competencia = st.selectbox("Competência", competencias)

        valor = st.text_input("Valor", "0,00")
        mora = st.text_input("Mora", "0,00")
        tx_expediente = st.text_input("Tx. Expediente", "0,00")
        atualizacao = st.text_input("Atualização", "0,00")
        multa = st.text_input("Multa", "0,00")
        juros = st.text_input("Juros", "0,00")
        desconto = st.text_input("Desconto", "0,00")
        total = st.text_input("Total", "0,00")

        vencimento = st.date_input("Vencimento", format="DD/MM/YYYY")
        texto_lacto = st.text_input("Texto Lacto")
        data_pagamento = st.date_input("Data de Pagamento", format="DD/MM/YYYY")
        banco = st.selectbox("Banco", bancos_filtrados)

        if st.button("Salvar"):
            def to_float(val):
                try:
                    return float(val.replace(",", "."))
                except:
                    return 0.0

            new_row = {
                "codigo_conta": codigo_conta_sel,
                "nome_imposto": nome_imposto,
                "data_envio": data_envio.strftime("%d/%m/%Y"),
                "competencia": competencia,
                "valor": to_float(valor),
                "mora": to_float(mora),
                "tx_expediente": to_float(tx_expediente),
                "atualizacao": to_float(atualizacao),
                "multa": to_float(multa),
                "juros": to_float(juros),
                "desconto": to_float(desconto),
                "total": to_float(total),
                "vencimento": vencimento.strftime("%d/%m/%Y"),
                "texto_lacto": texto_lacto,
                "data_pagamento": data_pagamento.strftime("%d/%m/%Y"),
                "banco": banco
            }

            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            save_data(data)
            st.success("Registro salvo com sucesso!")

    elif menu == "Registros Cadastrados":
        st.title("Registros Cadastrados")
        st.dataframe(data, use_container_width=True)