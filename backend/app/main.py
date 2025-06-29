"""
Aplicação principal para sistema de gestão de clientes
Usando FastAPI e SQLAlchemy com SQLite
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import clientes, atendimentos, procedimentos, materiais
from app.config import settings

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Instanciar aplicação FastAPI
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(clientes.router, prefix="/api/v1", tags=["clientes"])
app.include_router(atendimentos.router, prefix="/api/v1", tags=["atendimentos"])
app.include_router(procedimentos.router, prefix="/api/v1", tags=["procedimentos"])
app.include_router(materiais.router, prefix="/api/v1", tags=["materiais"])

@app.get("/")
async def root():
    """Endpoint raiz da aplicação"""
    return {
        "message": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "endpoints": {
            "clientes": "/api/v1/clientes",
            "atendimentos": "/api/v1/atendimentos", 
            "procedimentos": "/api/v1/procedimentos",
            "materiais": "/api/v1/materiais"
        }
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar se a aplicação está funcionando"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    ) 