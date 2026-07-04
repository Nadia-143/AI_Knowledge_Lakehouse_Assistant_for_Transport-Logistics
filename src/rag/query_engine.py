import pickle, requests, numpy as np, faiss
from sentence_transformers import SentenceTransformer
from src.common.config import GOLD, OPENROUTER_API_KEY, OPENROUTER_MODEL
INDEX_DIR=GOLD/'vector_index'
class RAGEngine:
    def __init__(self):
        self.chunks=pickle.load(open(INDEX_DIR/'chunks.pkl','rb')); self.bm25=pickle.load(open(INDEX_DIR/'bm25.pkl','rb')); self.embedding_config=pickle.load(open(INDEX_DIR/'embedding_config.pkl','rb')); self.faiss_index=faiss.read_index(str(INDEX_DIR/'faiss.index')); self.model=SentenceTransformer(self.embedding_config['model_name'])
    def hybrid_search(self, query, top_k=5):
        q_emb=self.model.encode([query],convert_to_numpy=True,normalize_embeddings=True).astype('float32'); dense_scores,dense_idx=self.faiss_index.search(q_emb,min(max(top_k*4,10),len(self.chunks))); dense_map={int(i):float(s) for i,s in zip(dense_idx.ravel(),dense_scores.ravel()) if i>=0}
        bm25_scores=np.array(self.bm25.get_scores(query.lower().split()),dtype='float32')
        if bm25_scores.max()>0: bm25_scores=bm25_scores/bm25_scores.max()
        candidates=set(dense_map.keys())|set(map(int,np.argsort(bm25_scores)[::-1][:min(max(top_k*4,10),len(self.chunks))])); terms=set(query.lower().split()); scored=[]
        for i in candidates:
            overlap=len(terms & set(self.chunks[i]['text'].lower().split()))/max(len(terms),1); final=0.55*dense_map.get(i,0.0)+0.35*float(bm25_scores[i])+0.10*overlap; scored.append((i,final))
        scored=sorted(scored,key=lambda x:x[1],reverse=True)[:top_k]; return [{**self.chunks[i],'score':float(score)} for i,score in scored]
    def generate_answer(self, query, contexts):
        context_text='\n\n'.join([f"[Source: {c['source']} | {c['chunk_id']}]\n{c['text']}" for c in contexts])
        prompt='You are an enterprise AI assistant for transport and logistics data. Answer only using the provided context. Always include source file names.\n\nQuestion:\n'+query+'\n\nContext:\n'+context_text
        if not OPENROUTER_API_KEY: return 'لم يتم ضبط مفتاح LLM. هذه أفضل المقاطع المسترجعة باستخدام real embeddings + FAISS + BM25:\n\n'+'\n\n'.join([f"- {c['source']} | score={c['score']:.3f}: {c['text'][:350]}..." for c in contexts])
        r=requests.post('https://openrouter.ai/api/v1/chat/completions',headers={'Authorization':f'Bearer {OPENROUTER_API_KEY}','Content-Type':'application/json'},json={'model':OPENROUTER_MODEL,'messages':[{'role':'user','content':prompt}],'temperature':0.2},timeout=60); r.raise_for_status(); return r.json()['choices'][0]['message']['content']
    def ask(self, query, top_k=5):
        contexts=self.hybrid_search(query,top_k=top_k); return {'answer':self.generate_answer(query,contexts),'sources':contexts,'retrieval_method':'FAISS dense embeddings + BM25 hybrid search + overlap reranking'}
