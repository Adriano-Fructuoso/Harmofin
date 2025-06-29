"""	•	O que vai aqui:
Toda a lógica principal de manipulação dos dados financeiros.
	•	Responsabilidades:
	•	Funções para: adicionar lançamento, remover, editar, listar, buscar por período/categoria, salvar e carregar CSV.
	•	Isola as regras do negócio e evita poluir o app.py.
	•	Exemplo de funções que terão aqui:
	•	adicionar_lancamento()
	•	listar_lancamentos()
	•	salvar_dados()
	•	carregar_dados()
	•	filtrar_por_categoria() """

# finance/core.py

import pandas as pd
from datetime import datetime
import os

def carregar_dados(data_path):
    """
    Carrega os dados financeiros do arquivo CSV.
    Retorna um DataFrame pandas.
    """
    try:
        print(f"Tentando carregar dados de: {data_path}")
        
        if os.path.exists(data_path):
            df = pd.read_csv(data_path, parse_dates=['Data'])
            print(f"Dados carregados com sucesso: {len(df)} registros")
            return df
        else:
            # Se não existir, retorna um DataFrame vazio com colunas padrão
            print(f"Arquivo não existe. Criando DataFrame vazio.")
            colunas = pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])
            df = pd.DataFrame(columns=colunas)
            return df
            
    except Exception as e:
        print(f"ERRO ao carregar dados: {e}")
        # Em caso de erro, retorna DataFrame vazio
        colunas = pd.Index(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor'])
        df = pd.DataFrame(columns=colunas)
        return df

def salvar_dados(df, data_path):
    """
    Salva o DataFrame no arquivo CSV.
    """
    try:
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        
        # Salvar o DataFrame
        df.to_csv(data_path, index=False)
        
        # Verificar se o arquivo foi criado/atualizado
        if os.path.exists(data_path):
            print(f"Dados salvos com sucesso em: {data_path}")
            print(f"Total de registros salvos: {len(df)}")
        else:
            print(f"ERRO: Arquivo não foi criado em: {data_path}")
            
    except Exception as e:
        print(f"ERRO ao salvar dados: {e}")
        raise e

def adicionar_lancamento(data, descricao, categoria, tipo, valor, data_path):
    """
    Adiciona um novo lançamento (receita ou despesa).
    """
    try:
        print(f"Adicionando lançamento: {descricao} - {categoria} - {tipo} - R$ {valor}")
        
        df = carregar_dados(data_path)
        print(f"Dados carregados: {len(df)} registros existentes")
        
        novo = {
            'Data': pd.to_datetime(data),
            'Descrição': descricao,
            'Categoria': categoria,
            'Tipo': tipo,
            'Valor': float(valor)
        }
        
        df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
        print(f"Novo DataFrame criado: {len(df)} registros")
        
        salvar_dados(df, data_path)
        print(f"Lançamento adicionado com sucesso!")
        
    except Exception as e:
        print(f"ERRO ao adicionar lançamento: {e}")
        raise e

def listar_lancamentos(data_path):
    """
    Retorna todos os lançamentos como DataFrame.
    """
    return carregar_dados(data_path)

def remover_lancamento(indice, data_path):
    """
    Remove um lançamento pelo índice (linha) no DataFrame.
    """
    try:
        print(f"Removendo lançamento no índice: {indice}")
        
        df = carregar_dados(data_path)
        print(f"Dados carregados: {len(df)} registros existentes")
        
        if indice < len(df):
            df = df.drop(indice).reset_index(drop=True)
            print(f"Lançamento removido. Novo total: {len(df)} registros")
            salvar_dados(df, data_path)
            print("Dados salvos após remoção!")
        else:
            print(f"ERRO: Índice {indice} não existe. Total de registros: {len(df)}")
            
    except Exception as e:
        print(f"ERRO ao remover lançamento: {e}")
        raise e

def editar_lancamento(indice, data, descricao, categoria, tipo, valor, data_path):
    """
    Edita um lançamento existente pelo índice (linha).
    """
    try:
        print(f"Editando lançamento no índice: {indice}")
        print(f"Novos dados: {descricao} - {categoria} - {tipo} - R$ {valor}")
        
        df = carregar_dados(data_path)
        print(f"Dados carregados: {len(df)} registros existentes")
        
        if indice < len(df):
            df.at[indice, 'Data'] = pd.to_datetime(data)
            df.at[indice, 'Descrição'] = descricao
            df.at[indice, 'Categoria'] = categoria
            df.at[indice, 'Tipo'] = tipo
            df.at[indice, 'Valor'] = float(valor)
            
            print(f"Lançamento editado. Total de registros: {len(df)}")
            salvar_dados(df, data_path)
            print("Dados salvos após edição!")
        else:
            print(f"ERRO: Índice {indice} não existe. Total de registros: {len(df)}")
            
    except Exception as e:
        print(f"ERRO ao editar lançamento: {e}")
        raise e

def filtrar_por_categoria(categoria, data_path):
    """
    Filtra os lançamentos pela categoria.
    """
    df = carregar_dados(data_path)
    return df[df['Categoria'] == categoria]

def buscar_por_periodo(data_inicio, data_fim, data_path):
    """
    Filtra os lançamentos dentro de um período.
    """
    df = carregar_dados(data_path)
    mask = (df['Data'] >= pd.to_datetime(data_inicio)) & (df['Data'] <= pd.to_datetime(data_fim))
    return df[mask]

def calcular_somatorio_geral(df):
    """
    Calcula o somatório geral de receitas, despesas e saldo.
    Retorna um dicionário com os valores.
    """
    receitas = df[df['Tipo'] == 'Receita']['Valor'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    saldo = receitas - despesas
    
    return {
        'receitas': receitas,
        'despesas': despesas,
        'saldo': saldo
    }

def calcular_somatorio_por_categoria(df):
    """
    Calcula o somatório por categoria separando receitas e despesas.
    Retorna dois dicionários: um para receitas e outro para despesas.
    """
    receitas_por_categoria = df[df['Tipo'] == 'Receita'].groupby('Categoria')['Valor'].sum().to_dict()
    despesas_por_categoria = df[df['Tipo'] == 'Despesa'].groupby('Categoria')['Valor'].sum().to_dict()
    
    return receitas_por_categoria, despesas_por_categoria

def calcular_evolucao_mensal(df, meses=6):
    """
    Calcula a evolução financeira dos últimos N meses.
    Retorna um DataFrame com receitas, despesas e saldo por mês.
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # Adicionar colunas de mês e ano
    df_copy = df.copy()
    df_copy['Mes_Ano'] = df_copy['Data'].dt.to_period('M')
    
    # Obter últimos N meses
    meses_disponiveis = sorted(df_copy['Mes_Ano'].unique(), reverse=True)[:meses]
    
    evolucao = []
    for mes in meses_disponiveis:
        df_mes = df_copy[df_copy['Mes_Ano'] == mes]
        somatorio = calcular_somatorio_geral(df_mes)
        evolucao.append({
            'Mes': str(mes),
            'Receitas': somatorio['receitas'],
            'Despesas': somatorio['despesas'],
            'Saldo': somatorio['saldo']
        })
    
    return pd.DataFrame(evolucao)

def comparar_meses(df, mes1, mes2):
    """
    Compara dois meses específicos.
    Retorna um dicionário com as métricas de cada mês.
    """
    if len(df) == 0:
        return {}
    
    df_copy = df.copy()
    df_copy['Mes_Ano'] = df_copy['Data'].dt.to_period('M')
    
    df_mes1 = df_copy[df_copy['Mes_Ano'] == mes1]
    df_mes2 = df_copy[df_copy['Mes_Ano'] == mes2]
    
    somatorio_mes1 = calcular_somatorio_geral(df_mes1)
    somatorio_mes2 = calcular_somatorio_geral(df_mes2)
    
    return {
        'mes1': {
            'periodo': str(mes1),
            'receitas': somatorio_mes1['receitas'],
            'despesas': somatorio_mes1['despesas'],
            'saldo': somatorio_mes1['saldo']
        },
        'mes2': {
            'periodo': str(mes2),
            'receitas': somatorio_mes2['receitas'],
            'despesas': somatorio_mes2['despesas'],
            'saldo': somatorio_mes2['saldo']
        },
        'diferenca': {
            'receitas': somatorio_mes2['receitas'] - somatorio_mes1['receitas'],
            'despesas': somatorio_mes2['despesas'] - somatorio_mes1['despesas'],
            'saldo': somatorio_mes2['saldo'] - somatorio_mes1['saldo']
        }
    }

def obter_top_categorias_mes(df, mes, tipo, top_n=5):
    """
    Obtém as top N categorias de um mês específico.
    """
    if len(df) == 0:
        return pd.Series()
    
    df_copy = df.copy()
    df_copy['Mes_Ano'] = df_copy['Data'].dt.to_period('M')
    
    df_mes = df_copy[df_copy['Mes_Ano'] == mes]
    df_tipo = df_mes[df_mes['Tipo'] == tipo]
    
    return df_tipo.groupby('Categoria')['Valor'].sum().sort_values(ascending=False).head(top_n)

def calcular_media_mensal(df, meses=6):
    """
    Calcula a média mensal dos últimos N meses.
    """
    evolucao = calcular_evolucao_mensal(df, meses)
    
    if len(evolucao) == 0:
        return {}
    
    return {
        'receitas_media': evolucao['Receitas'].mean(),
        'despesas_media': evolucao['Despesas'].mean(),
        'saldo_media': evolucao['Saldo'].mean()
    }

# Outras funções podem ser adicionadas depois (por exemplo, somatório por mês, categorias, etc.)

