from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class SemanticParseRequest(BaseModel):
    """语义解析请求"""
    text: str
    model: Optional[str] = "llama3"

class ModelFeature(BaseModel):
    """3D模型特征"""
    type: str
    value: Any
    weight: Optional[float] = 1.0

class SemanticParseResponse(BaseModel):
    """语义解析响应"""
    intent: str
    keywords: List[str]
    model_features: List[ModelFeature]
    confidence: Optional[float] = None
    additional_info: Optional[Dict[str, Any]] = None
