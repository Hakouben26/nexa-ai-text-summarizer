
import streamlit as st
import html

from summarizer import summarize_text
from pdf_reader import extract_text_from_pdf


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Nexa AI | Text Summarizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- SESSION STATE ----------------

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "original_text" not in st.session_state:
    st.session_state.original_text = ""

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "pdf_info" not in st.session_state:
    st.session_state.pdf_info = None


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1020;
    color: #f1f5f9;
}

[data-testid="stSidebar"] {
    background: #11182b;
    border-right: 1px solid #25304a;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    padding: 35px;
    border-radius: 20px;
    background: linear-gradient(120deg, #172554, #312e81, #581c87);
    border: 1px solid #4338ca;
    margin-bottom: 28px;
}

.hero h1 {
    color: white;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: #dbeafe;
    font-size: 16px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 12px;
}

.info-card {
    background: #151f35;
    border: 1px solid #293957;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

.metric-card {
    background: #151f35;
    border: 1px solid #293957;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}

.metric-value {
    font-size: 27px;
    font-weight: 800;
    color: #a78bfa;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
    margin-top: 5px;
}

.stTextArea textarea {
    background: #111a2e !important;
    color: #f8fafc !important;
    border: 1px solid #344563 !important;
    border-radius: 12px !important;
    font-size: 15px !important;
}

.stTextArea textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 1px #8b5cf6 !important;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #9333ea);
    color: white;
    border: none;
    border-radius: 10px;
    height: 48px;
    font-weight: 700;
    width: 100%;
    transition: 0.2s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #4f46e5, #7e22ce);
    border: none;
    color: white;
}

.result-box {
    background: #151f35;
    border: 1px solid #344563;
    border-left: 4px solid #8b5cf6;
    border-radius: 12px;
    padding: 22px;
    color: #e2e8f0;
    line-height: 1.8;
    font-size: 15px;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 30px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## ✨ Nexa AI")

    st.caption("INTELLIGENT TEXT TOOLS")

    st.divider()

    st.markdown("### ⚙️ Settings")

    summary_length = st.selectbox(
        "Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    language = st.selectbox(
        "Output Language",
        ["Same as original", "English", "Arabic", "French"]
    )

    st.divider()

    st.markdown("### 🚀 About")

    st.write(
        "Nexa AI uses advanced artificial intelligence "
        "to transform long texts and PDF documents "
        "into clear and meaningful summaries."
    )

    st.caption("Powered by Groq AI")

    st.divider()

    st.caption("Version 1.1.0")


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>✨ AI Text Summarizer</h1>
    <p>
        Transform long documents into clear, concise and
        meaningful summaries with artificial intelligence.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- MAIN CONTENT ----------------

left, right = st.columns([1, 1], gap="large")


# ---------------- LEFT COLUMN ----------------

with left:

    st.markdown(
        '<div class="section-title">📄 Upload PDF or Enter Text</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload your PDF document",
        type=["pdf"],
        help="Upload a text-based PDF document."
    )

    if uploaded_file is not None:

        if st.button("📥 Extract PDF Text"):

            try:

                with st.spinner("Reading PDF document..."):

                    uploaded_file.seek(0)

                    pdf_result = extract_text_from_pdf(uploaded_file)

                    st.session_state.input_text = pdf_result["text"]

                    st.session_state.pdf_info = {
                        "name": uploaded_file.name,
                        "pages": pdf_result["pages"],
                        "words": pdf_result["words"],
                        "characters": pdf_result["characters"]
                    }

                    st.session_state.summary = ""
                    st.session_state.original_text = ""

                st.success("PDF text extracted successfully!")

            except Exception as e:

                st.error(f"PDF extraction failed: {e}")

    # PDF information

    if st.session_state.pdf_info:

        pdf = st.session_state.pdf_info

        st.markdown(f"""
        <div class="info-card">
            <strong>📄 {html.escape(pdf["name"])}</strong>
            <p style="color:#94a3b8; margin-bottom:0;">
                Pages: {pdf["pages"]} |
                Words: {pdf["words"]} |
                Characters: {pdf["characters"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📝 Your Text</div>',
        unsafe_allow_html=True
    )

    input_text = st.text_area(
        "Text input",
        height=310,
        placeholder=(
            "Paste your text here...\n\n"
            "Or upload a PDF document above."
        ),
        label_visibility="collapsed",
        key="input_text"
    )

    word_count = len(input_text.split())

    st.caption(f"📄 {word_count} words")

    generate = st.button(
        "✨ Generate Summary",
        use_container_width=True
    )


# ---------------- RIGHT COLUMN ----------------

with right:

    st.markdown(
        '<div class="section-title">🧠 AI Summary</div>',
        unsafe_allow_html=True
    )

    if st.session_state.summary:

        safe_summary = html.escape(st.session_state.summary)

        st.markdown(
            f'<div class="result-box">{safe_summary}</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown("""
        <div class="info-card" style="height:310px;
        display:flex; flex-direction:column;
        justify-content:center; text-align:center;">
            <div style="font-size:45px;">✨</div>
            <h3 style="color:#e2e8f0;">Your summary will appear here</h3>
            <p style="color:#94a3b8;">
                Enter your text or upload a PDF and click
                Generate Summary to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ---------------- GENERATE SUMMARY ----------------

if generate:

    if not input_text.strip():

        st.warning("Please enter some text or upload a PDF first.")

    else:

        try:

            with st.spinner("🤖 AI is analyzing your document..."):

                result = summarize_text(
                    input_text,
                    summary_length,
                    language
                )

                st.session_state.summary = result
                st.session_state.original_text = input_text

            st.success("Summary generated successfully!")

            st.rerun()

        except Exception as e:

            st.error(f"Something went wrong: {e}")


# ---------------- STATISTICS ----------------

if st.session_state.summary:

    original_words = len(
        st.session_state.original_text.split()
    )

    summary_words = len(
        st.session_state.summary.split()
    )

    reduction = (
        (original_words - summary_words) / original_words * 100
        if original_words > 0 else 0
    )

    st.markdown("---")

    st.markdown("### 📊 Summary Statistics")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{original_words}</div>
            <div class="metric-label">Original Words</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary_words}</div>
            <div class="metric-label">Summary Words</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{reduction:.1f}%</div>
            <div class="metric-label">Word Reduction</div>
        </div>
        """, unsafe_allow_html=True)

    st.download_button(
        label="⬇️ Download Summary",
        data=st.session_state.summary,
        file_name="Nexa_AI_Summary.txt",
        mime="text/plain"
    )


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    Nexa AI · Intelligent Text Summarization · Powered by Groq
</div>
""", unsafe_allow_html=True)
