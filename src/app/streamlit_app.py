import streamlit as st
from pathlib import Path
import pandas as pd

# =========================================================
# Page Configuration
# =========================================================
st.set_page_config(
   page_title="AI Knowledge Lakehouse Assistant",
   page_icon="🚚",
   layout="wide"
)

# =========================================================
# Theme Colors
# عدلي الألوان من هنا فقط إذا تبين تغيرينها
# =========================================================
PRIMARY = "#12355B"      # Dark navy
SECONDARY = "#1F6F8B"    # Teal blue
BACKGROUND = "#F7F9FC"   # Light background
CARD = "#FFFFFF"
ACCENT = "#D4AF37"       # Gold accent
TEXT = "#1F2933"
MUTED = "#667085"

# =========================================================
# Custom Styling
# =========================================================
st.markdown(
   f"""
<style>
       .stApp {{
           background-color: {BACKGROUND};
       }}
       .hero {{
           background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
           padding: 38px 30px;
           border-radius: 24px;
           color: white;
           text-align: center;
           margin-bottom: 28px;
           box-shadow: 0px 8px 24px rgba(18,53,91,0.22);
       }}
       .hero h1 {{
           font-size: 42px;
           font-weight: 800;
           margin-bottom: 10px;
       }}
       .hero p {{
           font-size: 18px;
           margin: 0;
           opacity: 0.95;
       }}
       .center-image {{
           display: flex;
           justify-content: center;
           align-items: center;
           margin: 12px 0 28px 0;
       }}
       .section-title {{
           color: {PRIMARY};
           font-size: 25px;
           font-weight: 800;
           margin-top: 22px;
           margin-bottom: 14px;
           border-left: 6px solid {ACCENT};
           padding-left: 12px;
       }}
       .card {{
           background-color: {CARD};
           padding: 24px;
           border-radius: 18px;
           box-shadow: 0px 5px 18px rgba(0,0,0,0.07);
           border: 1px solid #edf0f5;
           margin-bottom: 18px;
           color: {TEXT};
       }}
       .metric-card {{
           background-color: {CARD};
           padding: 22px 16px;
           border-radius: 18px;
           text-align: center;
           box-shadow: 0px 5px 16px rgba(0,0,0,0.07);
           border-top: 5px solid {SECONDARY};
           min-height: 120px;
       }}
       .metric-card h3 {{
           color: {PRIMARY};
           margin-bottom: 8px;
           font-size: 24px;
       }}
       .metric-card p {{
           color: {MUTED};
           font-size: 14px;
           margin: 0;
       }}
       .team-box {{
           background-color: {CARD};
           padding: 24px;
           border-radius: 18px;
           box-shadow: 0px 5px 18px rgba(0,0,0,0.07);
           border: 1px solid #edf0f5;
       }}
       .team-member {{
           background: linear-gradient(90deg, #eef5fb, #ffffff);
           padding: 13px 16px;
           border-radius: 14px;
           margin: 9px 0;
           font-weight: 700;
           color: {PRIMARY};
           border-left: 5px solid {ACCENT};
       }}
       .answer-box {{
           background-color: {CARD};
           padding: 22px;
           border-radius: 18px;
           border-left: 6px solid {SECONDARY};
           box-shadow: 0px 5px 16px rgba(0,0,0,0.07);
           margin-top: 14px;
           color: {TEXT};
       }}
       .small-note {{
           color: {MUTED};
           font-size: 14px;
           text-align: center;
       }}
       div[data-testid="stAlert"] {{
           border-radius: 14px;
       }}
</style>
   """,
   unsafe_allow_html=True
)

# =========================================================
# Helper Functions
# =========================================================
def safe_read_csv(path: str):
   file_path = Path(path)
   if file_path.exists():
       try:
           return pd.read_csv(file_path)
       except Exception:
           return None
   return None

def find_project_image():
   possible_paths = [
       "assets/project_cover.png",
       "assets/project_cover.jpg",
       "assets/architecture.png",
       "assets/architecture.jpg",
       "outputs/screenshots/architecture.png",
       "outputs/screenshots/project_cover.png",
   ]
   for path in possible_paths:
       if Path(path).exists():
           return path
   return None

def generate_local_answer(question: str) -> str:
   if not question.strip():
       return "Please enter a question about the transport and logistics data platform."
   try:
       from src.rag import query_engine
       possible_functions = [
           "answer_question",
           "ask",
           "query",
           "run_query",
           "generate_answer",
       ]
       for func_name in possible_functions:
           if hasattr(query_engine, func_name):
               func = getattr(query_engine, func_name)
               response = func(question)
               return str(response)
   except Exception:
       pass
   return f"""
This assistant is designed to answer questions about the AI Knowledge Lakehouse for Transport & Logistics.
Your question was:
**{question}**
The platform includes synthetic logistics data generation, lakehouse processing, data quality validation, RAG indexing, and an AI assistant interface.
"""

# =========================================================
# Header
# =========================================================
st.markdown(
   """
<div class="hero">
<h1>🚚 AI Knowledge Lakehouse Assistant</h1>
<p>Integrated AI Data Platform for Transport & Logistics</p>
</div>
   """,
   unsafe_allow_html=True
)

# =========================================================
# Centered Project Image
# =========================================================
image_path = find_project_image()
if image_path:
   left, center, right = st.columns([1, 2, 1])
   with center:
       st.image(
           image_path,
           caption="Project Architecture / Cover",
           use_container_width=True
       )
else:
   st.markdown(
       """
<div class="card" style="text-align:center;">
<h3>📌 Project Image</h3>
<p class="small-note">
               Add your image here:<br><br>
<b>assets/project_cover.png</b><br>
               or<br>
<b>outputs/screenshots/architecture.png</b>
</p>
</div>
       """,
       unsafe_allow_html=True
   )

# =========================================================
# Project Overview
# =========================================================
st.markdown('<div class="section-title">Project Overview</div>', unsafe_allow_html=True)
st.markdown(
   """
<div class="card">
<p>
           This project builds an integrated AI data platform for the transport and logistics sector.
           It combines synthetic data generation, lakehouse architecture, data quality validation,
           RAG-based retrieval, and an interactive AI assistant interface.
</p>
<p>
           The platform simulates an enterprise-ready environment where logistics data can be ingested,
           processed, validated, indexed, and queried through an intelligent assistant.
</p>
</div>
   """,
   unsafe_allow_html=True
)

# =========================================================
# Platform Components
# =========================================================
st.markdown('<div class="section-title">Platform Components</div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
   st.markdown(
       """
<div class="metric-card">
<h3>Bronze</h3>
<p>Raw Data Layer</p>
</div>
       """,
       unsafe_allow_html=True
   )
with m2:
   st.markdown(
       """
<div class="metric-card">
<h3>Silver</h3>
<p>Cleaned Data Layer</p>
</div>
       """,
       unsafe_allow_html=True
   )
with m3:
   st.markdown(
       """
<div class="metric-card">
<h3>Gold</h3>
<p>Analytics Layer</p>
</div>
       """,
       unsafe_allow_html=True
   )
with m4:
   st.markdown(
       """
<div class="metric-card">
<h3>RAG</h3>
<p>AI Retrieval Layer</p>
</div>
       """,
       unsafe_allow_html=True
   )

# =========================================================
# Team Members
# =========================================================
st.markdown('<div class="section-title">Team Members</div>', unsafe_allow_html=True)
st.markdown(
   """
<div class="team-box">
<div class="team-member">Nadia Alghamdi</div>
<div class="team-member">Name 2</div>
<div class="team-member">Name 3</div>
<div class="team-member">Name 4</div>
</div>
   """,
   unsafe_allow_html=True
)

# =========================================================
# Data Preview
# =========================================================
st.markdown('<div class="section-title">Data Preview</div>', unsafe_allow_html=True)
data_files = [
   "data/raw/shipments.csv",
   "data/processed/cleaned_logistics_data.csv",
   "data/gold/gold_logistics_kpis.csv",
   "data/catalog/indicator_catalog.csv",
   "data/catalog/sla_catalog.csv",
]
selected_df = None
selected_file = None
for file in data_files:
   df = safe_read_csv(file)
   if df is not None:
       selected_df = df
       selected_file = file
       break
if selected_df is not None:
   st.caption(f"Preview from: `{selected_file}`")
   st.dataframe(selected_df.head(10), use_container_width=True)
else:
st.info("Data preview will appear here after running the data generation and lakehouse pipeline.")

# =========================================================
# AI Assistant
# =========================================================
st.markdown('<div class="section-title">AI Logistics Assistant</div>', unsafe_allow_html=True)
st.markdown(
   """
<div class="card">
<p>
           Ask a question about transport, logistics, SLA performance, data quality,
           lakehouse layers, or logistics indicators.
</p>
</div>
   """,
   unsafe_allow_html=True
)
question = st.text_input(
   "Enter your question",
   placeholder="Example: What are the main logistics KPIs in this platform?"
)
if st.button("Ask Assistant"):
   answer = generate_local_answer(question)
   st.markdown(
       f"""
<div class="answer-box">
<h4>Assistant Response</h4>
<p>{answer}</p>
</div>
       """,
       unsafe_allow_html=True
   )

# =========================================================
# Execution Status
# =========================================================
st.markdown('<div class="section-title">Execution Status</div>', unsafe_allow_html=True)
st.success("Application interface loaded successfully.")
st.info("Execution flow: tests → data generation → lakehouse pipeline → quality checks → RAG index → Streamlit app.")

# =========================================================
# Footer
# =========================================================
st.markdown(
   """
<br>
<div class="small-note">
       AI Knowledge Lakehouse Assistant for Transport & Logistics — Final Project Demo
</div>
   """,
   unsafe_allow_html=True
)
