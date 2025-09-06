import os
from dotenv import load_dotenv
from pymilvus import connections, utility

# Load environment variables
load_dotenv()

# Get credentials
ZILLIZ_URI = os.getenv("ZILLIZ_URI")
ZILLIZ_TOKEN = os.getenv("ZILLIZ_TOKEN")

print(f"Connecting to: {ZILLIZ_URI}")

try:
    # Connect to Zilliz Cloud
    connections.connect(
        alias="default",
        uri=ZILLIZ_URI,
        token=ZILLIZ_TOKEN
    )
    
    print("Successfully connected to Zilliz Cloud!")
    
    # List collections to verify connection
    collections = utility.list_collections()
    print(f"Available collections: {collections}")
    
except Exception as e:
    print(f"Connection failed: {e}")