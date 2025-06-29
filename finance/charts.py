"""	•	O que vai aqui:
Funções para gerar gráficos dos dados.
	•	Responsabilidades:
	•	Montar gráficos de pizza, barra, linha, etc.
	•	Recebe DataFrame (do pandas) e retorna um gráfico pronto para o Streamlit exibir.
	•	Exemplo de funções:
	•	grafico_despesas_por_categoria(df)
	•	grafico_saldo_ao_longo_do_tempo(df)"""

# finance/charts.py

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def grafico_despesas_por_categoria(df):
    """
    Gera um gráfico de pizza mostrando o total de despesas por categoria.
    Recebe o DataFrame filtrado (ou geral).
    Retorna a figura pronta para ser exibida no Streamlit.
    """
    despesas = df[df['Tipo'] == 'Despesa']
    if despesas.empty:
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.text(0.5, 0.5, 'Nenhuma despesa registrada\nAdicione despesas para ver o gráfico', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=14, color='gray')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Despesas por Categoria')
        return fig
    categorias = despesas.groupby('Categoria')['Valor'].sum()
    categorias = categorias[categorias > 0]
    categorias = categorias.sort_values(ascending=False)
    valor_total = categorias.sum()
    labels = [cat for cat in categorias.index]
    cores = plt.get_cmap('tab20')(np.arange(len(categorias))).tolist()
    fig, ax = plt.subplots(figsize=(14, 7))
    pie_result = ax.pie(
        categorias,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else '',
        startangle=90,
        colors=cores,
        textprops={'fontsize': 13}
    )
    ax.set_ylabel('')
    ax.set_title(f'Despesas por Categoria (Total R$ {valor_total:,.2f})', fontsize=15)
    return fig

def grafico_saldo_ao_longo_do_tempo(df):
    """
    Gera um gráfico de linha mostrando o saldo acumulado ao longo do tempo.
    Recebe o DataFrame completo.
    Retorna a figura pronta para o Streamlit.
    """
    # Cria uma coluna "Sinal" para receitas/depesa (+/-)
    df_sorted = df.sort_values('Data')
    df_sorted['Valor Ajustado'] = df_sorted.apply(
        lambda row: row['Valor'] if row['Tipo'] == 'Receita' else -row['Valor'],
        axis=1
    )
    df_sorted['Saldo Acumulado'] = df_sorted['Valor Ajustado'].cumsum()

    fig, ax = plt.subplots()
    ax.plot(df_sorted['Data'], df_sorted['Saldo Acumulado'], marker='o')
    ax.set_xlabel('Data')
    ax.set_ylabel('Saldo Acumulado')
    ax.set_title('Saldo ao longo do tempo')
    ax.grid(True)

    return fig

def grafico_receitas_por_categoria(df):
    """
    Gera um gráfico de pizza mostrando o total de receitas por categoria.
    Recebe o DataFrame filtrado (ou geral).
    Retorna a figura pronta para ser exibida no Streamlit.
    """
    receitas = df[df['Tipo'] == 'Receita']
    if receitas.empty:
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.text(0.5, 0.5, 'Nenhuma receita registrada\nAdicione receitas para ver o gráfico', 
                ha='center', va='center', transform=ax.transAxes, 
                fontsize=14, color='gray')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Receitas por Categoria')
        return fig
    categorias = receitas.groupby('Categoria')['Valor'].sum()
    categorias = categorias[categorias > 0]
    categorias = categorias.sort_values(ascending=False)
    valor_total = categorias.sum()
    labels = [cat for cat in categorias.index]
    cores = plt.get_cmap('tab20')(np.arange(len(categorias))).tolist()
    fig, ax = plt.subplots(figsize=(14, 7))
    pie_result = ax.pie(
        categorias,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else '',
        startangle=90,
        colors=cores,
        textprops={'fontsize': 13}
    )
    ax.set_ylabel('')
    ax.set_title(f'Receitas por Categoria (Total R$ {valor_total:,.2f})', fontsize=15)
    return fig
