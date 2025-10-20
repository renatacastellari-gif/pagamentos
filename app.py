import streamlit as st
import pandas as pd
import re
from datetime import datetime
import pytz
from sqlalchemy import create_engine

# Configuração da página
st.set_page_config(page_title="Cadastro de Impostos", page_icon="🛠️", layout="centered")

# Conexão com Supabase
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@db.etekikwterktwrrpusob.supabase.co:5432/postgres"
engine = create_engine(DATABASE_URL)
TABLE_NAME = "cadastro_impostos"

# Usuários e senhas
USERS = {"admin": "senha_admin123", "financeiro": "senha_financeiro456"}

# Estado de login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.usuario = None

# Tela de login
if not st.session_state.logged_in:
    st.title("Acesso Restrito")
    usuario = st.text_input("Usuário:")
    senha = st.text_input("Senha:", type="password")
    if st.button("Entrar"):
        if usuario in USERS and senha == USERS[usuario]:
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.success(f"Acesso liberado para {usuario}!")
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

# Conteúdo protegido
if st.session_state.logged_in:
    st.markdown(f"🔒 Logado como **{st.session_state.usuario}**")

    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.session_state.usuario = None
        st.rerun()

    # Funções para banco
    def load_data():
        try:
            return pd.read_sql_table(TABLE_NAME, con=engine)
        except Exception:
            return pd.DataFrame(columns=[
                "codigo_conta", "nome_imposto", "data_envio", "competencia", "valor", "mora",
                "tx_expediente", "atualizacao", "multa", "juros", "desconto", "total",
                "vencimento", "texto_lacto", "data_pagamento", "banco",
                "ultima_edicao_por", "ultima_edicao_em"
            ])

    def save_data(df):
        df.to_sql(TABLE_NAME, con=engine, if_exists='append', index=False)

    data = load_data()

    # Dados fixos
    codigo_conta = {
        "1 - 2300390": "2300390", "2 - 2300391": "2300391", "3 - 2300393": "2300393",
        "4 - 2300394": "2300394", "5 - 2300395": "2300395", "6 - 2300396": "2300396"
    }
    nomes_impostos = ["IPI a recolher", "ISS retido", "ICMS a recolher", "Taxas"]
    competencias = [f"{str(m).zfill(2)}/2025" for m in range(1, 13)]
    bancos_filtrados = ["Banco do Brasil", "Bradesco", "Itaú", "Outros"]

    menu = st.sidebar.selectbox("Menu", ["Cadastrar Imposto", "Registros Cadastrados"])

    def validar_numero(valor):
        return bool(re.match(r'^\d+(,\d{1,2})?$', valor)) or valor == ""

    def to_float(val):
        return float(val.replace(",", ".")) if validar_numero(val) and val else 0.0

    # Cadastro
    if menu == "Cadastrar Imposto":
        st.title("Cadastro de Imposto")
        codigo_conta_sel = st.selectbox("Código do Imposto / Conta", [""] + list(codigo_conta.keys()))
        nome_imposto = st.selectbox("Nome do Imposto", [""] + nomes_impostos)
        data_envio = st.date_input("Data de Envio", format="DD/MM/YYYY")
        competencia = st.selectbox("Competência", [""] + competencias)

        valor = st.text_input("Valor", "")
        mora = st.text_input("Mora", "")
        tx_expediente = st.text_input("Tx. Expediente", "")
        atualizacao = st.text_input("Atualização", "")
        multa = st.text_input("Multa", "")
        juros = st.text_input("Juros", "")
        desconto = st.text_input("Desconto", "")

        vencimento = st.date_input("Vencimento", format="DD/MM/YYYY")
        texto_lacto = st.text_input("Texto Lacto", "")
        data_pagamento = st.date_input("Data de Pagamento", format="DD/MM/YYYY")
        banco = st.selectbox("Banco", [""] + bancos_filtrados)

        total_calc = (
            to_float(valor) + to_float(mora) + to_float(tx_expediente) +
            to_float(atualizacao) + to_float(multa) + to_float(juros) -
            to_float(desconto)
        )
        st.text_input("Total", f"{total_calc:,.2f}", disabled=True)

        if st.button("Salvar"):
            hora_brasilia = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")
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
                "total": total_calc,
                "vencimento": vencimento.strftime("%d/%m/%Y"),
                "texto_lacto": texto_lacto,
                "data_pagamento": data_pagamento.strftime("%d/%m/%Y"),
                "banco": banco,
                "ultima_edicao_por": st.session_state.usuario,
                "ultima_edicao_em": hora_brasilia
            }
            data = pd.DataFrame([new_row])
            save_data(data)
            st.success("Registro salvo com sucesso!")

    # Consulta
    elif menu == "Registros Cadastrados":
        st.title("Registros Cadastrados")
        filtro_conta = st.selectbox("Filtrar por Código/Conta", ["Todos"] + list(codigo_conta.keys()))
        filtro_competencia = st.selectbox("Filtrar por Competência", ["Todos"] + competencias)

        df_filtrado = data.copy()
        if filtro_conta != "Todos":
            df_filtrado = df_filtrado[df_filtrado["codigo_conta"] == filtro_conta]
        if filtro_competencia != "Todos":
            df_filtrado = df_filtrado[df_filtrado["competencia"] == filtro_competencia]

        edited_data = st.experimental_data_editor(df_filtrado, use_container_width=True, num_rows="dynamic")

        if st.button("Salvar Alterações"):
            hora_brasilia = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")
            edited_data["ultima_edicao_por"] = st.session_state.usuario
            edited_data["ultima_edicao_em"] = hora_brasilia
            save_data(edited_data)
            st.success("Alterações salvas com sucesso!")

        if st.button("Exportar para Excel"):
            edited_data.to_excel("impostos.xlsx", index=False)
            st.success("Arquivo Excel gerado com sucesso!")
