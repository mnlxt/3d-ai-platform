from fastapi import APIRouter, HTTPException
from app.schemas.ai import SemanticParseRequest, SemanticParseResponse
from app.utils.ai_request import ollama_semantic_parse

router = APIRouter()

@router.post("/semantic-parse", response_model=SemanticParseResponse)
async def semantic_parse(request: SemanticParseRequest):
    """语义解析接口"""
    result = await ollama_semantic_parse(request.text)
    if not result:
        raise HTTPException(status_code=500, detail="Semantic parse failed")
    return SemanticParseResponse(**result)
