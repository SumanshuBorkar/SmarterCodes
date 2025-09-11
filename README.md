
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



## 🫆 Environment Configuration
- Create .env file in backend directory:
- Sign up at Zilliz Cloud
- Create a new serverless cluster
- Obtain your cluster URI and API token
- Update the .env file with your credentials
- (I have provided my credentials for now , but I will remove them soon )

```bash
# Zilliz Cloud Configuration
ZILLIZ_URI=++++
ZILLIZ_TOKEN=+++++

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

```
## How does this works ?

- Below is the sequence diagram explaining the flow.

<p align="center">
  <img src="https://uml.planttext.com/plantuml/svg/dLLXRzem4FtkNt7A9ofHLkrZ9APkxQgXTIegJ9fMLP7hN8c5usIsixQh-jztYHDmW9QA3q0uxZs_UtaNJgtZnbMvOboumi1FYmQuXQY-Y5X9FqeXIwuTN9X2EzHfy_CrKl-gr6_ymiMowxlWrdsUJhfQl_7R_CVbr1G2hItygNK5LgL-zs-fbFntfYJIbxhP5y1N8fPon--unLLZKQNzFYf4Z8t7CD4fFagzw8w2yPYnPlJZJwkXOlXAdsJ9zILm6aSeAPOGDTYw6B6L8uHg1unXUZMRmmVPT3rNHiLWdQ6pNcg7vL_kiEjbh7EAy3qlOYZzPK840teThS6zHiRw7cuJtQCJMPAvN2MYKUiytpwSKCXrWnlKR_i1jbJI9LAx8X5PfPTsuF3HxSSjKAEXmHBCxp1DoIaxy0HRsD1ctpA4DOgb-9f9WSzXYcAGccwwwmIJCSCTn87v8Phr0XbGKynYcD4sOKlMn2SG6WRqU4lJh1ArxWtwSFP9ereM6WpQIhbmyfx2zU2zN7yyEO6hx_2Sqp5yWN4RQapXLwiuUWavkxokyqvqzRgGsAnu0EiLGylNhDWCkH7PknRiJuNcALmnZtrplwod3nTiw8aEsxTTARnf-6vVtRqtqjaWrro7HDDFc5YPIyLD5z4DuiEYwRsx9z4jUtlNzmHpNfIGStgSr4_E3SHsI5lzFg7s7H4Di2ID3ggnPK5P7_IvZlR4kcsBuMOq6jtkJFAkA9zBUeJnftQdB3n8bu4eKeHCBZ95BrVVobD2qV_bVm00" alt="Logo" width="100%"/>
</p>

- Below is the Activity Diagram explaining the interaction of different components and activities 

<p align="center">
  <img src="https://uml.planttext.com/plantuml/svg/bLDDRzim3BtxLn0zEK0nP8TTaiEwxXleW25TBxknCXCBaIbFfBjum_xxA3KgakuqmBOaw_6Hxr6w4iMaqn2QCccQrPrG0dIEH4W0np5uX-eZhvl6Rw4j-p-HLK0ZUExe07URczSBq9uOsfbaqG2ithCQq7RMUVNMMFPmyRd2B_9VUqPBwZCxNAFR4tTVKyofFU_Wj-rRw0TIryEdRrzkm4KZPOLjYaEbBkI4_8Xe4mtnWK1SygFA9OZEWMmqaXUB8_xMDEaJcMVJuVg9zmBjW0TujLoQD2j6Qi17Oage13JSKzTPSGBRc83GAYkXbLbZeag6t9q6U8RlFWJ_AsF_FCfVlVCo1fn1fk8u3FR17QqR2aBGSho4wSnm8KokFtUuPFenKPfFlRujoFym-b-LHUGJSTPNECjlyOCFcAhOCtM6t23l8P5CmUg-dsqQw07PKTqddHAReX5UBc50wp79YJFvg6sEuRbJQ0bSxEZvEJEgDtP6pS7PG0Ve_QuFzggLd-cgZqTizHi5R3HEfOCM77T--wmf9jCAK-gg46jBWTbbYMDpPGkxENy1" alt="Logo" width="100%"/>
</p>
