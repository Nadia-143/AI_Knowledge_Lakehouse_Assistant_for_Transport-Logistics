import streamlit as st

from pathlib import Path

import html

st.set_page_config(

    page_title="AI Knowledge Lakehouse Assistant",

    page_icon="🤖",

    layout="wide"

)

# =========================

# CSS THEME

# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

* {

    font-family: 'Inter', sans-serif;

}

.stApp {

    background:

        radial-gradient(circle at top left, rgba(0,255,220,0.18), transparent 28%),

        radial-gradient(circle at bottom right, rgba(0,120,255,0.18), transparent 30%),

        linear-gradient(135deg, #050b18 0%, #07162a 45%, #040914 100%);

    color: white;

}

.block-container {

    padding-top: 1.4rem;

    padding-bottom: 2rem;

}

.top-title {

    text-align: center;

    margin-bottom: 26px;

}

.top-title h1 {

    font-size: 48px;

    font-weight: 900;

    margin-bottom: 8px;

    color: #ffffff;

    text-shadow: 0 0 22px rgba(0,255,220,0.25);

}

.top-title p {

    font-size: 16px;

    color: #9fdde7;

    margin: 0;

}

.glow-card {

    background: rgba(8, 22, 42, 0.88);

    border: 1px solid rgba(70,255,230,0.24);

    border-radius: 26px;

    padding: 24px;

    box-shadow:

        0 16px 40px rgba(0,0,0,0.38),

        inset 0 0 24px rgba(0,255,220,0.03);

    backdrop-filter: blur(10px);

    margin-bottom: 18px;

}

.neon-card {

    background:

        linear-gradient(145deg, rgba(10,30,55,0.95), rgba(5,13,26,0.98));

    border: 1px solid rgba(69,255,229,0.38);

    border-radius: 30px;

    padding: 22px;

    box-shadow:

        0 0 34px rgba(0,255,220,0.12),

        0 14px 34px rgba(0,0,0,0.40);

    margin-bottom: 18px;

}

.section-title {

    color: #67fff0;

    font-weight: 800;

    font-size: 19px;

    margin: 8px 0 12px 0;

    letter-spacing: .2px;

}

.robot-frame {

    background:

        radial-gradient(circle at center, rgba(79,255,232,0.20), transparent 48%),

        linear-gradient(180deg, rgba(9,26,48,0.95), rgba(4,12,25,0.98));

    border: 1px solid rgba(98,255,235,0.32);

    border-radius: 32px;

    padding: 14px;

    box-shadow: 0 0 40px rgba(0,255,220,0.14);

}

.answer-box {

    background: rgba(4, 14, 28, 0.98);

    border: 1px solid rgba(89,255,232,0.42);

    border-left: 6px solid #58f5de;

    border-radius: 22px;

    padding: 22px;

    min-height: 210px;

    color: #effdff;

    line-height: 1.7;

    box-shadow: 0 0 28px rgba(0,255,220,0.10);

}

.question-box {

    background: rgba(7, 20, 38, 0.92);

    border: 1px solid rgba(89,255,232,0.30);

    border-radius: 26px;

    padding: 24px;

    box-shadow: 0 16px 36px rgba(0,0,0,0.32);

}

.team-box {

    background: rgba(7, 20, 38, 0.82);

    border: 1px solid rgba(89,255,232,0.24);

    border-radius: 24px;

    padding: 18px;

}

.team-chip {

    display: block;

    background: linear-gradient(90deg, rgba(88,245,222,0.16), rgba(57,196,255,0.10));

    border: 1px solid rgba(88,245,222,0.25);

    border-radius: 999px;

    padding: 11px 15px;

    color: white;

    font-weight: 700;

    margin-bottom: 10px;

}

.kpi {

    background: rgba(8, 22, 42, 0.86);

    border: 1px solid rgba(70,255,230,0.22);

    border-radius: 20px;

    padding: 16px;

    text-align: center;

    box-shadow: 0 10px 24px rgba(0,0,0,0.25);

}

.kpi h3 {

    color: #58f5de;

    margin: 0;

    font-size: 24px;

}

.kpi p {

    color: #a7cbd7;

    margin: 5px 0 0 0;

    font-size: 13px;

}

.small-text {

    color: #b7d7e0;

    font-size: 14px;

    line-height: 1.65;

}

.stTextArea textarea {

    background-color: #06162b !important;

    color: #ffffff !important;

    border: 1px solid rgba(88,245,222,0.55) !important;

    border-radius: 18px !important;

    min-height: 180px !important;

}

.stButton button {

    background: linear-gradient(90deg, #58f5de, #39c4ff) !important;

    color: #04101e !important;

    border: 0 !important;

    border-radius: 999px !important;

    font-weight: 900 !important;

    padding: 0.75rem 1.8rem !important;

    width: 100%;

    box-shadow: 0 10px 22px rgba(0,255,220,0.20);

}

.stButton button:hover {

    transform: scale(1.01);

}

hr {

    border: none;

    border-top: 1px solid rgba(88,245,222,0.18);

}

.footer {

    text-align: center;

    color: #6fa6b8;

    font-size: 13px;

    margin-top: 22px;

}
</style>

""", unsafe_allow_html=True)


# =========================

# HELPERS

# =========================

def find_image():

    paths = [

        "src/app/ai-assistant-cover.png",

        "src/app/ai-assistant-cover.jpg",

        "src/app/assistant.png",

        "assets/project_cover.png",

        "outputs/screenshots/project_cover.png",

    ]

    for p in paths:

        if Path(p).exists():

            return p

    return None


def get_answer(question: str) -> str:

    if not question.strip():

        return "Type your question in the box on the right, then click Ask Assistant."

    try:

        from src.rag import query_engine

        for fn in ["answer_question", "ask", "query", "run_query", "generate_answer"]:

            if hasattr(query_engine, fn):

                return str(getattr(query_engine, fn)(question))

    except Exception:

        pass

    return f"""AI Assistant Response

Question:

{question}

This platform supports questions about:

• Transport and logistics KPIs

• Lakehouse Bronze, Silver, and Gold layers

• Data quality checks

• SLA indicators

• RAG retrieval and AI-generated insights

"""


# =========================

# STATE

# =========================

if "answer" not in st.session_state:

    st.session_state.answer = "The assistant response will appear here."

# =========================

# HEADER

# =========================

st.markdown("""
<div class="top-title">
<h1>AI Knowledge Lakehouse Assistant</h1>
<p>Transport & Logistics Intelligent Data Platform</p>
</div>

""", unsafe_allow_html=True)

# =========================

# KPI ROW

# =========================

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.markdown('<div class="kpi"><h3>Bronze</h3><p>Raw Data</p></div>', unsafe_allow_html=True)

with k2:

    st.markdown('<div class="kpi"><h3>Silver</h3><p>Clean Data</p></div>', unsafe_allow_html=True)

with k3:

    st.markdown('<div class="kpi"><h3>Gold</h3><p>KPI Layer</p></div>', unsafe_allow_html=True)

with k4:

    st.markdown('<div class="kpi"><h3>RAG</h3><p>AI Search</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================

# MAIN LAYOUT

# =========================

left, right = st.columns([1.15, 1])

with left:

    st.markdown('<div class="section-title">AI Assistant Visual</div>', unsafe_allow_html=True)

    img = find_image()

    if img:

        st.markdown('<div class="robot-frame">', unsafe_allow_html=True)

        st.image(img, use_column_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown("""
<div class="neon-card">
<div style="font-size:80px;text-align:center;">🤖</div>
<p class="small-text" style="text-align:center;">

                Add image as: <b>src/app/ai-assistant-cover.png</b>
</p>
</div>

        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Assistant Answer</div>', unsafe_allow_html=True)

    safe_answer = html.escape(st.session_state.answer).replace("\n", "<br>")

    st.markdown(f"""
<div class="answer-box">

        {safe_answer}
</div>

    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Team Members</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="team-box">
<div class="team-chip">Nadia Alghamdi</div>
<div class="team-chip">Ebtisam Mohammed Alzahrani</div>
<div class="team-chip">Manar ALmutairi</div>

</div>

    """, unsafe_allow_html=True)

with right:

    st.markdown('<div class="section-title">Ask the Assistant</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="question-box">
<p class="small-text">

            Ask about logistics indicators, data sources, SLA performance,

            lakehouse layers, or AI retrieval results.
</p>
</div>

    """, unsafe_allow_html=True)

    question = st.text_area(

        "Question",

        placeholder="Example: What are the main logistics KPIs in this project?",

        label_visibility="collapsed",

        height=210

    )

    if st.button("Ask Assistant"):

        st.session_state.answer = get_answer(question)

        st.rerun()

    st.markdown('<div class="section-title">Project Overview</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="glow-card">
<p class="small-text">

            This project integrates synthetic logistics data, schema validation,

            lakehouse processing, data quality checks, RAG indexing,

            and an interactive AI assistant interface.
</p>
</div>

    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Execution Flow</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="glow-card">
<p class="small-text">

            1. Generate synthetic transport data<br>

            2. Validate schema and quality rules<br>

            3. Process Bronze, Silver, and Gold layers<br>

            4. Build RAG index<br>

            5. Query through AI assistant
</p>
</div>

    """, unsafe_allow_html=True)

# =========================

# AVAILABLE SOURCES

# =========================

st.markdown('<div class="section-title">Available Sources</div>', unsafe_allow_html=True)

files = [

    "data/raw/shipments.csv",

    "data/raw/ports_operations.csv",

    "data/raw/rail_trips.csv",

    "data/raw/road_incidents.csv",

    "data/raw/passengers.csv",

    "data/catalog/transport_kpi_catalog.csv",

    "data/catalog/sla_templates.csv",

]

existing = [f for f in files if Path(f).exists()]

if existing:

    src_html = "<br>".join([f"• {f}" for f in existing])

else:

    src_html = "Source files will appear here after running the pipeline."

st.markdown(f"""
<div class="glow-card">
<p class="small-text">{src_html}</p>
</div>

""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">

    AI Knowledge Lakehouse Assistant for Transport & Logistics — Final Project Demo
</div>

""", unsafe_allow_html=True)
 
import streamlit as st

from pathlib import Path

import html

st.set_page_config(

    page_title="AI Knowledge Lakehouse Assistant",

    page_icon="🤖",

    layout="wide"

)

# =========================

# CSS THEME

# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

* {

    font-family: 'Inter', sans-serif;

}

.stApp {

    background:

        radial-gradient(circle at top left, rgba(0,255,220,0.18), transparent 28%),

        radial-gradient(circle at bottom right, rgba(0,120,255,0.18), transparent 30%),

        linear-gradient(135deg, #050b18 0%, #07162a 45%, #040914 100%);

    color: white;

}

.block-container {

    padding-top: 1.4rem;

    padding-bottom: 2rem;

}

.top-title {

    text-align: center;

    margin-bottom: 26px;

}

.top-title h1 {

    font-size: 48px;

    font-weight: 900;

    margin-bottom: 8px;

    color: #ffffff;

    text-shadow: 0 0 22px rgba(0,255,220,0.25);

}

.top-title p {

    font-size: 16px;

    color: #9fdde7;

    margin: 0;

}

.glow-card {

    background: rgba(8, 22, 42, 0.88);

    border: 1px solid rgba(70,255,230,0.24);

    border-radius: 26px;

    padding: 24px;

    box-shadow:

        0 16px 40px rgba(0,0,0,0.38),

        inset 0 0 24px rgba(0,255,220,0.03);

    backdrop-filter: blur(10px);

    margin-bottom: 18px;

}

.neon-card {

    background:

        linear-gradient(145deg, rgba(10,30,55,0.95), rgba(5,13,26,0.98));

    border: 1px solid rgba(69,255,229,0.38);

    border-radius: 30px;

    padding: 22px;

    box-shadow:

        0 0 34px rgba(0,255,220,0.12),

        0 14px 34px rgba(0,0,0,0.40);

    margin-bottom: 18px;

}

.section-title {

    color: #67fff0;

    font-weight: 800;

    font-size: 19px;

    margin: 8px 0 12px 0;

    letter-spacing: .2px;

}

.robot-frame {

    background:

        radial-gradient(circle at center, rgba(79,255,232,0.20), transparent 48%),

        linear-gradient(180deg, rgba(9,26,48,0.95), rgba(4,12,25,0.98));

    border: 1px solid rgba(98,255,235,0.32);

    border-radius: 32px;

    padding: 14px;

    box-shadow: 0 0 40px rgba(0,255,220,0.14);

}

.answer-box {

    background: rgba(4, 14, 28, 0.98);

    border: 1px solid rgba(89,255,232,0.42);

    border-left: 6px solid #58f5de;

    border-radius: 22px;

    padding: 22px;

    min-height: 210px;

    color: #effdff;

    line-height: 1.7;

    box-shadow: 0 0 28px rgba(0,255,220,0.10);

}

.question-box {

    background: rgba(7, 20, 38, 0.92);

    border: 1px solid rgba(89,255,232,0.30);

    border-radius: 26px;

    padding: 24px;

    box-shadow: 0 16px 36px rgba(0,0,0,0.32);

}

.team-box {

    background: rgba(7, 20, 38, 0.82);

    border: 1px solid rgba(89,255,232,0.24);

    border-radius: 24px;

    padding: 18px;

}

.team-chip {

    display: block;

    background: linear-gradient(90deg, rgba(88,245,222,0.16), rgba(57,196,255,0.10));

    border: 1px solid rgba(88,245,222,0.25);

    border-radius: 999px;

    padding: 11px 15px;

    color: white;

    font-weight: 700;

    margin-bottom: 10px;

}

.kpi {

    background: rgba(8, 22, 42, 0.86);

    border: 1px solid rgba(70,255,230,0.22);

    border-radius: 20px;

    padding: 16px;

    text-align: center;

    box-shadow: 0 10px 24px rgba(0,0,0,0.25);

}

.kpi h3 {

    color: #58f5de;

    margin: 0;

    font-size: 24px;

}

.kpi p {

    color: #a7cbd7;

    margin: 5px 0 0 0;

    font-size: 13px;

}

.small-text {

    color: #b7d7e0;

    font-size: 14px;

    line-height: 1.65;

}

.stTextArea textarea {

    background-color: #06162b !important;

    color: #ffffff !important;

    border: 1px solid rgba(88,245,222,0.55) !important;

    border-radius: 18px !important;

    min-height: 180px !important;

}

.stButton button {

    background: linear-gradient(90deg, #58f5de, #39c4ff) !important;

    color: #04101e !important;

    border: 0 !important;

    border-radius: 999px !important;

    font-weight: 900 !important;

    padding: 0.75rem 1.8rem !important;

    width: 100%;

    box-shadow: 0 10px 22px rgba(0,255,220,0.20);

}

.stButton button:hover {

    transform: scale(1.01);

}

hr {

    border: none;

    border-top: 1px solid rgba(88,245,222,0.18);

}

.footer {

    text-align: center;

    color: #6fa6b8;

    font-size: 13px;

    margin-top: 22px;

}
</style>

""", unsafe_allow_html=True)


# =========================

# HELPERS

# =========================

def find_image():

    paths = [

        "src/app/ai-assistant-cover.png",

        "src/app/ai-assistant-cover.jpg",

        "src/app/assistant.png",

        "assets/project_cover.png",

        "outputs/screenshots/project_cover.png",

    ]

    for p in paths:

        if Path(p).exists():

            return p

    return None


def get_answer(question: str) -> str:

    if not question.strip():

        return "Type your question in the box on the right, then click Ask Assistant."

    try:

        from src.rag import query_engine

        for fn in ["answer_question", "ask", "query", "run_query", "generate_answer"]:

            if hasattr(query_engine, fn):

                return str(getattr(query_engine, fn)(question))

    except Exception:

        pass

    return f"""AI Assistant Response

Question:

{question}

This platform supports questions about:

• Transport and logistics KPIs

• Lakehouse Bronze, Silver, and Gold layers

• Data quality checks

• SLA indicators

• RAG retrieval and AI-generated insights

"""


# =========================

# STATE

# =========================

if "answer" not in st.session_state:

    st.session_state.answer = "The assistant response will appear here."

# =========================

# HEADER

# =========================

st.markdown("""
<div class="top-title">
<h1>AI Knowledge Lakehouse Assistant</h1>
<p>Transport & Logistics Intelligent Data Platform</p>
</div>

""", unsafe_allow_html=True)

# =========================

# KPI ROW

# =========================

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.markdown('<div class="kpi"><h3>Bronze</h3><p>Raw Data</p></div>', unsafe_allow_html=True)

with k2:

    st.markdown('<div class="kpi"><h3>Silver</h3><p>Clean Data</p></div>', unsafe_allow_html=True)

with k3:

    st.markdown('<div class="kpi"><h3>Gold</h3><p>KPI Layer</p></div>', unsafe_allow_html=True)

with k4:

    st.markdown('<div class="kpi"><h3>RAG</h3><p>AI Search</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================

# MAIN LAYOUT

# =========================

left, right = st.columns([1.15, 1])

with left:

    st.markdown('<div class="section-title">AI Assistant Visual</div>', unsafe_allow_html=True)

    img = find_image()

    if img:

        st.markdown('<div class="robot-frame">', unsafe_allow_html=True)

        st.image(img, use_column_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown("""
<div class="neon-card">
<div style="font-size:80px;text-align:center;">🤖</div>
<p class="small-text" style="text-align:center;">

                Add image as: <b>src/app/ai-assistant-cover.png</b>
</p>
</div>

        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Assistant Answer</div>', unsafe_allow_html=True)

    safe_answer = html.escape(st.session_state.answer).replace("\n", "<br>")

    st.markdown(f"""
<div class="answer-box">

        {safe_answer}
</div>

    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Team Members</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="team-box">
<div class="team-chip">Nadia Alghamdi</div>
<div class="team-chip">Name 2</div>
<div class="team-chip">Name 3</div>
<div class="team-chip">Name 4</div>
</div>

    """, unsafe_allow_html=True)

with right:

    st.markdown('<div class="section-title">Ask the Assistant</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="question-box">
<p class="small-text">

            Ask about logistics indicators, data sources, SLA performance,

            lakehouse layers, or AI retrieval results.
</p>
</div>

    """, unsafe_allow_html=True)

    question = st.text_area(

        "Question",

        placeholder="Example: What are the main logistics KPIs in this project?",

        label_visibility="collapsed",

        height=210

    )

    if st.button("Ask Assistant"):

        st.session_state.answer = get_answer(question)

        st.rerun()

    st.markdown('<div class="section-title">Project Overview</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="glow-card">
<p class="small-text">

            This project integrates synthetic logistics data, schema validation,

            lakehouse processing, data quality checks, RAG indexing,

            and an interactive AI assistant interface.
</p>
</div>

    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Execution Flow</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="glow-card">
<p class="small-text">

            1. Generate synthetic transport data<br>

            2. Validate schema and quality rules<br>

            3. Process Bronze, Silver, and Gold layers<br>

            4. Build RAG index<br>

            5. Query through AI assistant
</p>
</div>

    """, unsafe_allow_html=True)

# =========================

# AVAILABLE SOURCES

# =========================

st.markdown('<div class="section-title">Available Sources</div>', unsafe_allow_html=True)

files = [

    "data/raw/shipments.csv",

    "data/raw/ports_operations.csv",

    "data/raw/rail_trips.csv",

    "data/raw/road_incidents.csv",

    "data/raw/passengers.csv",

    "data/catalog/transport_kpi_catalog.csv",

    "data/catalog/sla_templates.csv",

]

existing = [f for f in files if Path(f).exists()]

if existing:

    src_html = "<br>".join([f"• {f}" for f in existing])

else:

    src_html = "Source files will appear here after running the pipeline."

st.markdown(f"""
<div class="glow-card">
<p class="small-text">{src_html}</p>
</div>

""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">

    AI Knowledge Lakehouse Assistant for Transport & Logistics — Final Project Demo
</div>

""", unsafe_allow_html=True)
 
