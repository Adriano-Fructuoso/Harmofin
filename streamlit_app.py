"""
Aplicação Streamlit para o Sistema de Gestão de Clínicas de Harmonização
Interface web para a API FastAPI
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="Harmofin - Sistema de Gestão",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações da API
API_BASE_URL = "http://localhost:8001"  # Para desenvolvimento local
# API_BASE_URL = "https://seu-backend-deployado.com"  # Para produção

def check_api_health():
    """Verifica se a API está funcionando"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_data_from_api(endpoint):
    """Busca dados da API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro ao buscar dados: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")
        return None

# Header principal
st.title("🏥 Harmofin - Sistema de Gestão de Clínicas de Harmonização")
st.markdown("---")

# Sidebar para navegação
st.sidebar.title("📋 Menu")
page = st.sidebar.selectbox(
    "Selecione uma seção:",
    ["🏠 Dashboard", "👥 Clientes", "📋 Atendimentos", "💉 Procedimentos", "📦 Materiais", "🔧 Status da API"]
)

# Verificar status da API
api_status = check_api_health()

if page == "🏠 Dashboard":
    st.header("📊 Dashboard")
    
    if not api_status:
        st.warning("⚠️ API não está disponível. Verifique se o backend está rodando.")
        st.info("Para desenvolvimento local, execute: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001`")
    else:
        # Buscar estatísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            clientes_data = get_data_from_api("/api/v1/clientes")
            if clientes_data:
                st.metric("👥 Clientes", clientes_data.get("total", 0))
            else:
                st.metric("👥 Clientes", "N/A")
        
        with col2:
            atendimentos_data = get_data_from_api("/api/v1/atendimentos")
            if atendimentos_data:
                st.metric("📋 Atendimentos", atendimentos_data.get("total", 0))
            else:
                st.metric("📋 Atendimentos", "N/A")
        
        with col3:
            procedimentos_data = get_data_from_api("/api/v1/procedimentos")
            if procedimentos_data:
                st.metric("💉 Procedimentos", procedimentos_data.get("total", 0))
            else:
                st.metric("💉 Procedimentos", "N/A")
        
        with col4:
            materiais_data = get_data_from_api("/api/v1/materiais")
            if materiais_data:
                st.metric("📦 Materiais", materiais_data.get("total", 0))
            else:
                st.metric("📦 Materiais", "N/A")

elif page == "👥 Clientes":
    st.header("👥 Gestão de Clientes")
    
    if api_status:
        clientes_data = get_data_from_api("/api/v1/clientes")
        if clientes_data and "clientes" in clientes_data:
            df = pd.DataFrame(clientes_data["clientes"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum cliente encontrado.")
    else:
        st.warning("API não disponível")

elif page == "📋 Atendimentos":
    st.header("📋 Gestão de Atendimentos")
    
    if api_status:
        atendimentos_data = get_data_from_api("/api/v1/atendimentos")
        if atendimentos_data and "atendimentos" in atendimentos_data:
            df = pd.DataFrame(atendimentos_data["atendimentos"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum atendimento encontrado.")
    else:
        st.warning("API não disponível")

elif page == "💉 Procedimentos":
    st.header("💉 Gestão de Procedimentos")
    
    if api_status:
        procedimentos_data = get_data_from_api("/api/v1/procedimentos")
        if procedimentos_data and "procedimentos" in procedimentos_data:
            df = pd.DataFrame(procedimentos_data["procedimentos"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum procedimento encontrado.")
    else:
        st.warning("API não disponível")

elif page == "📦 Materiais":
    st.header("📦 Gestão de Materiais")
    
    if api_status:
        materiais_data = get_data_from_api("/api/v1/materiais")
        if materiais_data and "materiais" in materiais_data:
            df = pd.DataFrame(materiais_data["materiais"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum material encontrado.")
    else:
        st.warning("API não disponível")

elif page == "🔧 Status da API":
    st.header("🔧 Status da API")
    
    if api_status:
        st.success("✅ API está funcionando corretamente!")
        
        # Testar endpoints
        endpoints = [
            ("/health", "Health Check"),
            ("/api/v1/clientes", "Clientes"),
            ("/api/v1/atendimentos", "Atendimentos"),
            ("/api/v1/procedimentos", "Procedimentos"),
            ("/api/v1/materiais", "Materiais")
        ]
        
        for endpoint, name in endpoints:
            with st.expander(f"Teste: {name}"):
                data = get_data_from_api(endpoint)
                if data:
                    st.json(data)
                else:
                    st.error(f"Erro ao acessar {endpoint}")
    else:
        st.error("❌ API não está disponível")
        st.info("""
        Para resolver:
        1. Verifique se o backend está rodando
        2. Confirme se a porta 8001 está livre
        3. Execute: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001`
        """)

# Footer
st.markdown("---")
st.markdown("**Harmofin** - Sistema de Gestão de Clínicas de Harmonização | v2.0.0") 