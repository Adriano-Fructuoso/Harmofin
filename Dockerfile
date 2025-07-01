# Dockerfile otimizado para produção
FROM python:3.9-slim

WORKDIR /app

# Instalar apenas dependências essenciais do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar requirements primeiro para aproveitar cache do Docker
COPY backend/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/app/ ./app/
COPY backend/scripts/ ./scripts/

# Criar usuário não-root para segurança
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expor porta
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Comando para executar a aplicação
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"] 