"""
ui/app.py  -  LexBot Streamlit UI
Run from inside legal-agent/:
    streamlit run ui/app.py
"""

import os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import streamlit as st

if "case_text" not in st.session_state:
    st.session_state.case_text = ""

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LexBot – Indian Law Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1529 50%, #0a0e1a 100%);
    color: #e2e8f0;
}

/* Header */
.lex-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.lex-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.lex-subtitle {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 0.4rem;
    letter-spacing: 0.05em;
}

/* Section cards */
.section-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    transition: border-color 0.3s ease;
}
.section-card:hover {
    border-color: rgba(246,211,101,0.3);
}
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #f6d365;
    margin: 0 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Input area */
.stTextArea textarea {
    background: #1e1e2f !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus {
    border-color: #f6d365 !important;
    box-shadow: 0 0 0 2px rgba(246,211,101,0.2) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #f6d365 0%, #fda085 100%) !important;
    color: #0a0e1a !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2.5rem !important;
    letter-spacing: 0.03em !important;
    transition: opacity 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.9 !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07101f 0%, #0f1d36 100%) !important;
    border-right: 1px solid rgba(246,211,101,0.18) !important;
    box-shadow: 0 0 0 1px rgba(246,211,101,0.05), 0 20px 60px rgba(0,0,0,0.35);
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
.sidebar-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(246,211,101,0.14);
    border-radius: 18px;
    padding: 1rem 1rem 1.1rem;
    margin: 1rem 0;
}
.sidebar-card h3 {
    color: #f6d365;
    margin: 0 0 0.65rem;
    font-size: 1.05rem;
}
.sidebar-card p,
.sidebar-card li {
    color: #d8e2ff;
    margin: 0.2rem 0;
    line-height: 1.5;
}
.sidebar-card li {
    padding-left: 0.8rem;
}

/* Metrics */
.metric-box {
    background: rgba(246,211,101,0.08);
    border: 1px solid rgba(246,211,101,0.2);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #f6d365;
}
.metric-label {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}

/* Law section pills */
.law-pill {
    display: inline-block;
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    color: #63b3ed;
    border-radius: 20px;
    padding: 0.25rem 0.8rem;
    font-size: 0.82rem;
    font-weight: 500;
    margin: 0.2rem;
}

/* Disclaimer box */
.disclaimer {
    background: rgba(245,101,101,0.08);
    border: 1px solid rgba(245,101,101,0.25);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #fc8181;
    font-size: 0.88rem;
    margin-top: 1rem;
}

/* Progress spinner overlay */
.analyzing-text {
    text-align: center;
    color: #f6d365;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 1rem;
}

/* Divider */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* Copy report button */
.copy-area {
    background: rgba(255,255,255,0.03);
    border: 1px dashed rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem;
    margin-top: 1rem;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# Bonus: Premium card UI effect
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def extract_text_from_file(uploaded_file) -> str:
    """Extract plain text from PDF, TXT, or DOCX uploaded file."""
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="replace")

    elif name.endswith(".pdf"):
        import pdfplumber, io
        text_parts = []
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_parts.append(t)
        return "\n".join(text_parts)

    elif name.endswith(".docx"):
        import docx, io
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    else:
        return ""


@st.cache_resource(show_spinner=False)
def load_retriever():
    """Load FAISS index once and cache."""
    from rag.retriever import retrieve_multi, retrieve
    from rag.vector_store import index_exists, load_index
    if not index_exists():
        return None, None
    idx, docs = load_index()
    return idx, docs


def run_pipeline(case_description: str):
    """Full 3-step pipeline: parse → retrieve → analyze."""
    from agents.parser_agent    import ParserAgent
    from agents.reasoning_agent import ReasoningAgent
    from rag.retriever          import retrieve_multi

    # Step 1: Parse
    parser = ParserAgent()
    parsed = parser.parse(case_description)

    # Step 2: RAG Retrieve
    rag_docs = retrieve_multi(parsed["search_queries"], k_each=5)

    # Step 3: Analyze
    reasoner = ReasoningAgent()
    report   = reasoner.analyze(case_description, rag_docs)

    return parsed, rag_docs, report


def section_card(icon: str, title: str, content: str):
    st.markdown(f"""
    <div class="section-card">
      <div class="section-title">{icon} {title}</div>
      {content}
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        "<div class='sidebar-card'>"
        "<h3>⚖️ LexBot</h3>"
        "<p><strong>Indian Law AI Agent</strong></p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ AI Settings")

    # 🔹 Model Selection
    model_option = st.selectbox(
        "Select Model",
        ["Groq (Cloud)", "Local (Ollama)"]
    )

    # 🔹 Groq API Key Input
    if model_option == "Groq (Cloud)":
        groq_key = st.text_input(
            "Enter Groq API Key",
            type="password",
            placeholder="gsk_..."
        )

        if groq_key:
            st.session_state["GROQ_API_KEY"] = groq_key
            st.success("✅ API Key Loaded")

    # 🔹 Clear Key Button
    if st.button("Clear API Key"):
        st.session_state.pop("GROQ_API_KEY", None)
        st.info("API Key removed")

    with st.expander("📘 How to get Groq API Key"):
        st.markdown("""
1. Go to https://console.groq.com  
2. Sign in  
3. Click **API Keys**  
4. Create new key  
5. Paste it here  

🔒 Your key is not stored anywhere.
""")

    # 🧠 USE THE SETTINGS IN BACKEND
    api_key = st.session_state.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    os.environ["CURRENT_MODEL_CHOICE"] = model_option
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key

    from rag.vector_store import index_exists
    index_ready = index_exists()
    
    st.markdown(
        "<div class='sidebar-card'>"
        "<h3>📊 System Status</h3>"
        f"<p>{'✅ Vector Index Ready' if index_ready else '❌ Vector Index Missing'}</p>"
        f"<p style='color:#94a3b8; font-size:0.9rem; margin-top:0.4rem;'>"
        f"{'Ready for analysis' if index_ready else 'Run: python main.py --build'}"
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='sidebar-card'>"
        "<h3>📚 Data Coverage</h3>"
        "<ul>"
        "<li>IPC: 575 sections</li>"
        "<li>CrPC: 525 sections</li>"
        "<li>CPC: 171 sections</li>"
        "</ul>"
        "</div>",
        unsafe_allow_html=True,
    )

    sample_cases = {
        "Theft Case": "Ram stole a mobile phone worth Rs. 15,000 from a shop by hiding it under his jacket and walking out without paying. He was caught by the shopkeeper at the exit.",
        "Murder Case": "Suresh attacked Mohan with a knife during a heated argument over property and caused his death. Witnesses saw the attack.",
        "Civil Dispute": "Vijay entered into a contract with Ravi to supply 500 kg of rice within 30 days. Ravi failed to deliver and refused to refund the advance payment of Rs. 50,000.",
        "Domestic Violence": "Priya was repeatedly beaten by her husband and in-laws for not bringing sufficient dowry. She has medical reports as evidence.",
    }
    selected_sample = st.selectbox("Choose a sample case:", ["-- Select --"] + list(sample_cases.keys()))
    if st.button("Load sample into input"):
        st.session_state.case_text = sample_cases[selected_sample] if selected_sample != "-- Select --" else ""
    if st.button("Clear case input"):
        st.session_state.case_text = ""

    st.markdown(
        "<div class='sidebar-card'>"
        "<h3>📌 About LexBot</h3>"
        "<p>Instant case analysis from IPC / CrPC / CPC content.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("Why use this AI law assistant?", expanded=False):
        st.write("Fast summary of facts")
        st.write("Relevant law retrieval")
        st.write("Arguments + outcome prediction")

    if st.button("Refresh Status"):
        st.experimental_rerun()


# ── Main Header ────────────────────────────────────────────────────────────────

st.markdown("""
<div class="lex-header">
  <h1 class="lex-title glow">⚖️ LexBot – Indian Law Agent</h1>
  <p class="lex-subtitle">AI-powered legal analysis across IPC • CrPC • CPC</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Center main content
st.markdown("<div style='max-width:900px; margin:auto;'>", unsafe_allow_html=True)

# ── Case Input ─────────────────────────────────────────────────────────────────

col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.markdown("### Describe Your Case")
    st.write("Paste or upload your legal case below")

    tab_type, tab_upload = st.tabs(["✏️  Type / Paste", "📂  Upload File  (PDF · DOCX · TXT)"])

    case_input = ""

    with tab_type:
        default_text = ""
        if selected_sample != "-- Select --":
            default_text = sample_cases[selected_sample]

        case_input_typed = st.text_area(
            label="Case Description",
            value=default_text,
            height=180,
            placeholder="Describe the facts of your case in detail...\n\nExample: Ram stole a mobile phone from a shop by hiding it under his jacket. He was caught at the exit by the shopkeeper...",
            label_visibility="collapsed",
            key="case_text",
        )
        case_input = case_input_typed

    with tab_upload:
        st.markdown(
            "<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:0.5rem'>"
            "Upload a case file — text will be extracted automatically."
            "</p>",
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload case document",
            type=["pdf", "txt", "docx"],
            label_visibility="collapsed",
            key="case_file",
        )
        if uploaded_file is not None:
            with st.spinner("Extracting text from file..."):
                extracted = extract_text_from_file(uploaded_file)
            if extracted.strip():
                st.success(f"Extracted {len(extracted)} characters from **{uploaded_file.name}**")
                st.markdown("**Preview (first 500 chars):**")
                st.code(extracted[:500] + ("..." if len(extracted) > 500 else ""), language=None)
                case_input = extracted   # use uploaded text for analysis
            else:
                st.error("Could not extract text from the file. Try a different format.")

    analyze_btn = st.button("⚖️  Analyze Case", use_container_width=True)

# ── Analysis ───────────────────────────────────────────────────────────────────

if analyze_btn:
    if not case_input.strip():
        st.warning("Please describe your case before analyzing.")
    else:
        from rag.vector_store import index_exists as _idx_exists
        if not _idx_exists():
            st.error("Vector index not found. Please run:  `python main.py --build`")
            st.stop()

        st.markdown("---")

        progress = st.progress(0)
        status = st.empty()
        status.text("🔍 Parsing case...")

        try:
            progress.progress(15)
            parser = __import__('agents.parser_agent', fromlist=['ParserAgent']).ParserAgent()
            parsed = parser.parse(case_input)
            status.success("✔ Case parsed")
            time.sleep(0.15)

            status.info("📚 Retrieving applicable laws...")
            progress.progress(40)
            retriever = __import__('rag.retriever', fromlist=['retrieve_multi']).retrieve_multi
            rag_docs = retriever(parsed['search_queries'], k_each=5)
            status.success("✔ Laws retrieved")
            time.sleep(0.15)

            status.info("🧠 Generating legal analysis...")
            progress.progress(70)
            reasoner = __import__('agents.reasoning_agent', fromlist=['ReasoningAgent']).ReasoningAgent()
            report = reasoner.analyze(case_input, rag_docs)
            status.success("✔ Analysis generated")
            time.sleep(0.15)

            status.info("✨ Finalizing report...")
            progress.progress(95)
            time.sleep(0.2)
            progress.progress(100)
            status.success("✅ Analysis complete")
            time.sleep(0.1)
        except Exception as e:
            st.error(f"Error during analysis: {e}")
            st.stop()

        # ── Row: Quick Metrics ────────────────────────────────────────────────
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-value">{parsed['case_type']}</div>
              <div class="metric-label">Case Type</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-value">{len(rag_docs)}</div>
              <div class="metric-label">Laws Retrieved</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            ipc_count  = sum(1 for d in rag_docs if d["source"] == "IPC")
            crpc_count = sum(1 for d in rag_docs if d["source"] == "CrPC")
            cpc_count  = sum(1 for d in rag_docs if d["source"] == "CPC")
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-value">IPC:{ipc_count} CrPC:{crpc_count} CPC:{cpc_count}</div>
              <div class="metric-label">By Act</div>
            </div>""", unsafe_allow_html=True)
        with m4:
            top_score = max((d["score"] for d in rag_docs), default=0)
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-value">{top_score:.0%}</div>
              <div class="metric-label">Top Relevance</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Retrieved Sections Pills ──────────────────────────────────────────
        with st.expander("📚 Retrieved Legal Sections", expanded=False):
            pills_html = " ".join(
                f'<span class="law-pill">{d["source"]} §{d["section"]} – {d["title"][:35]}</span>'
                for d in rag_docs
            )
            st.markdown(f'<div style="padding:0.5rem">{pills_html}</div>', unsafe_allow_html=True)

        # ── Parse Info ────────────────────────────────────────────────────────
        with st.expander("🔍 Case Parse Details", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**Petitioner:** {parsed['petitioner']}")
                st.markdown(f"**Respondent:** {parsed['respondent']}")
            with c2:
                st.markdown(f"**Primary Issue:** {parsed['primary_issue']}")
            st.markdown("**Search Queries Used:**")
            for q in parsed["search_queries"]:
                st.markdown(f"  - {q}")

        # ── Full 11-Section Report ────────────────────────────────────────────
        st.markdown("---")
        st.markdown("## Legal Analysis Report")

        # Split the markdown report by sections and render
        sections = {
            "1. CASE SUMMARY":              ("📄", "Case Summary"),
            "2. LEGAL CLASSIFICATION":      ("⚖️", "Legal Classification"),
            "3. APPLICABLE LAWS":           ("📚", "Applicable Laws (from RAG)"),
            "4. LEGAL ANALYSIS":            ("🧠", "Legal Analysis"),
            "5. ARGUMENTS":                 ("🧑‍⚖️", "Arguments"),
            "6. OPPOSITION STRATEGY":       ("🎯", "Opposition Strategy"),
            "7. CROSS EXAMINATION":         ("❓", "Cross Examination Questions"),
            "8. RISK ANALYSIS":             ("📊", "Risk Analysis"),
            "9. CASE COMPLEXITY":           ("💰", "Case Complexity & Estimated Fees"),
            "10. OUTCOME PREDICTION":       ("📈", "Outcome Prediction"),
            "11. VALIDATION":               ("⚠️", "Validation & Disclaimer"),
        }

        # Display the full report in a styled container
        report_lines = report.split("\n")
        current_section = []
        current_key     = None

        def flush_section(key, lines):
            if not key or not lines:
                return
            icon, human_title = sections.get(key, ("📌", key))
            content_md = "\n".join(lines).strip()
            with st.container():
                st.markdown(f"""
                <div class="section-card">
                  <div class="section-title">{icon} {human_title}</div>
                </div>""", unsafe_allow_html=True)
                st.markdown(content_md)
                st.markdown("<br>", unsafe_allow_html=True)

        for line in report_lines:
            matched = None
            stripped = line.strip("# ").strip()
            for sec_key in sections:
                if sec_key.lower() in stripped.lower():
                    matched = sec_key
                    break

            if matched:
                flush_section(current_key, current_section)
                current_key     = matched
                current_section = []
            else:
                current_section.append(line)

        flush_section(current_key, current_section)

        # ── Download Report ───────────────────────────────────────────────────
        st.markdown("---")
        dl_col1, dl_col2 = st.columns([3, 1])
        with dl_col1:
            st.markdown("### Download Report")
        with dl_col2:
            st.download_button(
                label="📥 Download as Markdown",
                data=report,
                file_name="legal_analysis_report.md",
                mime="text/markdown",
                use_container_width=True,
            )

        # ── Disclaimer ────────────────────────────────────────────────────────
        st.markdown("""
        <div class="disclaimer">
          <strong>⚠️ Important Disclaimer</strong><br>
          This analysis is generated by an AI system for informational purposes only.
          It is based on retrieved sections from IPC, CrPC, and CPC databases via RAG.
          This does <strong>NOT</strong> constitute formal legal advice.
          Please consult a qualified advocate before taking any legal action.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

else:
    # ── Landing state ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    features = [
        ("📄", "Case Summary", "Extracts facts, key events, and parties involved"),
        ("📚", "RAG-Powered Laws", "Retrieves exact IPC/CrPC/CPC sections from 1,271 laws"),
        ("🧠", "Legal Analysis", "Applies retrieved laws to your specific case facts"),
        ("🧑‍⚖️", "Arguments", "Generates arguments for both sides of the case"),
        ("📈", "Outcome Prediction", "Estimates probability of success with reasoning"),
        ("💰", "Fee Estimation", "Estimates complexity, hearings, and legal costs"),
    ]
    cols = [c1, c2, c3, c1, c2, c3]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="section-card" style="text-align:center; padding:1.5rem 1rem;">
              <div style="font-size:2rem">{icon}</div>
              <div style="font-weight:600; color:#f6d365; margin:0.5rem 0">{title}</div>
              <div style="color:#94a3b8; font-size:0.88rem">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
