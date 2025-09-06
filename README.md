
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

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd semantic-search-app

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"

# Frontend setup
cd ../frontend
npm install
