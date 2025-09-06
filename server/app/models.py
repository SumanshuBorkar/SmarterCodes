from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SearchRequest(BaseModel):
    url: str
    query: str

class ChunkResult(BaseModel):
    content: str
    score: float
    chunk_id: int
    token_count: Optional[int] = None
    character_count: Optional[int] = None
    has_code: Optional[bool] = False
    language: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[ChunkResult]
    total_chunks: int
    query: str
    url: str
    processing_time: Optional[float] = None