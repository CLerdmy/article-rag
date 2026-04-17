from fastapi import FastAPI
from api.routes import router
from service.rag_service import RAGService

app = FastAPI(title="Article RAG API")

app.state.rag = RAGService()

app.include_router(router, prefix="/api")