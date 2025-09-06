import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ZILLIZ_URI = os.getenv(
        "ZILLIZ_URI"
    )
    ZILLIZ_TOKEN = os.getenv("ZILLIZ_TOKEN") 

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    MAX_TOKENS_PER_CHUNK = 500

    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "web_content_chunks")


settings = Settings()
