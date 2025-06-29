#!/usr/bin/env python3
"""
Script para testar se o backend está funcionando corretamente
"""

import requests
import sys

def test_backend():
    """Testa se o backend está funcionando"""
    try:
        # Testar endpoint de health
        response = requests.get('http://localhost:8001/health', timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        
        # Testar endpoint raiz
        response = requests.get('http://localhost:8001/', timeout=5)
        print(f"✅ Endpoint raiz: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        
        # Testar endpoint de clientes
        response = requests.get('http://localhost:8001/api/v1/clientes', timeout=5)
        print(f"✅ Endpoint clientes: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        
        print("\n🎉 Backend está funcionando corretamente!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao backend na porta 8001")
        print("   Verifique se o backend está rodando com: uvicorn app.main:app --reload --host 0.0.0.0 --port 8001")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    test_backend() 