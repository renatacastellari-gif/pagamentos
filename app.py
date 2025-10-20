import streamlit as st
import psycopg2
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Teste de Conexão com Banco", layout="centered")

st.title("🧾 Teste de Conexão com Banco")

# --- Credenciais do Supabase (ajuste conforme seu projeto) ---
DB_USER = "postgres.etekiwkterkwrrpusob"  # copie exatamente do Supabase (usuário pooler)
DB_HOST = "aws-1-us-east-2.pooler.supabase.com"
DB_NAME = "postgres"
DB_PORT = "5432"
DB_PASSWORD = st.secrets["DB_PASSWORD"]  # senha armazenada no secrets.toml

# String de conexão
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Função de teste
def testar_conexao():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT NOW();"))
            data = result.fetchone()
        st.success(f"✅ Conexão bem-sucedida! Servidor respondeu em: {data[0]}")
    except Exception as e:
        st.error(f"❌ Erro ao conectar:\n\n{e}")

# Botão de teste
if st.button("Testar conexão agora"):
    testar_conexao()
