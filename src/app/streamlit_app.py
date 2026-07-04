import streamlit as st, pandas as pd
from src.common.config import RAW, REFERENCE, GOLD
from src.rag.query_engine import RAGEngine
st.set_page_config(page_title='AI Knowledge Lakehouse Assistant',layout='wide'); st.title('AI Knowledge Lakehouse Assistant'); st.caption('NotebookLM-inspired assistant with FAISS embeddings + BM25 hybrid retrieval')
tab1,tab2,tab3=st.tabs(['Data Overview','Ask Assistant','Quality Metrics'])
with tab1:
    st.subheader('Available Sources')
    for p in RAW.glob('*.csv'): st.write(f'- Raw: {p.name}')
    for p in REFERENCE.glob('*.csv'): st.write(f'- Reference: {p.name}')
with tab2:
    query=st.text_input('Question','ما هو SLA الخاص بتحديث بيانات الشحنات؟')
    if st.button('Ask'):
        try:
            result=RAGEngine().ask(query); st.markdown('### Answer'); st.write(result['answer']); st.info(result['retrieval_method']); st.markdown('### Sources')
            for src in result['sources']: st.write(f"**{src['source']}** — score: {src['score']:.3f}"); st.code(src['text'][:700])
        except Exception as e: st.error(f'Run `python src/rag/build_index.py` first. Details: {e}')
with tab3:
    q=GOLD/'quality_metrics.csv'; st.dataframe(pd.read_csv(q)) if q.exists() else st.info('Run quality gate first.')
