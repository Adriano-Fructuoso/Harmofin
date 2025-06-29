""" app.py
	•	O que vai aqui:
O ponto de entrada da aplicação Streamlit.
	•	Responsabilidades:
	•	Montar a interface do dashboard (usando streamlit).
	•	Chamar funções que vêm da pasta finance/ para manipular e exibir os dados.
	•	Exibir tabelas, gráficos e formulários para o usuário interagir.
	•	Não deve ter lógica pesada, só orquestra o que está vindo de outros arquivos.
	•	Exemplo:
	•	Recebe dados de finance/core.py
	•	Monta gráficos usando funções de finance/charts.py """

# app.py

import streamlit as st
from finance.core import (
    carregar_dados,
    salvar_dados,
    adicionar_lancamento,
    listar_lancamentos,
    remover_lancamento,
    editar_lancamento,
    filtrar_por_categoria,
    buscar_por_periodo,
    calcular_somatorio_geral,
    calcular_somatorio_por_categoria,
    calcular_evolucao_mensal,
    comparar_meses,
    obter_top_categorias_mes,
    calcular_media_mensal
)
from finance.charts import grafico_despesas_por_categoria, grafico_receitas_por_categoria, grafico_saldo_ao_longo_do_tempo
import pandas as pd
from streamlit import column_config
import os
import json

# ==============================
# INÍCIO DO DASHBOARD FINANCEIRO
# ==============================

# --- LOGIN SIMPLES ---
USUARIOS_PATH = "data/usuarios.json"

# Função para criar arquivo CSV inicial para novo usuário
def criar_arquivo_inicial_usuario(usuario):
    """
    Cria o arquivo CSV inicial para um novo usuário.
    """
    try:
        data_path = f"data/dados_{usuario}.csv"
        
        # Criar DataFrame vazio com colunas padrão (usando a mesma abordagem do carregar_dados)
        colunas = pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])
        df_inicial = pd.DataFrame(columns=colunas)
        
        # Salvar DataFrame vazio
        salvar_dados(df_inicial, data_path)
        
        print(f"Arquivo inicial criado para usuário {usuario}: {data_path}")
        return True
        
    except Exception as e:
        print(f"ERRO ao criar arquivo inicial para {usuario}: {e}")
        return False

# Carregar usuários do arquivo, se existir
if os.path.exists(USUARIOS_PATH):
    with open(USUARIOS_PATH, "r") as f:
        USUARIOS = json.load(f)
else:
    USUARIOS = {"Adriano": "142536"}
    with open(USUARIOS_PATH, "w") as f:
        json.dump(USUARIOS, f)

# Verificar se o usuário está logado
if "usuario_logado" not in st.session_state:
    # Configurar página para login (sem sidebar)
    st.set_page_config(
        page_title="Login - Dashboard Financeiro",
        page_icon="💰",
        layout="centered"
    )
    
    # Centralizar o formulário de login
    st.title("💰 Dashboard Financeiro Pessoal")
    st.markdown("---")
    
    # Criar duas colunas para centralizar o formulário
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Login")
        aba = st.radio("Escolha uma opção:", ["Entrar", "Criar nova conta"])
        
        if aba == "Entrar":
            usuario = st.text_input("Nome de usuário")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if usuario and senha:
                    if usuario in USUARIOS and senha == USUARIOS[usuario]:
                        st.session_state["usuario_logado"] = usuario
                        st.success("Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos")
                else:
                    st.warning("Preencha usuário e senha.")
        else:
            novo_usuario = st.text_input("Novo nome de usuário")
            nova_senha = st.text_input("Nova senha", type="password")
            if st.button("Criar conta", use_container_width=True):
                if not novo_usuario or not nova_senha:
                    st.warning("Preencha usuário e senha.")
                elif novo_usuario in USUARIOS:
                    st.error("Usuário já existe!")
                else:
                    USUARIOS[novo_usuario] = nova_senha
                    with open(USUARIOS_PATH, "w") as f:
                        json.dump(USUARIOS, f)
                    
                    # Criar arquivo CSV inicial para o novo usuário
                    if criar_arquivo_inicial_usuario(novo_usuario):
                        st.session_state["usuario_logado"] = novo_usuario
                        st.success("Conta criada e login realizado!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar arquivo de dados. Tente novamente.")
    
    st.stop()

# Após o login, configurar a página normal com sidebar
st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="💰",
    layout="wide"
)

# Título e introdução
st.title("Dashboard Financeiro Pessoal")
st.write("Bem-vindo! Use o menu ao lado para navegar pelo seu financeiro.")

# Sidebar para navegação e formulário de novos lançamentos (só aparece após login)
menu = st.sidebar.selectbox("Selecione uma opção:", ["Resumo", "Novo Lançamento", "Relatórios Mensais", "Relatórios"])

usuario = st.session_state["usuario_logado"]
DATA_PATH = f"data/dados_{usuario}.csv"

# Inicializar dados na session_state se não existir
if 'df_dados' not in st.session_state:
    st.session_state['df_dados'] = carregar_dados(DATA_PATH)

# Função para atualizar dados na session_state
def atualizar_dados():
    st.session_state['df_dados'] = carregar_dados(DATA_PATH)

# Função para sincronizar dados da session_state com o arquivo CSV
def sincronizar_dados():
    """
    Garante que os dados da session_state estejam sincronizados com o arquivo CSV.
    Útil para garantir persistência após operações de CRUD.
    """
    try:
        # Recarregar dados do arquivo CSV
        df_atual = carregar_dados(DATA_PATH)
        
        # Atualizar session_state
        st.session_state['df_dados'] = df_atual
        
        print(f"Dados sincronizados: {len(df_atual)} registros")
        return True
        
    except Exception as e:
        print(f"ERRO na sincronização: {e}")
        return False

# Botão para atualizar dados manualmente
if st.sidebar.button("🔄 Atualizar Dados"):
    if sincronizar_dados():
        st.sidebar.success("Dados sincronizados com sucesso!")
    else:
        st.sidebar.error("Erro ao sincronizar dados!")

if menu == "Resumo":
    st.header("Resumo Financeiro")
    
    # Usar dados da session_state
    df = st.session_state['df_dados']
    
    # Garantir que as colunas de filtro sejam categóricas
    if len(df) > 0:
        df['Categoria'] = df['Categoria'].astype('category')
        df['Tipo'] = df['Tipo'].astype('category')
    
    # Calcula o somatório geral
    somatorio = calcular_somatorio_geral(df)
    
    # Calcula o total da categoria 'Investimentos'
    total_investimentos = float(df[df['Categoria'] == 'Investimentos']['Valor'].sum())
    
    # Exibe o somatório geral em cards
    st.subheader("📊 Resumo Geral")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 Total de Receitas",
            value=f"R$ {somatorio['receitas']:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="💸 Total de Despesas",
            value=f"R$ {somatorio['despesas']:,.2f}",
            delta=None
        )
    
    with col3:
        saldo_color = "normal" if somatorio['saldo'] >= 0 else "inverse"
        st.metric(
            label="💳 Saldo",
            value=f"R$ {somatorio['saldo']:,.2f}",
            delta=None,
            delta_color=saldo_color
        )
    
    # Linha separada para investimentos
    st.markdown("")
    col_inv = st.columns(1)
    with col_inv[0]:
        st.metric(
            label="📈 Investimentos",
            value=f"R$ {total_investimentos:,.2f}",
            delta=None
        )
    
    # Filtros temporais
    st.subheader("📅 Filtros Temporais")
    col_filtro1, col_filtro2 = st.columns(2)
    
    with col_filtro1:
        # Filtro por período
        if len(df) > 0:
            data_min = df['Data'].min()
            data_max = df['Data'].max()
            
            periodo = st.selectbox(
                "Selecione o período:",
                ["Todos os dados", "Último mês", "Últimos 3 meses", "Últimos 6 meses", "Este ano", "Período personalizado"]
            )
            
            if periodo == "Período personalizado":
                data_inicio = st.date_input("Data de início", data_min)
                data_fim = st.date_input("Data de fim", data_max)
            elif periodo == "Último mês":
                data_fim = data_max
                data_inicio = data_fim - pd.DateOffset(months=1)
            elif periodo == "Últimos 3 meses":
                data_fim = data_max
                data_inicio = data_fim - pd.DateOffset(months=3)
            elif periodo == "Últimos 6 meses":
                data_fim = data_max
                data_inicio = data_fim - pd.DateOffset(months=6)
            elif periodo == "Este ano":
                data_inicio = pd.Timestamp(data_max.year, 1, 1)
                data_fim = data_max
            else:  # Todos os dados
                data_inicio = data_min
                data_fim = data_max
        else:
            periodo = "Todos os dados"
            data_inicio = pd.Timestamp.now()
            data_fim = pd.Timestamp.now()
    
    with col_filtro2:
        # Filtro por mês específico
        if len(df) > 0:
            meses_disponiveis = sorted(df['Data'].dt.to_period('M').unique(), reverse=True)
            meses_opcoes = [str(mes) for mes in meses_disponiveis]
            meses_opcoes.insert(0, "Todos os meses")
            
            mes_selecionado = st.selectbox("Mês específico:", meses_opcoes)
        else:
            mes_selecionado = "Todos os meses"

    # Aplicar filtros temporais
    if len(df) > 0:
        df_filtrado_tempo = df[(df['Data'] >= data_inicio) & (df['Data'] <= data_fim)]
    else:
        df_filtrado_tempo = df

    # Botão para mostrar/ocultar filtro de categoria
    if st.button("Filtrar categoria"):
        if st.session_state.get('filtro_categoria_aberto', False):
            st.session_state['filtro_categoria_aberto'] = False
        else:
            st.session_state['filtro_categoria_aberto'] = True

    if st.session_state.get('filtro_categoria_aberto', False) and len(df_filtrado_tempo) > 0:
        categorias_unicas = sorted(df_filtrado_tempo['Categoria'].unique())
        # Estado para selecionar todas
        if 'todas_categorias_selecionadas' not in st.session_state:
            st.session_state['todas_categorias_selecionadas'] = True
        if st.button(
            "Selecionar todas" if not st.session_state['todas_categorias_selecionadas'] else "Desmarcar todas",
            key='btn_todas_categorias'):
            st.session_state['todas_categorias_selecionadas'] = not st.session_state['todas_categorias_selecionadas']
            st.rerun()
        if st.session_state['todas_categorias_selecionadas']:
            categorias_selecionadas = st.multiselect(
                "Selecione as categorias:",
                options=categorias_unicas,
                default=categorias_unicas,
                key='multiselect_categorias'
            )
        else:
            categorias_selecionadas = st.multiselect(
                "Selecione as categorias:",
                options=categorias_unicas,
                default=[],
                key='multiselect_categorias'
            )
        if not categorias_selecionadas:
            categorias_selecionadas = categorias_unicas  # Se nada selecionado, mostra tudo
    else:
        categorias_selecionadas = sorted(df_filtrado_tempo['Categoria'].unique()) if len(df_filtrado_tempo) > 0 else []

    # Aplicar filtro de categoria
    df_filtrado = df_filtrado_tempo[df_filtrado_tempo['Categoria'].isin(categorias_selecionadas)] if len(df_filtrado_tempo) > 0 else df_filtrado_tempo

    # Recalcular métricas com dados filtrados
    somatorio = calcular_somatorio_geral(df_filtrado)
    total_investimentos = float(df_filtrado[df_filtrado['Categoria'] == 'Investimentos']['Valor'].sum())

    # Formatar valores numéricos e datas para exibição
    df_exibir = pd.DataFrame(df_filtrado)
    if len(df_exibir) > 0:
        if 'Valor' in df_exibir.columns:
            df_exibir['Valor'] = df_exibir['Valor'].apply(lambda x: f"R$ {x:,.2f}")
        if 'Data' in df_exibir.columns:
            df_exibir['Data'] = pd.to_datetime(df_exibir['Data']).dt.strftime('%d/%m/%Y')
        df_exibir = df_exibir.rename(columns={
            "Data": "Data",
            "Descrição": "Descrição",
            "Categoria": "Categoria",
            "Tipo": "Tipo",
            "Valor": "Valor"
        })
    st.subheader("📋 Todos os Lançamentos")
    st.dataframe(
        df_exibir,
        use_container_width=True,
        hide_index=True
    )

    # --- Exclusão ---
    if st.button("🗑️ Excluir lançamento"):
        if st.session_state.get('excluir_aberto', False):
            st.session_state['excluir_aberto'] = False
        else:
            st.session_state['excluir_aberto'] = True

    if st.session_state.get('excluir_aberto', False) and len(df) > 0:
        opcoes_excluir = [
            f"{str(row['Data'])[:10]} | {row['Descrição']} | {row['Categoria']} | {row['Tipo']} | R$ {row['Valor']:,.2f}"
            for _, row in df.reset_index().iterrows()
        ]
        idx_excluir = st.selectbox(
            "Selecione um lançamento para excluir:",
            options=range(len(opcoes_excluir)),
            format_func=lambda i: opcoes_excluir[i],
            key='excluir_idx'
        )
        if st.button("Confirmar exclusão", key='confirmar_excluir'):
            remover_lancamento(idx_excluir, DATA_PATH)
            sincronizar_dados()  # Sincronizar dados após exclusão
            st.success("Lançamento excluído!")
            del st.session_state['excluir_aberto']
            st.rerun()

    # --- Edição ---
    if st.button("✏️ Editar lançamento"):
        if st.session_state.get('editar_aberto', False):
            st.session_state['editar_aberto'] = False
            if 'editar_idx' in st.session_state:
                del st.session_state['editar_idx']
        else:
            st.session_state['editar_aberto'] = True

    if st.session_state.get('editar_aberto', False) and len(df) > 0:
        opcoes_edit = [
            f"{str(row['Data'])[:10]} | {row['Descrição']} | {row['Categoria']} | {row['Tipo']} | R$ {row['Valor']:,.2f}"
            for _, row in df.reset_index().iterrows()
        ]
        idx_edit = st.selectbox(
            "Selecione um lançamento para editar:",
            options=range(len(opcoes_edit)),
            format_func=lambda i: opcoes_edit[i],
            key='editar_idx_selectbox'
        )
        if st.button("Editar este lançamento", key="confirmar_editar"):
            st.session_state['editar_idx'] = idx_edit

    # Formulário de edição
    if st.session_state.get('editar_aberto', False) and 'editar_idx' in st.session_state:
        editar_idx = st.session_state['editar_idx']
        row = df.iloc[editar_idx]
        st.markdown("---")
        st.subheader("Editar lançamento")
        with st.form("form_editar_lancamento"):
            data_edit = st.date_input("Data", pd.to_datetime(row['Data']))
            descricao_edit = st.text_input("Descrição", row['Descrição'])
            categoria_edit = st.text_input("Categoria", row['Categoria'])
            tipo_edit = st.selectbox("Tipo", ["Receita", "Despesa"], index=0 if row['Tipo']=="Receita" else 1)
            valor_edit = st.number_input("Valor", min_value=0.0, step=0.01, value=float(row['Valor']))
            submit_edit = st.form_submit_button("Salvar alterações")
            if submit_edit:
                editar_lancamento(editar_idx, data_edit, descricao_edit, categoria_edit, tipo_edit, valor_edit, DATA_PATH)
                sincronizar_dados()  # Sincronizar dados após edição
                st.success("Lançamento editado com sucesso!")
                del st.session_state['editar_aberto']
                del st.session_state['editar_idx']
                st.rerun()
    
    # Gráficos um abaixo do outro, ocupando toda a largura
    if len(df) > 0:
        st.subheader("📈 Análise por Categoria")
        st.write("**Receitas por categoria**")
        fig_receitas = grafico_receitas_por_categoria(df)
        st.pyplot(fig_receitas, use_container_width=True)
        st.write("**Despesas por categoria**")
        fig_despesas = grafico_despesas_por_categoria(df)
        st.pyplot(fig_despesas, use_container_width=True)

elif menu == "Novo Lançamento":
    st.header("Adicionar novo lançamento")

    # Listas fixas de categorias por tipo
    categorias_receita = [
        "Salário",
        "Mesada",
        "Investimentos",
        "Venda de Bens",
        "Transferências Recebidas",
        "Outros Pagamentos Recebidos"
    ]
    categorias_despesa = [
        "Alimentação",
        "Moradia",
        "Comunicação",
        "Cartão de Crédito",
        "Educação",
        "Saúde",
        "Lazer & Diversão",
        "Transferências Enviadas",
        "Outros Pagamentos"
    ]

    # Campo Tipo fora do form para atualização dinâmica
    tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
    if tipo == "Receita":
        categorias = categorias_receita
    else:
        categorias = categorias_despesa

    with st.form("form_lancamento"):
        data = st.date_input("Data")
        descricao = st.text_input("Descrição")
        categoria = st.selectbox("Categoria", categorias)
        valor = st.number_input("Valor", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Adicionar")
        if submit:
            adicionar_lancamento(data, descricao, categoria, tipo, valor, DATA_PATH)
            sincronizar_dados()  # Sincronizar dados após adição
            st.success("Lançamento adicionado!")

elif menu == "Relatórios Mensais":
    st.header("📊 Relatórios Mensais")
    
    # Usar dados da session_state
    df = st.session_state['df_dados']
    
    if len(df) > 0:
        # Adicionar colunas de mês e ano para análise
        df['Ano'] = df['Data'].dt.year
        df['Mes'] = df['Data'].dt.month
        df['Mes_Ano'] = df['Data'].dt.to_period('M')
        
        # Obter meses disponíveis
        meses_disponiveis = sorted(df['Mes_Ano'].unique(), reverse=True)
        
        st.subheader("📈 Comparativo Mensal")
        
        # Selecionar meses para comparação
        col1, col2 = st.columns(2)
        
        with col1:
            mes1 = st.selectbox(
                "Selecione o primeiro mês:",
                options=meses_disponiveis,
                format_func=lambda x: str(x)
            )
        
        with col2:
            mes2 = st.selectbox(
                "Selecione o segundo mês:",
                options=meses_disponiveis,
                format_func=lambda x: str(x)
            )
        
        # Usar função de comparação
        comparacao = comparar_meses(df, mes1, mes2)
        
        if comparacao:
            # Exibir comparação
            st.subheader(f"Comparação: {mes1} vs {mes2}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f"Receitas {mes1}",
                    value=f"R$ {comparacao['mes1']['receitas']:,.2f}",
                    delta=f"R$ {comparacao['diferenca']['receitas']:,.2f}" if mes1 != mes2 else None
                )
            
            with col2:
                st.metric(
                    label=f"Despesas {mes1}",
                    value=f"R$ {comparacao['mes1']['despesas']:,.2f}",
                    delta=f"R$ {comparacao['diferenca']['despesas']:,.2f}" if mes1 != mes2 else None
                )
            
            with col3:
                st.metric(
                    label=f"Saldo {mes1}",
                    value=f"R$ {comparacao['mes1']['saldo']:,.2f}",
                    delta=f"R$ {comparacao['diferenca']['saldo']:,.2f}" if mes1 != mes2 else None
                )
        
        # Evolução mensal dos últimos 6 meses
        st.subheader("📈 Evolução dos Últimos 6 Meses")
        
        df_evolucao = calcular_evolucao_mensal(df, 6)
        
        if len(df_evolucao) > 0:
            # Gráfico de evolução
            import matplotlib.pyplot as plt
            
            fig, ax = plt.subplots(figsize=(12, 6))
            x = range(len(df_evolucao))
            
            ax.plot(x, df_evolucao['Receitas'], marker='o', label='Receitas', linewidth=2)
            ax.plot(x, df_evolucao['Despesas'], marker='s', label='Despesas', linewidth=2)
            ax.plot(x, df_evolucao['Saldo'], marker='^', label='Saldo', linewidth=2)
            
            ax.set_xlabel('Mês')
            ax.set_ylabel('Valor (R$)')
            ax.set_title('Evolução Financeira Mensal')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_xticks(x)
            ax.set_xticklabels(df_evolucao['Mes'], rotation=45)
            
            st.pyplot(fig)
            
            # Médias mensais
            medias = calcular_media_mensal(df, 6)
            if medias:
                st.subheader("📊 Médias dos Últimos 6 Meses")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Receitas Média", f"R$ {medias['receitas_media']:,.2f}")
                with col2:
                    st.metric("Despesas Média", f"R$ {medias['despesas_media']:,.2f}")
                with col3:
                    st.metric("Saldo Média", f"R$ {medias['saldo_media']:,.2f}")
        
        # Top categorias por mês
        st.subheader("🏆 Top Categorias por Mês")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{mes1}**")
            top_receitas_mes1 = obter_top_categorias_mes(df, mes1, 'Receita', 5)
            top_despesas_mes1 = obter_top_categorias_mes(df, mes1, 'Despesa', 5)
            
            if len(top_receitas_mes1) > 0:
                st.write("**Top Receitas:**")
                for cat, valor in top_receitas_mes1.items():
                    st.write(f"• {cat}: R$ {valor:,.2f}")
            
            if len(top_despesas_mes1) > 0:
                st.write("**Top Despesas:**")
                for cat, valor in top_despesas_mes1.items():
                    st.write(f"• {cat}: R$ {valor:,.2f}")
        
        with col2:
            st.write(f"**{mes2}**")
            top_receitas_mes2 = obter_top_categorias_mes(df, mes2, 'Receita', 5)
            top_despesas_mes2 = obter_top_categorias_mes(df, mes2, 'Despesa', 5)
            
            if len(top_receitas_mes2) > 0:
                st.write("**Top Receitas:**")
                for cat, valor in top_receitas_mes2.items():
                    st.write(f"• {cat}: R$ {valor:,.2f}")
            
            if len(top_despesas_mes2) > 0:
                st.write("**Top Despesas:**")
                for cat, valor in top_despesas_mes2.items():
                    st.write(f"• {cat}: R$ {valor:,.2f}")
    
    else:
        st.info("Adicione lançamentos para ver os relatórios mensais.")

elif menu == "Relatórios":
    st.header("Relatórios avançados (em breve)")
    # Aqui podem entrar gráficos de saldo, metas, exportações, etc.

# ==============================
# FIM DO DASHBOARD
# ==============================

# Observações:
# - Toda lógica pesada fica em finance/core.py (salvar, carregar, filtrar dados).
# - Toda lógica de gráficos fica em finance/charts.py.
# - O app.py apenas chama essas funções e monta a interface.