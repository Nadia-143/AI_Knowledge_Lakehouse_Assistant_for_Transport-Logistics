import pickle, pandas as pd, faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from src.common.config import DOCUMENTS, REFERENCE, GOLD
INDEX_DIR=GOLD/'vector_index'; INDEX_DIR.mkdir(parents=True,exist_ok=True); EMBEDDING_MODEL='sentence-transformers/all-MiniLM-L6-v2'
def load_sources():
    docs=[]
    for path in DOCUMENTS.glob('*.*'): docs.append({'source':path.name,'text':path.read_text(encoding='utf-8')})
    for path in REFERENCE.glob('*.csv'): docs.append({'source':path.name,'text':pd.read_csv(path).to_markdown(index=False)})
    q=GOLD/'quality_metrics.csv'
    if q.exists(): docs.append({'source':'quality_metrics.csv','text':pd.read_csv(q).to_markdown(index=False)})
    return docs
def chunk_text(text, chunk_size=700, overlap=120):
    chunks=[]; start=0
    while start<len(text):
        end=start+chunk_size; chunks.append(text[start:end]); start=end-overlap
    return [c.strip() for c in chunks if c.strip()]
def build():
    chunks=[]
    for doc in load_sources():
        for i,chunk in enumerate(chunk_text(doc['text'])): chunks.append({'chunk_id':f"{doc['source']}::chunk_{i}",'source':doc['source'],'text':chunk})
    texts=[c['text'] for c in chunks]; model=SentenceTransformer(EMBEDDING_MODEL); embeddings=model.encode(texts,convert_to_numpy=True,normalize_embeddings=True).astype('float32')
    index=faiss.IndexFlatIP(embeddings.shape[1]); index.add(embeddings); bm25=BM25Okapi([t.lower().split() for t in texts])
    pickle.dump(chunks,open(INDEX_DIR/'chunks.pkl','wb')); pickle.dump(bm25,open(INDEX_DIR/'bm25.pkl','wb')); pickle.dump({'model_name':EMBEDDING_MODEL,'dimension':embeddings.shape[1]},open(INDEX_DIR/'embedding_config.pkl','wb')); faiss.write_index(index,str(INDEX_DIR/'faiss.index'))
    print(f'Built real embedding + FAISS RAG index with {len(chunks)} chunks at {INDEX_DIR}')
if __name__=='__main__': build()
