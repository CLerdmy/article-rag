from fastapi import FastAPI
from api.routes import router
from config.config_loader import load_config
from service.rag_service import RAGService

app = FastAPI(title="Article RAG API")

config = load_config()

app.state.rag = RAGService(config=config)

app.include_router(router, prefix="/api")