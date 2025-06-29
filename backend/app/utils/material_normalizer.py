"""
Utilitários para normalização e agrupamento de materiais
"""

import re
import unicodedata
from typing import List, Dict, Tuple
from difflib import SequenceMatcher

def normalizar_nome(nome: str) -> str:
    """
    Normaliza o nome do material para comparação
    - Remove acentos
    - Converte para minúsculas
    - Remove espaços extras
    - Remove caracteres especiais
    """
    if not nome:
        return ""
    
    # Converter para minúsculas
    nome = nome.lower().strip()
    
    # Remover acentos
    nome = unicodedata.normalize('NFD', nome)
    nome = ''.join(c for c in nome if not unicodedata.combining(c))
    
    # Remover caracteres especiais, mantendo apenas letras, números e espaços
    nome = re.sub(r'[^a-z0-9\s]', '', nome)
    
    # Remover espaços extras
    nome = re.sub(r'\s+', ' ', nome).strip()
    
    return nome

def calcular_similaridade(nome1: str, nome2: str) -> float:
    """
    Calcula a similaridade entre dois nomes (0.0 a 1.0)
    """
    if not nome1 or not nome2:
        return 0.0
    
    nome1_norm = normalizar_nome(nome1)
    nome2_norm = normalizar_nome(nome2)
    
    if nome1_norm == nome2_norm:
        return 1.0
    
    return SequenceMatcher(None, nome1_norm, nome2_norm).ratio()

def encontrar_materiais_similares(nome: str, materiais: List[Dict], threshold: float = 0.8) -> List[Dict]:
    """
    Encontra materiais similares ao nome fornecido
    """
    if not nome:
        return []
    
    similares = []
    
    for material in materiais:
        similaridade = calcular_similaridade(nome, material['nome'])
        if similaridade >= threshold:
            similares.append({
                **material,
                'similaridade': similaridade
            })
    
    # Ordenar por similaridade (maior primeiro)
    similares.sort(key=lambda x: x['similaridade'], reverse=True)
    
    return similares

def agrupar_materiais_similares(materiais: List[Dict], threshold: float = 0.8) -> List[Dict]:
    """
    Agrupa materiais similares em grupos
    """
    if not materiais:
        return []
    
    grupos = []
    materiais_processados = set()
    
    for i, material in enumerate(materiais):
        if i in materiais_processados:
            continue
        
        grupo = [material]
        materiais_processados.add(i)
        
        # Procurar materiais similares
        for j, outro_material in enumerate(materiais[i+1:], i+1):
            if j in materiais_processados:
                continue
            
            similaridade = calcular_similaridade(material['nome'], outro_material['nome'])
            if similaridade >= threshold:
                grupo.append(outro_material)
                materiais_processados.add(j)
        
        # Criar representante do grupo (o material com mais estoque ou o primeiro)
        if len(grupo) > 1:
            representante = max(grupo, key=lambda x: x.get('quantidade_disponivel', 0))
            representante['materiais_similares'] = grupo
            representante['total_estoque'] = sum(m.get('quantidade_disponivel', 0) for m in grupo)
            grupos.append(representante)
        else:
            grupos.append(material)
    
    return grupos

def sugerir_nome_padrao(materiais: List[Dict]) -> str:
    """
    Sugere um nome padrão para um grupo de materiais similares
    """
    if not materiais:
        return ""
    
    if len(materiais) == 1:
        return materiais[0]['nome']
    
    # Encontrar o nome mais comum ou o mais completo
    nomes = [m['nome'] for m in materiais]
    
    # Preferir nomes com acentos e formatação correta
    for nome in nomes:
        if any(c in nome for c in 'áéíóúâêîôûãõç'):
            return nome
    
    # Se não encontrar, usar o primeiro nome
    return nomes[0] 