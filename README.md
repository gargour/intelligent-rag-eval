.env Structure : 
GROK_API_KEY=
GROK_MODEL=llama-3.3-70b-versatile
GROK_BASE_URL=https://api.groq.com/openai/v1
LLM_PROVIDER=grok

OPENAI_API_KEY=
EMBEDDING_PROVIDER=sentence-transformers
EMBEDDING_MODEL=text-embedding-3-small

VECTORSTORE_PROVIDER=faiss
FAISS_INDEX_DIR=./data/faiss_index

DATABASE_URL=postgresql://raguser:ragpass@localhost:5432/ragdb

API_HOST=0.0.0.0
API_PORT=8000
API_SECRET_KEY=change-me
API_BASE_URL=http://localhost:8000
