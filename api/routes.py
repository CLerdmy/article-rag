from fastapi import APIRouter, Request, UploadFile, Depends, File
from .schemas import QueryRequest, QueryResponse
from service.rag_service import RAGService

router = APIRouter(tags=["rag"])


# DI
def get_rag(request: Request) -> RAGService:
    return request.app.state.rag


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    rag: RAGService = Depends(get_rag)
):
    result = rag.ingest(file)
    return {"message": result}


@router.post("/query", response_model=QueryResponse)
async def query(
    req: QueryRequest,
    rag: RAGService = Depends(get_rag)
):
    answer = rag.query(req.query)
    return QueryResponse(answer=answer)