import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

# Monta string de conexão a partir do secrets.toml
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]
DB_NAME = st.secrets["DB_NAME"]

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Teste de conexão
st.title("🧾 Teste de Conexão com Banco")

if st.button("Testar conexão agora"):
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute("SELECT NOW();")
            st.success(f"✅ Conectado com sucesso! Hora atual no banco: {list(result)[0][0]}")
    except Exception as e:
        st.error(f"❌ Erro ao conectar: {e}")
