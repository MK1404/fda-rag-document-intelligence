import re
import streamlit as st
from openai import OpenAI
from pinecone import Pinecone


# =====================
# 🔐 Secrets
# =====================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])

INDEX_NAME = "fda483-rag-v1-clean"
index = pc.Index(INDEX_NAME)


# =====================
# 🎨 UI Styling
# =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #f8fafc, #eef2ff);
}

.main-title {
    font-size: 36px;
    font-weight: 700;
    color: #0f172a;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}

.metric {
    font-size: 34px;
    font-weight: 700;
    color: #2563eb;
}

.stButton>button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    font-weight: 600;
}

section[data-testid="stSidebar"] {
    background: #f1f5f9;
}
</style>
""", unsafe_allow_html=True)


# =====================
# 🧠 Core helpers
# =====================
def get_embedding(text):
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=text.replace("\n", " ")
    ).data[0].embedding


def trim_context(txt, max_chars=150000):
    return txt[:max_chars]


# =====================
# 📂 Load all PDFs
# =====================
@st.cache_data(show_spinner=False)
def load_all_pdfs():
    emb = get_embedding("list pdfs")
    res = index.query(vector=emb, top_k=5000, include_metadata=True)

    pdfs = set()
    for m in res["matches"]:
        src = m["metadata"].get("source")
        if src:
            pdfs.add(src)

    return sorted(pdfs)


ALL_PDFS = load_all_pdfs()


# =====================
# 📊 Stats
# =====================
@st.cache_data(show_spinner=False)
def get_stats():
    stats = index.describe_index_stats()
    return len(ALL_PDFS), stats["total_vector_count"]


# =====================
# 🔍 Retrieval
# =====================
def retrieve_context(question, pdf_filter=None, top_k=40):
    emb = get_embedding(question)

    if pdf_filter and pdf_filter != "All PDFs":
        res = index.query(
            vector=emb,
            top_k=top_k,
            include_metadata=True,
            filter={"source": {"$eq": pdf_filter}}
        )
    else:
        res = index.query(
            vector=emb,
            top_k=top_k,
            include_metadata=True
        )

    return trim_context("\n\n".join(
        m["metadata"]["text"] for m in res["matches"]
    ))


SYSTEM_PROMPT = """
You are a senior FDA Quality, Compliance, and R&D subject matter expert.

Your role:
- Analyze FDA 483 reports, inspection findings, CAPA details, and quality documentation
- Provide precise, factual, and compliance-focused answers
- Maintain regulatory language and professional tone

STRICT RULES:
1. Use ONLY the provided document context
2. Never use outside knowledge or assumptions
3. If information is missing, respond exactly:
   "Not found in the provided PDFs."
4. Preserve original wording when listing observations or findings
5. Do NOT summarize unless explicitly asked
6. When steps, causes, or issues exist, present them in clear numbered or bullet format
7. Do not combine data from unrelated sections incorrectly

Output Style:
- Structured
- Clear compliance language
- Fully detailed
- No hallucination

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

def rag_bot(question, pdf_choice):
    context = retrieve_context(question, pdf_choice)

    if not context.strip():
        return "Not found in the provided PDFs."

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"}
        ]
    )

    return res.choices[0].message.content


# =====================
# 📂 SIDEBAR (FIRST)
# =====================
st.sidebar.title("📁 Document Filter")

pdf_choice = st.sidebar.selectbox(
    "Choose document source",
    ["All PDFs"] + ALL_PDFS,
    index=0
)

st.sidebar.caption("Default searches across all PDFs")


# =====================
# 🌐 MAIN UI
# =====================

st.markdown('<div class="main-title">📑 FDA Document Intelligence AI</div>', unsafe_allow_html=True)
st.write("AI-powered Quality & Compliance Assistant")

pdf_count, chunk_count = get_stats()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <div>Total PDFs</div>
        <div class="metric">{pdf_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div>Knowledge Chunks</div>
        <div class="metric">{chunk_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

question = st.text_input(
    "Ask FDA quality or compliance question:",
    placeholder="Example: List all observations for a site"
)

if st.button("🔍 Analyze Documents") and question:
    with st.spinner("Analyzing FDA documents..."):
        answer = rag_bot(question, pdf_choice)

    st.markdown("### 📋 AI Response")
    st.markdown(answer)
