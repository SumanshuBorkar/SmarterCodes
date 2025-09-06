from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
from app.config import settings
import logging
import time

logger = logging.getLogger(__name__)


class ZillizClient:
    def __init__(self, retries=3, delay=2):
        self.collection_name = settings.COLLECTION_NAME
        self.dimension = 384 
        self.retries = retries
        self.delay = delay
        self.connected = False
        self.collection = None
        self.connect_with_retry()
        if self.connected:
            self.create_collection_if_not_exists()
            self.load_collection()

    def connect_with_retry(self):
        for attempt in range(self.retries):
            try:
                self.connect()
                self.connected = True
                return
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < self.retries - 1:
                    time.sleep(self.delay)
                else:
                    logger.error(f"All connection attempts failed")
                    self.connected = False

    def connect(self):
        try:
            try:
                connections.disconnect("default")
            except:
                pass

            connections.connect(
                alias="default", uri=settings.ZILLIZ_URI, token=settings.ZILLIZ_TOKEN
            )
            logger.info("Successfully connected to Zilliz Cloud")
        except Exception as e:
            logger.error(f"Failed to connect to Zilliz Cloud: {e}")
            raise

    def create_collection_if_not_exists(self):
        try:
            if utility.has_collection(self.collection_name):
                self.collection = Collection(self.collection_name)
                logger.info(f"Collection {self.collection_name} already exists")
                return

            fields = [
                FieldSchema(
                    name="id", dtype=DataType.INT64, is_primary=True, auto_id=True
                ),
                FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=500),
                FieldSchema(name="chunk_id", dtype=DataType.INT64),
                FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=10000),
                FieldSchema(
                    name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dimension
                ),
            ]

            schema = CollectionSchema(fields, "Web content chunks with embeddings")
            self.collection = Collection(self.collection_name, schema)

            index_params = {
                "index_type": "AUTOINDEX",
                "metric_type": "L2",
                "params": {},
            }

            self.collection.create_index("embedding", index_params)
            logger.info(f"Created collection {self.collection_name} with index")

        except Exception as e:
            logger.error(f"Error creating collection: {e}")

    def load_collection(self):
        """Load the collection into memory"""
        try:
            if self.collection:
                self.collection.load()
                logger.info(f"Collection {self.collection_name} loaded successfully")
        except Exception as e:
            logger.error(f"Error loading collection: {e}")

    def insert_chunks(self, url: str, chunks: list, embeddings: list):
        try:
            if not self.connected or not self.collection:
                raise Exception(
                    "Not connected to Zilliz Cloud or collection not available"
                )

            self.load_collection()

            data = [
                [url] * len(chunks),
                list(range(len(chunks))), 
                chunks, 
                embeddings, 
            ]

            mr = self.collection.insert(data)
            self.collection.flush()
            logger.info(f"Inserted {len(chunks)} chunks for URL: {url}")
            return mr
        except Exception as e:
            logger.error(f"Error inserting chunks: {e}")
            raise

    def search_similar_chunks(self, query_embedding: list, limit: int = 10):
        try:
            if not self.connected or not self.collection:
                raise Exception(
                    "Not connected to Zilliz Cloud or collection not available"
                )

            self.load_collection()

            search_params = {"metric_type": "L2", "params": {"level": 2}}

            results = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=limit,
                output_fields=["content", "chunk_id", "url"],
            )

            return results
        except Exception as e:
            logger.error(f"Error searching chunks: {e}")
            raise

    def count_chunks_for_url(self, url: str):
        try:
            if not self.connected or not self.collection:
                return 0

            self.load_collection()

            query = f'url == "{url}"'
            result = self.collection.query(expr=query, output_fields=["count(*)"])
            return result[0]["count(*)"] if result else 0
        except Exception as e:
            logger.error(f"Error counting chunks: {e}")
            return 0


try:
    zilliz_client = ZillizClient()
    logger.info("Zilliz client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Zilliz client: {e}")
    zilliz_client = None
