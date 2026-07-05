import streamlit as st
from pathlib import Path
import base64
import html
# =========================================================
# Page Config
# =========================================================
st.set_page_config(
   page_title="المساعد الذكي",
   page_icon="🤖",
   layout="wide",
   initial_sidebar_state="collapsed"
)
APP_DIR = Path(__file__).parent

# =========================================================
# Helpers
# =========================================================
def file_to_base64(path):
   path = Path(path)
   if path.exists():
       return base64.b64encode(path.read_bytes()).decode("utf-8")
   return None

def normalize_rag_result(result):
   """
   يحول ناتج RAG إلى جواب + مصادر إن وجدت.
   يدعم string أو dict أو list.
   """
   if result is None:
       return "", []
   if isinstance(result, dict):
       answer = (
           result.get("answer")
           or result.get("response")
           or result.get("result")
           or result.get("output")
           or ""
       )
       sources = (
           result.get("sources")
           or result.get("documents")
           or result.get("contexts")
           or result.get("context")
           or result.get("source_documents")
           or []
       )
       return str(answer).strip(), sources
   if isinstance(result, str):
       return result.strip(), []
   if isinstance(result, list):
       if not result:
           return "", []
       joined = "\n".join(str(x) for x in result if str(x).strip())
       return joined.strip(), result
   return str(result).strip(), []

def is_weak_or_hallucinated_answer(answer):
   """
   فلترة الإجابات العامة أو غير المفيدة.
   """
   if not answer or not answer.strip():
       return True
   weak_patterns = [
       "i don't know",
       "i do not know",
       "لا أعلم",
       "لا اعلم",
       "لا توجد معلومات",
       "لا يوجد معلومات",
       "not found",
       "no relevant",
       "no context",
       "لا يوجد سياق",
       "لا يوجد مصدر",
       "غير متوفر",
       "غير موجود",
       "cannot answer",
       "لا يمكنني الإجابة",
   ]
   answer_lower = answer.lower()
   for pattern in weak_patterns:
       if pattern in answer_lower:
           return True
   return False

def get_answer(question: str) -> str:
   """
   المنطق الصحيح:
   1. يأخذ السؤال.
   2. يحاول يبحث في RAG.
   3. إذا وجد إجابة مدعومة يعرضها.
   4. إذا لم يجد، لا يخترع جواب.
   """
   q = question.strip()
   if not q:
       return "لم يتم إدخال سؤال."
   try:
       from src.rag import query_engine
       # أسماء الدوال المحتملة في مشروعك
       possible_functions = [
           "answer_question",
           "ask",
           "query",
           "run_query",
           "generate_answer",
           "search",
           "retrieve"
       ]
       for fn_name in possible_functions:
           if hasattr(query_engine, fn_name):
               fn = getattr(query_engine, fn_name)
               result = fn(q)
               answer, sources = normalize_rag_result(result)
               if is_weak_or_hallucinated_answer(answer):
                   return "لم أجد إجابة مرتبطة بهذا السؤال في مصادر البيانات المتاحة."
               # إذا رجعت الدالة dict وفيه مصادر، ممتاز
               if sources:
                   return answer
               # إذا رجعت الدالة نص فقط، نعرض النص بشرط أنه مو جواب ضعيف
               # الأفضل مستقبلًا أن query_engine يرجع answer + sources
               return answer
   except Exception:
       return "تعذر الوصول إلى محرك البحث المعرفي RAG. تأكدي من بناء الفهرس وتشغيل ملفات المشروع المطلوبة."
   return "لم أجد إجابة مرتبطة بهذا السؤال في مصادر البيانات المتاحة."

def clear_chat():
   st.session_state.chat_history = []

# =========================================================
# Session State
# =========================================================
if "chat_history" not in st.session_state:
   st.session_state.chat_history = []

# =========================================================
# Assets
# =========================================================
logo_base64 = file_to_base64(APP_DIR / "sdaia_logo.png")
background_base64 = None
logo_html = (
   f'<img src="data:image/png;base64,{logo_base64}">'
   if logo_base64
   else '<div class="logo-fallback">أكاديمية سدايا</div>'
)
page_background_css = """
       background:
           radial-gradient(circle at 50% 42%, rgba(34,232,213,0.16), transparent 28%),
           radial-gradient(circle at 18% 30%, rgba(34,232,213,0.10), transparent 32%),
           radial-gradient(circle at 84% 65%, rgba(51,191,255,0.09), transparent 34%),
           radial-gradient(circle, rgba(34,232,213,0.07) 1px, transparent 1.2px) 0 0/26px 26px,
           linear-gradient(180deg, #030710 0%, #04101c 55%, #030710 100%);
   """

# =========================================================
# Latest Answer
# =========================================================
latest_answer = (
   st.session_state.chat_history[-1]["a"]
   if st.session_state.chat_history
   else "بانتظار السؤال. سيتم عرض الإجابة فقط إذا وُجدت معلومة مرتبطة في مصادر البيانات."
)
answer_safe = html.escape(latest_answer).replace("\n", "<br>")

# =========================================================
# Content
# =========================================================
TEAM = [
   "نادية الغامدي",
   "  ابتسام محمد الزهراني ",
   "منار المطيري"
]
DATA_SOURCES = [
   "بيانات الشحنات",
   "عمليات الموانئ",
   "رحلات السكك الحديدية",
   "حوادث الطرق",
   "بيانات الركاب",
   "كتالوج مؤشرات الأداء",
   "قوالب اتفاقيات SLA"
]
team_chips = "".join(f'<span class="chip">{name}</span>' for name in TEAM)
source_chips = "".join(f'<span class="source-chip">{source}</span>' for source in DATA_SOURCES)

# =========================================================
# Icons
# =========================================================
ICON_PERSON = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="8" r="3.6"/>
<path d="M4.5 19.5c0-3.8 3.4-6 7.5-6s7.5 2.2 7.5 6"/>
</svg>
"""
ICON_SPARKLE = """
<svg viewBox="0 0 24 24" fill="currentColor">
<path d="M12 2.5l1.7 5 5 1.7-5 1.7-1.7 5-1.7-5-5-1.7 5-1.7 1.7-5z"/>
</svg>
"""
ICON_CHECK = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M4 12.5l4.5 4.5L20 6"/>
</svg>
"""
ICON_CHAT = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
stroke-width="2" stroke-linejoin="round">
<path d="M4 4.5h16v11H8.5L4 19V4.5z"/>
</svg>
"""
ICON_DB = """
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
<ellipse cx="12" cy="5" rx="7.5" ry="2.6"/>
<path d="M4.5 5v6.2c0 1.4 3.4 2.6 7.5 2.6s7.5-1.2 7.5-2.6V5"/>
<path d="M4.5 11.2v6.2c0 1.4 3.4 2.6 7.5 2.6s7.5-1.2 7.5-2.6v-6.2"/>
</svg>
"""

# =========================================================
# CSS
# =========================================================
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&display=swap');
* {
   font-family:
       'DIN Next LT Arabic',
       'DIN Next Arabic',
       'DIN Text Arabic',
       'DINNextLTArabic',
       'Tajawal',
       'Arial',
       sans-serif !important;
   box-sizing: border-box;
}
:root {
   --cyan: #22e8d5;
   --blue: #33bfff;
   --panel: rgba(8, 22, 38, 0.82);
   --muted: #8fb0bf;
}
.stApp,
[data-testid="stAppViewContainer"] {
   direction: rtl;
   PAGE_BACKGROUND_CSS
   color: #eaf6f7;
}
[data-testid="stHeader"] {
   background: transparent !important;
}
[data-testid="stToolbar"] {
   display: none !important;
}
.block-container {
   max-width: 1180px;
   padding-top: 1.4rem;
   padding-bottom: 2rem;
}
[data-testid="stException"] {
   display: none !important;
}
/* ---------- Header ---------- */
.header-row {
   position: relative;
   min-height: 82px;
}
.logo-left {
   position: absolute;
   left: 0;
   top: 0;
}
.logo-left img {
   width: 300px;
   height: auto;
   filter: drop-shadow(0 0 16px rgba(34,232,213,0.34));
}
.logo-fallback {
   color: var(--cyan);
   font-weight: 900;
   font-size: 18px;
}
.title-block {
   text-align: center;
}
.main-title {
   font-size: 54px;
   font-weight: 900;
   color: #fff;
   text-shadow: 0 0 26px rgba(34,232,213,0.55);
   margin-bottom: 4px;
}
.sub-title {
   font-size: 20px;
   font-weight: 800;
   color: var(--cyan);
   display: flex;
   align-items: center;
   justify-content: center;
   gap: 12px;
}
.sub-title::before,
.sub-title::after {
   content: "";
   height: 1px;
   width: 64px;
   background: linear-gradient(90deg, transparent, rgba(34,232,213,0.6), transparent);
}
.brief {
   max-width: 760px;
   margin: 14px auto 6px;
   color: #d9ffff;
   font-size: 14px;
   line-height: 1.9;
   font-weight: 700;
   text-align: center;
   text-shadow: 0 0 12px rgba(0,0,0,0.85);
}
.meta-row {
   display: flex;
   align-items: center;
   justify-content: center;
   gap: 15px;
   flex-wrap: wrap;
   margin: 20px 0 10px;
}
.meta-label {
   color: var(--muted);
   font-weight: 800;
   font-size: 14px;
}
.chip {
   padding: 8px 18px;
   border-radius: 999px;
   font-weight: 800;
   font-size: 14px;
   color: #fff;
   background: rgba(255,255,255,0.05);
   border: 1px solid rgba(34,232,213,0.35);
   backdrop-filter: blur(8px);
}
.trainer-row {
   display: flex;
   align-items: center;
   justify-content: center;
   margin-bottom: 26px;
}
.trainer-pill {
   display: flex;
   align-items: center;
   gap: 10px;
   padding: 9px 22px;
   border-radius: 999px;
   border: 1px solid rgba(34,232,213,0.35);
   background: rgba(255,255,255,0.04);
   font-weight: 800;
   font-size: 14px;
   color: #fff;
   backdrop-filter: blur(8px);
}
.trainer-pill .ic {
   width: 26px;
   height: 26px;
   border-radius: 50%;
   background: rgba(34,232,213,0.15);
   color: var(--cyan);
   display: flex;
   align-items: center;
   justify-content: center;
}
.trainer-pill .ic svg {
   width: 15px;
   height: 15px;
}
.trainer-pill b {
   color: var(--cyan);
}
/* ---------- Robot ---------- */
.bubbles-row {
   display: flex;
   justify-content: space-between;
   padding: 0 6px;
   margin-bottom: 6px;
}
.speech-bubble {
   width: 64px;
   height: 64px;
   border-radius: 50%;
   border: 2px solid var(--cyan);
   display: flex;
   align-items: center;
   justify-content: center;
   color: var(--cyan);
   font-size: 20px;
   font-weight: 900;
   box-shadow: 0 0 20px rgba(34,232,213,0.40);
   background: rgba(6,18,32,0.58);
   position: relative;
}
.speech-bubble::after {
   content: "";
   position: absolute;
   bottom: -11px;
   left: 16px;
   width: 14px;
   height: 14px;
   border-bottom: 2px solid var(--cyan);
   border-left: 2px solid var(--cyan);
   background: rgba(6,18,32,0.58);
   transform: rotate(-45deg);
}
.robot-wrap {
   display: flex;
   flex-direction: column;
   align-items: center;
   padding-top: 10px;
}
.robot {
   position: relative;
   width: 190px;
}
.robot-antenna {
   width: 4px;
   height: 24px;
   background: rgba(255,255,255,0.7);
   margin: 0 auto;
   border-radius: 2px;
}
.robot-antenna::after {
   content: "";
   display: block;
   width: 11px;
   height: 11px;
   border-radius: 50%;
   background: var(--cyan);
   box-shadow: 0 0 14px 4px rgba(34,232,213,0.75);
   margin: -4px auto 0;
}
.robot-head {
   width: 158px;
   height: 134px;
   margin: 6px auto 0;
   position: relative;
   background: linear-gradient(160deg, #f2fbfc, #c3dde3);
   border: 3px solid rgba(255,255,255,0.85);
   border-radius: 56% 56% 48% 48% / 62% 62% 38% 38%;
   box-shadow: 0 0 40px rgba(34,232,213,0.40), inset 0 -14px 22px rgba(0,0,0,0.10);
}
.robot-ear {
   position: absolute;
   top: 30px;
   width: 22px;
   height: 46px;
   border-radius: 12px;
   background: linear-gradient(160deg, #e7f3f5, #b7d3da);
   border: 3px solid rgba(255,255,255,0.85);
}
.robot-ear.l {
   left: -16px;
}
.robot-ear.r {
   right: -16px;
}
.robot-visor {
   position: absolute;
   left: 50%;
   top: 40px;
   transform: translateX(-50%);
   width: 114px;
   height: 56px;
   border-radius: 30px;
   background: #061019;
   display: flex;
   align-items: center;
   justify-content: center;
   gap: 20px;
   box-shadow: inset 0 0 18px rgba(34,232,213,0.15);
}
.robot-eye {
   width: 18px;
   height: 18px;
   border-radius: 50%;
   background: var(--cyan);
   box-shadow: 0 0 14px 5px rgba(34,232,213,0.75);
}
.robot-smile {
   position: absolute;
   left: 50%;
   bottom: 22px;
   transform: translateX(-50%);
   width: 30px;
   height: 14px;
   border-bottom: 4px solid var(--cyan);
   border-radius: 0 0 18px 18px;
}
.robot-body {
   width: 168px;
   height: 114px;
   margin: -8px auto 0;
   position: relative;
   background: linear-gradient(160deg, #eef6f8, #aecdd4);
   border: 3px solid rgba(255,255,255,0.85);
   border-radius: 46% 46% 42% 42% / 58% 58% 42% 42%;
}
.robot-core {
   position: absolute;
   left: 50%;
   top: 24px;
   transform: translateX(-50%) rotate(45deg);
   width: 26px;
   height: 26px;
   border-radius: 7px;
   background: #0a1b26;
   border: 2px solid var(--cyan);
   box-shadow: 0 0 16px 4px rgba(34,232,213,0.55);
}
.robot-glow {
   width: 230px;
   height: 40px;
   margin: -4px auto 0;
   border-radius: 50%;
   background: radial-gradient(ellipse at center, rgba(34,232,213,0.45), transparent 70%);
   filter: blur(2px);
}
/* ---------- Panels ---------- */
.panel {
   background: var(--panel);
   border: 1px solid rgba(34,232,213,0.35);
   border-radius: 22px;
   padding: 20px 22px;
   height: 100%;
   box-shadow: 0 18px 36px rgba(0,0,0,0.45);
   backdrop-filter: blur(10px);
   text-align: right;
   direction: rtl;
}
.panel-head {
   display: flex;
   align-items: center;
   gap: 10px;
   margin-bottom: 14px;
}
.panel-head .ic {
   width: 30px;
   height: 30px;
   border-radius: 9px;
   display: flex;
   align-items: center;
   justify-content: center;
   background: rgba(34,232,213,0.15);
   color: var(--cyan);
}
.panel-head .ic svg {
   width: 17px;
   height: 17px;
}
.panel-head .title {
   font-size: 19px;
   font-weight: 900;
   color: #fff;
}
.panel-text {
   color: #dff2f2;
   font-size: 15px;
   line-height: 1.9;
   font-weight: 600;
}
.panel-foot {
   margin-top: 16px;
}
.check-ic {
   width: 28px;
   height: 28px;
   border-radius: 50%;
   border: 1.5px solid var(--cyan);
   color: var(--cyan);
   display: flex;
   align-items: center;
   justify-content: center;
}
.check-ic svg {
   width: 15px;
   height: 15px;
}
/* Question form */
div[data-testid="stForm"] {
   background: var(--panel);
   border: 1px solid rgba(34,232,213,0.35);
   border-radius: 22px;
   padding: 20px 22px;
   box-shadow: 0 18px 36px rgba(0,0,0,0.45);
   backdrop-filter: blur(10px);
   text-align: right;
   direction: rtl;
}
.stTextArea textarea {
   background-color: rgba(4,14,26,0.9) !important;
   color: #fff !important;
   border: 1px solid rgba(34,232,213,0.40) !important;
   border-radius: 14px !important;
   min-height: 96px !important;
   direction: rtl !important;
   text-align: right !important;
   font-size: 14.5px !important;
   font-weight: 600 !important;
}
div[data-testid="stFormSubmitButton"] button,
div[data-testid="stButton"] button {
   background: linear-gradient(90deg, var(--cyan), var(--blue)) !important;
   color: #03121a !important;
   border: 0 !important;
   border-radius: 999px !important;
   font-weight: 900 !important;
   padding: 0.6rem 1.2rem !important;
   width: 100%;
   box-shadow: 0 10px 22px rgba(34,232,213,0.25);
   margin-top: 8px;
}
/* ---------- Sources ---------- */
.sources-panel {
   margin-top: 22px;
}
.source-desc {
   color: #dff2f2;
   font-size: 14px;
   line-height: 1.9;
   font-weight: 600;
   margin-bottom: 14px;
}
.source-chip {
   display: inline-block;
   margin: 5px 4px;
   padding: 8px 13px;
   border-radius: 999px;
   color: #fff;
   font-size: 13.5px;
   font-weight: 800;
   background: rgba(34,232,213,0.10);
   border: 1px solid rgba(34,232,213,0.30);
}
/* ---------- History ---------- */
.history {
   margin: 22px 0 6px;
}
.history-row {
   display: flex;
   margin-bottom: 10px;
}
.history-row.q {
   justify-content: flex-end;
}
.history-row.a {
   justify-content: flex-start;
}
.bubble {
   max-width: 70%;
   padding: 10px 16px;
   border-radius: 16px;
   font-size: 14px;
   line-height: 1.7;
   font-weight: 600;
}
.bubble.q {
   background: rgba(34,232,213,0.08);
   border: 1px solid rgba(34,232,213,0.30);
   color: #dffaf5;
}
.bubble.a {
   background: rgba(51,191,255,0.08);
   border: 1px solid rgba(51,191,255,0.30);
   color: #e6f6ff;
}
.clear-btn button {
   background: rgba(255,255,255,0.05) !important;
   color: #cfeeee !important;
   border: 1px solid rgba(255,255,255,0.20) !important;
   box-shadow: none !important;
}
.footer {
   text-align: center;
   color: var(--muted);
   font-size: 13px;
   margin-top: 22px;
}
@media (max-width: 900px) {
   .robot {
       width: 150px;
   }
   .main-title {
       font-size: 40px;
   }
   .logo-left img {
       width: 200px;
   }
}
</style>
"""
css = css.replace("PAGE_BACKGROUND_CSS", page_background_css)
st.markdown(css, unsafe_allow_html=True)

# =========================================================
# Header
# =========================================================
st.markdown(f"""
<div class="header-row">
<div class="logo-left">{logo_html}</div>
</div>
<div class="title-block">
<div class="main-title">المساعد الذكي</div>
<div class="sub-title">في قطاع النقل والخدمات اللوجستية</div>
<div class="brief">
       مساعد معرفي ذكي يحاكي بيئة بيانات مؤسسية لقطاع النقل والخدمات اللوجستية،
       ويدعم الاستفسارات حول المؤشرات، جودة البيانات، واتفاقيات مستوى الخدمة باستخدام RAG.
</div>
</div>
<div class="meta-row">
<span class="meta-label">أسماء الفريق:</span>
   {team_chips}
</div>
<div class="trainer-row">
<div class="trainer-pill">
<span class="ic">{ICON_PERSON}</span>
       المدرب: <b>أحمد عبدالفتاح</b>
</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# Main Layout
# الجواب يسار | الروبوت وسط | السؤال يمين
# =========================================================
col_question, col_robot, col_answer = st.columns([1, 1.15, 1])

with col_answer:
   st.markdown(f"""
<div class="panel" style="min-height: 300px;">
<div class="panel-head">
<span class="ic">{ICON_SPARKLE}</span>
<span class="title">إجابة المساعد</span>
</div>
<div class="panel-text">{answer_safe}</div>
<div class="panel-foot"><span class="check-ic">{ICON_CHECK}</span></div>
</div>
   """, unsafe_allow_html=True)

with col_robot:
   st.markdown("""
<div class="bubbles-row">
<div class="speech-bubble">•••</div>
<div class="speech-bubble">؟</div>
</div>
<div class="robot-wrap">
<div class="robot">
<div class="robot-antenna"></div>
<div class="robot-head">
<div class="robot-ear l"></div>
<div class="robot-ear r"></div>
<div class="robot-visor">
<div class="robot-eye"></div>
<div class="robot-eye"></div>
</div>
<div class="robot-smile"></div>
</div>
<div class="robot-body">
<div class="robot-core"></div>
</div>
</div>
<div class="robot-glow"></div>
</div>
   """, unsafe_allow_html=True)

with col_question:
   with st.form("question_form", clear_on_submit=True):
       st.markdown(f"""
<div class="panel-head">
<span class="ic">{ICON_CHAT}</span>
<span class="title">اسأل المساعد</span>
</div>
       """, unsafe_allow_html=True)
       question = st.text_area(
           "السؤال",
           placeholder="اكتبي سؤالك هنا...",
           label_visibility="collapsed",
           height=300
       )
       submitted = st.form_submit_button("➤ إرسال السؤال")
   if submitted:
       answer = get_answer(question)
       st.session_state.chat_history.append({
           "q": question.strip(),
           "a": answer
       })
       try:
           st.rerun()
       except Exception:
           st.experimental_rerun()

# =========================================================
# Sources Panel
# =========================================================
st.markdown(f"""
<div class="panel sources-panel">
<div class="panel-head">
<span class="ic">{ICON_DB}</span>
<span class="title">مصادر البيانات</span>
</div>
<div class="source-desc">
       يعتمد المشروع على بيانات تجريبية مولّدة لمحاكاة قطاع النقل والخدمات اللوجستية،
       مع كتالوج مؤشرات وقوالب SLA لاختبار سيناريوهات التحليل والاسترجاع الذكي.
</div>
<div>
       {source_chips}
</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# History
# =========================================================
if len(st.session_state.chat_history) > 1:
   rows = []
   for turn in st.session_state.chat_history[:-1]:
       q = html.escape(turn["q"])
       a = html.escape(turn["a"])
       rows.append(
           f'<div class="history-row q"><div class="bubble q">{q}</div></div>'
       )
       rows.append(
           f'<div class="history-row a"><div class="bubble a">{a}</div></div>'
       )
   st.markdown(f'<div class="history">{"".join(rows)}</div>', unsafe_allow_html=True)

# =========================================================
# Clear Button + Footer
# =========================================================
st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
st.button("مسح المحادثة", on_click=clear_chat)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown(
   '<div class="footer">مشروع المساعد الذكي لقطاع النقل والخدمات اللوجستية — أكاديمية سدايا</div>',
   unsafe_allow_html=True
)
