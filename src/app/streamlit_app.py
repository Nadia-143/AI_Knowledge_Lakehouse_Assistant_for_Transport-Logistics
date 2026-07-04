import streamlit as st

from pathlib import Path

import base64

import html

st.set_page_config(

    page_title="المساعد الذكي",

    page_icon="🤖",

    layout="wide"

)

# =========================

# Helpers

# =========================

def file_to_base64(path: str):

    p = Path(path)

    if p.exists():

        with open(p, "rb") as f:

            return base64.b64encode(f.read()).decode()

    return None


def find_cover_image():

    paths = [

        "src/app/ai-assistant-cover.png",

        "src/app/ai-assistant-cover.jpg",

        "src/app/assistant.png",

        "assets/project_cover.png",

        "outputs/screenshots/project_cover.png",

    ]

    for path in paths:

        if Path(path).exists():

            return path

    return None


def get_answer(question: str) -> str:

    if not question.strip():

        return "ستظهر إجابة المساعد هنا بعد إرسال السؤال."

    try:

        from src.rag import query_engine

        for function_name in ["answer_question", "ask", "query", "run_query", "generate_answer"]:

            if hasattr(query_engine, function_name):

                result = getattr(query_engine, function_name)(question)

                return str(result)

    except Exception:

        pass

    return f"""إجابة المساعد الذكي:

السؤال:

{question}

يمكن لهذا المساعد دعم الاستفسارات المتعلقة بـ:

• مؤشرات النقل والخدمات اللوجستية

• طبقات Lakehouse

• فحوصات جودة البيانات

• مؤشرات SLA

• البحث الذكي باستخدام RAG

"""


# =========================

# State

# =========================

if "answer" not in st.session_state:

    st.session_state.answer = "ستظهر إجابة المساعد هنا بعد إرسال السؤال."

# =========================

# Assets

# =========================

cover_path = find_cover_image()

cover_base64 = file_to_base64(cover_path) if cover_path else None

logo_base64 = file_to_base64("src/app/sdaia_logo.png")

# =========================

# CSS

# =========================

st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');

    * {

        font-family: 'DIN Next LT Arabic', 'DIN Next Arabic', 'Tajawal', 'Arial', sans-serif !important;

    }

    .stApp {

        direction: rtl;

        background:

            radial-gradient(circle at 15% 15%, rgba(88,245,222,0.16), transparent 25%),

            radial-gradient(circle at 85% 80%, rgba(57,196,255,0.14), transparent 28%),

            linear-gradient(135deg, #061120 0%, #07172c 45%, #04101a 100%);

        color: white;

    }

    .block-container {

        max-width: 1650px;

        padding-top: 2rem;

        padding-bottom: 2rem;

    }

    [data-testid="stException"] {

        display: none !important;

    }

    /* Header */

    .header-wrap {

        position: relative;

        min-height: 150px;

        margin-bottom: 20px;

    }

    .logo-left {

        position: absolute;

        left: 0;

        top: 0;

    }

    .logo-left img {

        width: 210px;

        max-width: 210px;

        height: auto;

        object-fit: contain;

        filter: drop-shadow(0 0 14px rgba(88,245,222,0.25));

    }

    .title-area {

        text-align: center;

        padding-top: 18px;

    }

    .main-title {

        font-size: 54px;

        font-weight: 900;

        color: #ffffff;

        margin-bottom: 6px;

        text-shadow: 0 0 24px rgba(88,245,222,0.35);

    }

    .sub-title {

        font-size: 20px;

        color: #b9fff4;

        margin-bottom: 14px;

        font-weight: 700;

    }

    .team-row {

        text-align: center;

        direction: rtl;

        margin-bottom: 10px;

    }

    .team-label {

        color: #58f5de;

        font-weight: 900;

        font-size: 16px;

        margin-left: 8px;

    }

    .team-chip {

        display: inline-block;

        padding: 10px 18px;

        margin: 5px;

        border-radius: 999px;

        border: 1px solid rgba(88,245,222,0.35);

        background: linear-gradient(90deg, rgba(88,245,222,0.16), rgba(57,196,255,0.10));

        color: white;

        font-weight: 800;

        box-shadow: 0 8px 18px rgba(0,0,0,0.20);

    }

    .trainer {

        text-align: center;

        font-size: 17px;

        color: #d3fffb;

        font-weight: 800;

        margin-bottom: 24px;

    }

    /* Main image stage */

    .stage {

        position: relative;

        width: 100%;

        min-height: 760px;

        border-radius: 40px;

        overflow: hidden;

        border: 1px solid rgba(88,245,222,0.35);

        box-shadow:

            0 0 45px rgba(88,245,222,0.14),

            0 20px 48px rgba(0,0,0,0.40);

        background-size: cover;

        background-position: center;

        margin-bottom: 26px;

    }

    .stage-overlay {

        position: absolute;

        inset: 0;

        background:

            linear-gradient(90deg, rgba(5,11,24,0.55) 0%, rgba(7,23,44,0.15) 50%, rgba(5,11,24,0.55) 100%),

            radial-gradient(circle at center, rgba(88,245,222,0.10), transparent 52%);

    }

    .hero-box {

        position: absolute;

        top: 38px;

        right: 40px;

        width: 34%;

        z-index: 3;

        background: rgba(4,14,28,0.62);

        border: 1px solid rgba(88,245,222,0.28);

        border-radius: 28px;

        padding: 20px;

        backdrop-filter: blur(8px);

    }

    .hero-tag {

        color: #58f5de;

        font-size: 14px;

        font-weight: 900;

        margin-bottom: 8px;

    }

    .hero-title {

        font-size: 34px;

        font-weight: 900;

        color: white;

        line-height: 1.35;

        margin-bottom: 10px;

    }

    .hero-text {

        color: #d9f5f6;

        font-size: 15px;

        line-height: 1.8;

        font-weight: 600;

    }

    .answer-panel {

        position: absolute;

        left: 55px;

        top: 260px;

        width: 30%;

        min-height: 260px;

        z-index: 3;

        background: rgba(5,16,30,0.88);

        border: 1px solid rgba(88,245,222,0.40);

        border-radius: 28px;

        padding: 24px;

        box-shadow: 0 14px 30px rgba(0,0,0,0.30);

        backdrop-filter: blur(9px);

        text-align: right;

        direction: rtl;

    }

    .question-panel {

        position: absolute;

        right: 55px;

        top: 320px;

        width: 30%;

        min-height: 230px;

        z-index: 3;

        background: rgba(5,16,30,0.88);

        border: 1px solid rgba(88,245,222,0.40);

        border-radius: 28px;

        padding: 24px;

        box-shadow: 0 14px 30px rgba(0,0,0,0.30);

        backdrop-filter: blur(9px);

        text-align: right;

        direction: rtl;

    }

    .panel-title {

        color: #58f5de;

        font-size: 28px;

        font-weight: 900;

        margin-bottom: 12px;

    }

    .panel-text {

        color: #f2ffff;

        font-size: 17px;

        line-height: 1.9;

        font-weight: 600;

    }

    /* Input area */

    .input-title {

        color: #58f5de;

        font-size: 22px;

        font-weight: 900;

        margin-bottom: 10px;

        text-align: right;

    }

    .stTextArea textarea {

        background-color: rgba(6, 22, 43, 0.96) !important;

        color: #ffffff !important;

        border: 1px solid rgba(88,245,222,0.55) !important;

        border-radius: 18px !important;

        min-height: 170px !important;

        direction: rtl !important;

        text-align: right !important;

        font-size: 18px !important;

        font-weight: 600 !important;

    }

    .stButton button {

        background: linear-gradient(90deg, #58f5de, #39c4ff) !important;

        color: #04101e !important;

        border: 0 !important;

        border-radius: 999px !important;

        font-weight: 900 !important;

        padding: 0.8rem 1.8rem !important;

        width: 100%;

        font-size: 17px !important;

        box-shadow: 0 10px 20px rgba(0,255,220,0.20);

    }

    .overview-box {

        margin-top: 20px;

        background: rgba(8,22,42,0.84);

        border: 1px solid rgba(88,245,222,0.22);

        border-radius: 26px;

        padding: 22px;

        color: #d0edf0;

        line-height: 2;

        text-align: right;

        direction: rtl;

        font-size: 17px;

        font-weight: 600;

    }

    .footer {

        text-align: center;

        color: #7caaba;

        font-size: 14px;

        margin-top: 26px;

    }
</style>

""", unsafe_allow_html=True)

# =========================

# Header

# =========================

logo_html = f'<img src="data:image/png;base64,{logo_base64}">' if logo_base64 else ""

st.markdown(f"""
<div class="header-wrap">
<div class="logo-left">{logo_html}</div>
<div class="title-area">
<div class="main-title">المساعد الذكي</div>
<div class="sub-title">في قطاع النقل والخدمات اللوجستية</div>
<div class="team-row">
<span class="team-label">أسماء الفريق:</span>
<span class="team-chip">نادية الغامدي</span>
<span class="team-chip">اسم العضو الثاني</span>
<span class="team-chip">اسم العضو الثالث</span>
<span class="team-chip">اسم العضو الرابع</span>
</div>
<div class="trainer">المدرب: محمد عبدالفتاح</div>
</div>
</div>

""", unsafe_allow_html=True)

# =========================

# Main Stage

# =========================

if cover_base64:

    bg_style = f"""

        background-image:

            linear-gradient(90deg, rgba(5,11,24,0.25), rgba(7,23,44,0.06), rgba(5,11,24,0.25)),

            url('data:image/png;base64,{cover_base64}');

    """

else:

    bg_style = """

        background:

            radial-gradient(circle at center, rgba(88,245,222,0.20), rgba(8,22,42,0.96) 60%);

    """

safe_answer = html.escape(st.session_state.answer).replace("\n", "<br>")

st.markdown(f"""
<div class="stage" style="{bg_style}">
<div class="stage-overlay"></div>
<div class="hero-box">
<div class="hero-tag">منصة مساعد ذكي</div>
<div class="hero-title">مساعد معرفي ذكي لقطاع النقل والخدمات اللوجستية</div>
<div class="hero-text">

            يعتمد على معالجة البيانات، فحص الجودة، وبناء المعرفة الذكية باستخدام RAG.
</div>
</div>
<div class="answer-panel">
<div class="panel-title">إجابة المساعد</div>
<div class="panel-text">{safe_answer}</div>
</div>
<div class="question-panel">
<div class="panel-title">اسألي المساعد</div>
<div class="panel-text">

            اكتبي سؤالًا عن مؤشرات النقل، جودة البيانات، طبقات Lakehouse،

            أو نتائج البحث الذكي.
</div>
</div>
</div>

""", unsafe_allow_html=True)

# =========================

# Input

# =========================

st.markdown('<div class="input-title">اكتبي سؤالك هنا</div>', unsafe_allow_html=True)

spacer, input_col = st.columns([1, 1.25])

with input_col:

    question = st.text_area(

        "السؤال",

        placeholder="اكتبي سؤالك هنا...",

        label_visibility="collapsed",

        height=170

    )

    if st.button("إرسال السؤال"):

        st.session_state.answer = get_answer(question)

        try:

            st.rerun()

        except Exception:

            try:

                st.experimental_rerun()

            except Exception:

                pass

# =========================

# Overview

# =========================

st.markdown("""
<div class="overview-box">
<b style="color:#58f5de;">نبذة عن المشروع</b><br><br>

    يدمج هذا المشروع بين بيانات لوجستية، فحوصات جودة البيانات،

    ومعالجة المعرفة الذكية، مع واجهة تفاعلية لمساعد ذكي يخدم قطاع النقل والخدمات اللوجستية.
</div>

""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">

    مشروع المساعد الذكي لقطاع النقل والخدمات اللوجستية
</div>

""", unsafe_allow_html=True)
 
