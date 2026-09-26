import requests
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Velloe Enterprise AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background: #f6f8fb;
        color: #172033;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    /* ==============================
       SIDEBAR
    ============================== */

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: #9ca3af !important;
    }

    .sidebar-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }

    .sidebar-section {
        color: #9ca3af;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 1.6rem;
        margin-bottom: 0.7rem;
    }

    .system-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0.55rem 0;
        color: #e5e7eb;
        font-size: 0.9rem;
    }

    .green-dot {
        width: 7px;
        height: 7px;
        background: #22c55e;
        border-radius: 50%;
        display: inline-block;
    }

    .blue-dot {
        width: 7px;
        height: 7px;
        background: #60a5fa;
        border-radius: 50%;
        display: inline-block;
    }

    /* ==============================
       HERO
    ============================== */

    .hero {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 2.2rem;
    }

    .brand-title {
        font-size: 2rem;
        font-weight: 750;
        letter-spacing: -0.03em;
        color: #111827;
        line-height: 1.1;
    }

    .brand-subtitle {
        margin-top: 0.45rem;
        font-size: 0.95rem;
        color: #6b7280;
    }

    .online-badge {
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        border-radius: 999px;
        padding: 0.4rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 700;
        white-space: nowrap;
    }

    /* ==============================
       QUERY AREA
    ============================== */

    .query-title {
        font-size: 1.45rem;
        font-weight: 750;
        color: #111827;
        margin-bottom: 0.3rem;
    }

    .query-subtitle {
        color: #6b7280;
        font-size: 0.92rem;
        margin-bottom: 1rem;
    }

    /* Text area */

    textarea {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        line-height: 1.5 !important;
    }

    textarea::placeholder {
        color: #9ca3af !important;
        opacity: 1 !important;
    }

    textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }

    /* Button */

    div.stButton > button {
        background: #ff4b4b;
        color: white;
        border: none;
        border-radius: 9px;
        padding: 0.65rem 1.15rem;
        font-size: 0.9rem;
        font-weight: 700;
        transition: 0.15s ease;
    }

    div.stButton > button:hover {
        background: #e63e3e;
        color: white;
        border: none;
    }

    /* ==============================
   ANSWER
============================== */

.answer-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    margin-top: 2rem;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
}

.answer-label {
    color: #6b7280;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

.answer-card p {
    color: #111827;
    font-size: 1rem;
    line-height: 1.7;
}

.status {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
    font-size: 0.72rem;
    font-weight: 700;
}

/* ==============================
   EVIDENCE
============================== */

.evidence-section {
    margin-top: 2rem;
}

.evidence-title {
    font-size: 1rem;
    font-weight: 750;
    color: #111827;
    margin-bottom: 0.8rem;
}

.evidence-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.7rem;
}

.evidence-source {
    color: #374151;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.45rem;
}

.evidence-text {
    color: #4b5563;
    font-size: 0.86rem;
    line-height: 1.55;
}

    
    /* ==============================
       RETRIEVAL DETAILS
    ============================== */

    .retrieval-step {
        color: #4b5563;
        font-size: 0.88rem;
        padding: 0.25rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Velloe Enterprise AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### Access")

    user_role = st.selectbox(
        "User role",
        ["clinician", "admin"],
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">System</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="system-row">
            <span class="green-dot"></span>
            Knowledge Base Connected
        </div>

        <div class="system-row">
            <span class="green-dot"></span>
            Qdrant Retrieval
        </div>

        <div class="system-row">
            <span class="green-dot"></span>
            Gemini Generation
        </div>

        <div class="system-row">
            <span class="blue-dot"></span>
            Role-based Access
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption("Enterprise Knowledge Assistant")
    st.caption("Grounded answers from approved documentation.")


# =========================================================
# HERO
# =========================================================

hero_left, hero_right = st.columns([5, 1])

with hero_left:
    st.markdown(
        """
        <div style="font-size: 2rem; font-weight: 750; color: #111827;">
            Velloe Enterprise AI
        </div>
        <div style="font-size: 0.95rem; color: #6b7280; margin-top: 6px;">
            Healthcare Knowledge Assistant · Grounded Enterprise Search
        </div>
        """,
        unsafe_allow_html=True,
    )

with hero_right:
    st.markdown(
        """
        <div style="
            background:#ecfdf5;
            color:#047857;
            border:1px solid #a7f3d0;
            border-radius:999px;
            padding:7px 12px;
            text-align:center;
            font-size:12px;
            font-weight:700;
            margin-top:8px;
        ">
            ● SYSTEM ONLINE
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# =========================================================
# QUERY
# =========================================================

st.markdown(
    '<div class="query-title">Ask your enterprise knowledge base</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="query-subtitle">'
    'Search approved enterprise documentation and receive evidence-grounded answers.'
    '</div>',
    unsafe_allow_html=True,
)

query = st.text_area(
    "Question",
    placeholder=(
        "Example: What is the recommended dose for Drug-A "
        "for an adult weighing 50-80kg?"
    ),
    height=120,
    label_visibility="collapsed",
)

ask = st.button(
    "Ask Knowledge Base  →",
    type="primary",
)

# =========================================================
# BACKEND REQUEST
# =========================================================

if ask:

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Searching enterprise knowledge..."):

        try:

            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={
                    "q": query,
                    "thread_id": "streamlit-demo",
                },
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

        except requests.exceptions.RequestException as e:

            st.error(
                f"Unable to connect to the backend: {e}"
            )

            st.stop()

    # =====================================================
    # ANSWER
    # =====================================================

    st.markdown(
        '<div class="answer-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="answer-label">Answer</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        data.get(
            "answer",
            "No answer returned."
        )
    )

    st.markdown(
        f'<span class="status">● {data.get("status", "Completed")}</span>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True,
    )

    # =====================================================
    # EVIDENCE
    # =====================================================

    sources = data.get("sources", [])

    if sources:

        st.markdown(
            '<div class="section-title">Evidence</div>',
            unsafe_allow_html=True,
        )

        for source in sources:

            st.markdown(
                f"""
                <div class="evidence-card">

                    <div class="evidence-source">
                        Enterprise Knowledge
                    </div>

                    <div class="evidence-text">
                        {source}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    # =====================================================
    # RETRIEVAL DETAILS
    # =====================================================

    thought_process = data.get("thought_process", [])

    if thought_process:

        with st.expander("Retrieval details"):

            for step in thought_process:

                st.markdown(
                    f'<div class="retrieval-step">✓ {step}</div>',
                    unsafe_allow_html=True,
                )