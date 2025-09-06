from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import SearchRequest, SearchResponse, ChunkResult
from app.utils import html_processor
from app.zilliz_client import zilliz_client
import logging
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Semantic Search Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def estimate_token_count(text: str) -> int:
    """Estimate token count based on word count"""
    words = text.split()
    return len(words)


def detect_code_content(text: str) -> bool:
    """Detect if text contains code"""
    code_indicators = [
        r"function\s+\w+\s*\(",
        r"class\s+\w+",
        r"import\s+\w+",
        r"from\s+\w+\s+import",
        r"def\s+\w+\s*\(",
        r"const\s+\w+\s*=",
        r"let\s+\w+\s*=",
        r"var\s+\w+\s*=",
        r"<\?php",
        r"<\/?[a-z][a-z0-9]*[^>]*>",
        r"{\s*[\w\s]+\s*}",
        r"\[\s*[\w\s]+\s*\]",
        r"&&|\|\||===|!==|=>|->",
    ]

    for pattern in code_indicators:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    special_chars = len(re.findall(r"[{}();<>=\[\]\+\-\*\/&|]", text))
    total_chars = len(text)

    if total_chars > 0 and special_chars / total_chars > 0.05:
        return True

    return False


def detect_code_language(text: str) -> str:
    """Try to detect programming language"""
    language_patterns = {
        "javascript": [r"function\s*\w*\s*\(", r"const\s+\w+\s*=", r"let\s+\w+\s*="],
        "python": [r"def\s+\w+\s*\(", r"import\s+\w+", r"from\s+\w+\s+import"],
        "html": [r"<\/?[a-z][a-z0-9]*[^>]*>", r"&[a-z]+;"],
        "css": [r"[.#][\w-]+\s*{", r"@media", r"@keyframes"],
        "php": [r"<\?php", r"\$\w+\s*="],
        "java": [r"public\s+class", r"System\.out\.print"],
        "sql": [r"SELECT\s+.+FROM", r"INSERT\s+INTO", r"UPDATE\s+\w+\s+SET"],
    }

    for language, patterns in language_patterns.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return language

    return "unknown"


@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")
    if zilliz_client and zilliz_client.connected:
        logger.info("Connected to Zilliz Cloud")
    else:
        logger.warning("Not connected to Zilliz Cloud")


@app.post("/search", response_model=SearchResponse)
async def search_content(request: SearchRequest):
    try:
        start_time = time.time()

        if zilliz_client is None or not zilliz_client.connected:
            raise HTTPException(status_code=500, detail="Vector database not available")

        logger.info(
            f"Processing search request for URL: {request.url}, Query: {request.query}"
        )

        query_embedding = html_processor.generate_embeddings([request.query])[0]

        search_results = zilliz_client.search_similar_chunks(query_embedding)

        results = []
        for hits in search_results:
            for hit in hits:
                content = hit.entity.get("content")

                has_code = detect_code_content(content)
                language = detect_code_language(content) if has_code else None

                result = ChunkResult(
                    content=content,
                    score=hit.distance,
                    chunk_id=hit.entity.get("chunk_id"),
                    token_count=estimate_token_count(content),
                    character_count=len(content),
                    has_code=has_code,
                    language=language,
                )
                results.append(result)

        total_chunks = zilliz_client.count_chunks_for_url(request.url)

        processing_time = time.time() - start_time

        return SearchResponse(
            results=results[:10],
            total_chunks=total_chunks,
            query=request.query,
            url=request.url,
            processing_time=processing_time,
        )

    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index")
async def index_url(request: SearchRequest):
    try:
        if zilliz_client is None or not zilliz_client.connected:
            raise HTTPException(status_code=500, detail="Vector database not available")

        logger.info(f"Indexing URL: {request.url}")

        chunks, embeddings = html_processor.process_url(request.url)

        zilliz_client.insert_chunks(request.url, chunks, embeddings)

        return {
            "message": f"Successfully indexed {len(chunks)} chunks from {request.url}"
        }

    except Exception as e:
        logger.error(f"Error indexing URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database_connected": zilliz_client is not None and zilliz_client.connected,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
