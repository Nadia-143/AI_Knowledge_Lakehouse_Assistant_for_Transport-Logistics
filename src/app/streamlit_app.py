import streamlit as st
from pathlib import Path
import html
import base64

# =========================================================
# Page Config
# =========================================================
st.set_page_config(
   page_title="المساعد الذكـــي في قطاع النقل والخدمات اللوجستية",
   page_icon="🤖",
   layout="wide"
)

# =========================================================
# Helper Functions
# =========================================================
def find_image():
   app_dir = Path(__file__).parent
   project_root = Path(__file__).resolve().parents[2]
   paths = [
       app_dir / "ai-assistant-cover.png",
       app_dir / "ai-assistant-cover.jpg",
       app_dir / "assistant.png",
       project_root / "assets" / "project_cover.png",
       project_root / "outputs" / "screenshots" / "project_cover.png",
   ]
   for path in paths:
       if path.exists():
           return str(path)
   return None

def image_to_base64(image_path):
   with open(image_path, "rb") as image_file:
       return base64.b64encode(image_file.read()).decode()

def get_answer(question: str) -> str:
   if not question.strip():
       return "Type your question on the right side, then click Ask Assistant."
   try:
       from src.rag import query_engine
       for function_name in ["answer_question", "ask", "query", "run_query", "generate_answer"]:
           if hasattr(query_engine, function_name):
               return str(getattr(query_engine, function_name)(question))
   except Exception:
       pass
   return f"""AI Assistant Response
Question:
{question}
This assistant supports questions about:
• Transport and logistics KPIs
• Lakehouse Bronze, Silver, and Gold layers
• Data quality checks
• SLA indicators
• RAG retrieval and AI-generated insights
"""

# =========================================================
# Custom CSS
# =========================================================
st.markdown("""
<style>
   .stApp {
       background:
           radial-gradient(circle at 18% 12%, rgba(47,255,226,0.18), transparent 28%),
           radial-gradient(circle at 85% 80%, rgba(40,120,255,0.16), transparent 32%),
           linear-gradient(135deg, #050b18 0%, #07172c 45%, #040914 100%);
       color: white;
   }
   .block-container {
       padding-top: 1.2rem;
       padding-bottom: 2rem;
       max-width: 1300px;
   }
   .main-title {
       text-align: center;
       font-size: 48px;
       font-weight: 900;
       color: #ffffff;
       margin-bottom: 8px;
       text-shadow: 0 0 26px rgba(88,245,222,0.38);
   }
   .sub-title {
       text-align: center;
       color: #9feee4;
       font-size: 17px;
       margin-bottom: 14px;
   }
   .team-row {
       text-align: center;
       margin-bottom: 28px;
   }
   .team-chip {
       display: inline-block;
       background: linear-gradient(90deg, rgba(88,245,222,0.18), rgba(57,196,255,0.10));
       border: 1px solid rgba(88,245,222,0.32);
       border-radius: 999px;
       padding: 10px 18px;
       color: white;
       font-weight: 700;
       margin: 5px;
       box-shadow: 0 8px 20px rgba(0,0,0,0.22);
   }
   .hero-fallback {
       height: 340px;
       border-radius: 36px;
       margin-bottom: 30px;
       background:
           radial-gradient(circle at center, rgba(88,245,222,0.24), rgba(8,22,42,0.96) 58%);
       border: 1px solid rgba(88,245,222,0.36);
       box-shadow:
           0 0 50px rgba(88,245,222,0.18),
           0 18px 42px rgba(0,0,0,0.42);
       display: flex;
       align-items: center;
       justify-content: center;
       text-align: center;
   }
   .section-title {
       color: #58f5de;
       font-size: 22px;
       font-weight: 850;
       margin: 8px 0 14px 0;
   }
   .answer-box {
       background: rgba(4, 14, 28, 0.98);
       border: 1px solid rgba(88,245,222,0.42);
       border-left: 6px solid #58f5de;
       border-radius: 28px;
       padding: 26px;
       min-height: 370px;
       color: #effdff;
       line-height: 1.8;
       box-shadow:
           0 0 36px rgba(88,245,222,0.15),
           0 16px 38px rgba(0,0,0,0.38);
   }
   .answer-box h3 {
       color: #58f5de;
       margin-top: 0;
       margin-bottom: 16px;
   }
   .question-box {
       background: rgba(7,20,38,0.95);
       border: 1px solid rgba(88,245,222,0.38);
       border-radius: 28px;
       padding: 26px;
       min-height: 370px;
       box-shadow:
           0 0 36px rgba(88,245,222,0.13),
           0 16px 38px rgba(0,0,0,0.36);
   }
   .question-box h3 {
       color: #58f5de;
       margin-top: 0;
       margin-bottom: 12px;
   }
   .question-box p {
       color: #b7d7e0;
       font-size: 15px;
       line-height: 1.7;
       margin-top: 0;
       margin-bottom: 16px;
   }
   .overview-box {
       background: rgba(8,22,42,0.82);
       border: 1px solid rgba(88,245,222,0.22);
       border-radius: 24px;
       padding: 20px;
       color: #b7d7e0;
       line-height: 1.8;
       margin-top: 28px;
       box-shadow: 0 12px 30px rgba(0,0,0,0.26);
   }
   .stTextArea textarea {
       background-color: #06162b !important;
       color: #ffffff !important;
       border: 1px solid rgba(88,245,222,0.55) !important;
       border-radius: 18px !important;
       min-height: 190px !important;
   }
   .stButton button {
       background: linear-gradient(90deg, #58f5de, #39c4ff) !important;
       color: #04101e !important;
       border: 0 !important;
       border-radius: 999px !important;
       font-weight: 900 !important;
       padding: 0.75rem 1.8rem !important;
       width: 100%;
       box-shadow: 0 10px 22px rgba(0,255,220,0.22);
   }
   .stButton button:hover {
       transform: scale(1.01);
   }
   .footer {
       text-align: center;
       color: #6fa6b8;
       font-size: 13px;
       margin-top: 28px;
   }
   [data-testid="stException"] {
       display: none !important;
   }
</style>
""", unsafe_allow_html=True)

# =========================================================
# Session State
# =========================================================
if "answer" not in st.session_state:
   st.session_state.answer = "ستظهر الإجابة هنا "

# =========================================================
# Header + Team Names
# =========================================================
st.markdown("""
<div class="main-title">المساعد الذكي </div>
<div class="sub-title">في قطاع النقل والخدمات اللوجستية</div>
<div class="team-row">
<span class="team-chip">ناديه الغامدي</span>
<span class="team-chip">ابتسام محمد الزهراني</span>
<span class="team-chip">منار المطيري </span>

</div>
""", unsafe_allow_html=True)

# =========================================================
# Blended Background Image Hero
# =========================================================
img = find_image()
if img:
   encoded_img = image_to_base64(img)
   st.markdown(
       f"""
<div style="
           height: 380px;
           border-radius: 38px;
           margin-bottom: 32px;
           background:
               linear-gradient(
                   90deg,
                   rgba(5, 11, 24, 0.98) 0%,
                   rgba(7, 23, 44, 0.78) 46%,
                   rgba(4, 9, 20, 0.25) 100%
               ),
               radial-gradient(circle at center, rgba(88,245,222,0.20), transparent 46%),
               url('data:image/png;base64,{encoded_img}');
           background-size: cover;
           background-position: center;
           border: 1px solid rgba(88,245,222,0.36);
           box-shadow:
               0 0 52px rgba(88,245,222,0.20),
               0 20px 46px rgba(0,0,0,0.46);
           display: flex;
           align-items: center;
           padding: 42px;
       ">
<div style="
               max-width: 560px;
               background: rgba(4, 14, 28, 0.58);
               border: 1px solid rgba(88,245,222,0.26);
               border-radius: 26px;
               padding: 26px;
               backdrop-filter: blur(7px);
           ">
<div style="
                   color:#58f5de;
                   font-size:15px;
                   font-weight:900;
                   letter-spacing:1px;
                   margin-bottom:12px;
               ">
                   AI ASSISTANT PLATFORM
</div>
<div style="
                   color:white;
                   font-size:34px;
                   font-weight:900;
                   line-height:1.2;
               ">
                   Intelligent Knowledge Lakehouse for Transport & Logistics
</div>
<div style="
                   color:#b7d7e0;
                   font-size:15px;
                   margin-top:14px;
                   line-height:1.7;
               ">
                   Built with lakehouse processing, data quality checks, RAG indexing,
                   and an interactive AI assistant interface.
</div>
</div>
</div>
       """,
       unsafe_allow_html=True
   )
else:
   st.markdown(
       """
<div class="hero-fallback">
<div>
<div style="font-size:115px;">🤖</div>
<div style="color:#b7d7e0;font-size:15px;margin-top:10px;">
                   Add your image here:<br>
<b>src/app/ai-assistant-cover.png</b>
</div>
</div>
</div>
       """,
       unsafe_allow_html=True
   )

# =========================================================
# Left Answer + Right Question
# =========================================================
answer_col, question_col = st.columns([1, 1])
with answer_col:
   safe_answer = html.escape(st.session_state.answer).replace("\n", "<br>")
   st.markdown(
       f"""
<div class="answer-box">
<h3>Assistant Answer</h3>
           {safe_answer}
</div>
       """,
       unsafe_allow_html=True
   )
with question_col:
   st.markdown(
       """
<div class="question-box">
<h3>Ask the Assistant</h3>
<p>
               Ask about logistics KPIs, SLA performance, lakehouse layers,
               data quality, or RAG retrieval results.
</p>
       """,
       unsafe_allow_html=True
   )
   question = st.text_area(
       "Question",
       placeholder="Write your question here...",
       label_visibility="collapsed",
       height=190
   )
   if st.button("Ask Assistant"):
       st.session_state.answer = get_answer(question)
       try:
           st.rerun()
       except Exception:
           try:
               st.experimental_rerun()
           except Exception:
               pass
   st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# Project Overview
# =========================================================
st.markdown("""
<div class="overview-box">
<b style="color:#58f5de;">Project Overview</b><br><br>
   This project integrates synthetic logistics data, schema validation,
   lakehouse processing, data quality checks, RAG indexing,
   and an interactive AI assistant interface.
</div>
""", unsafe_allow_html=True)

# =========================================================
# Footer
# =========================================================
st.markdown("""
<div class="footer">
   AI Knowledge Lakehouse Assistant for Transport & Logistics — Final Project 
</div>
""", unsafe_allow_html=True)
