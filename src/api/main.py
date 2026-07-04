from fastapi import FastAPI
from pydantic import BaseModel
from src.rag.query_engine import RAGEngine
app=FastAPI(title='AI Knowledge Lakehouse Assistant API')
class AskRequest(BaseModel): question: str; top_k: int=5
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/ask')
def ask(req: AskRequest): return RAGEngine().ask(req.question,top_k=req.top_k)
