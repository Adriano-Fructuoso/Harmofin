# Dockerfile para deploy no Fly.io
FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements do backend
COPY backend/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/app/ ./app/
COPY backend/scripts/ ./scripts/

# Criar diretório para logs
RUN mkdir -p /app/logs

# Expor porta
EXPOSE 8001

# Comando para executar a aplicação
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"] 