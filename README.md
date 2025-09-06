
# Semantic Search Application

A comprehensive single-page application (SPA) that enables users to input website URLs and search queries, returning the top 10 most relevant HTML content chunks using semantic search powered by vector embeddings.

## Features

- **Smart URL Indexing**: Process and store website content in Zilliz Cloud vector database
- **Semantic Search**: Advanced vector similarity search using sentence transformers
- **Code Intelligence**: Automatic code detection with syntax highlighting
- **HTML Cleaning**: Advanced content extraction and cleaning
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Modern UI**: React-based responsive frontend
- **Production Ready**: Scalable architecture with cloud deployment support

## Architecture

React Frontend → FastAPI Backend → Zilliz Cloud → Semantic Search Results


## 📋 Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support

### Frontend Requirements
- Node.js 14.0 or higher
- npm or yarn package manager

### Cloud Services
- Zilliz Cloud account (free tier available)

## Environment Configuration
- Create .env file in backend directory:
```bash
# Zilliz Cloud Configuration
ZILLIZ_URI=https://in03-03c9fdee0c3edc6.serverless.aws-eu-central-1.cloud.zilliz.com
ZILLIZ_TOKEN=f5aff2f44940b8e0e06b5026a4381761c8bb0b8614db9a5c5d8e657246d8e58de5971164572fcb93e3a158f24d557a22f3ffa304

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
COLLECTION_NAME=web_content_chunks

# Server Configuration
PORT=8000
LOG_LEVEL=info

```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/SumanshuBorkar/SmarterCodes.git

# Backend setup

cd server

#  Most stable in pyhton 3.11.9
brew install pyenv
pyenv install 3.11.9
pyenv local 3.11.9

#  Setup the virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt   # If any error arrises , install the dependencies in working_requirements.txt file. 
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend setup
cd ../frontend
npm install
npm run dev
