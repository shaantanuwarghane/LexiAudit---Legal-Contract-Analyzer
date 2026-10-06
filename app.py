import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from document_parser import extract_text_from_file
from risk_analyzer import audit_entire_contract

load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="LexiAudit AI - Contract Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern Custom CSS Styling ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Header Card */
    .hero-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: #FFFFFF;
        padding: 28px 32px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1);
    }
    .hero-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #F8FAFC;
        margin: 0;
    }
    .hero-sub {
        font-size: 15px;
        color: #94A3B8;
        margin-top: 6px;
    }

    /* KPI Metric Cards */
    .metric-card {
        background: #FFFFFF;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .metric-num {
        font-size: 26px;
        font-weight: 800;
    }
    .metric-label {
        font-size: 13px;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Risk Badges */
    .badge-high {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-med {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-low {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
    }

    /* Custom Cards */
    .clause-card {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Code block container */
    .stCodeBlock {
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Header Section ---
st.markdown("""
<div class="hero-card">
    <div class="hero-title">⚖️ LexiAudit AI — Contract Intelligence & Risk Redlining</div>
    <div class="hero-sub">Enterprise-grade legal contract auditing powered by Generative AI. Upload NDAs, MSAs, or Vendor Contracts for instant risk assessment.</div>
</div>
""", unsafe_allow_html=True)


# --- Sidebar ---
st.sidebar.markdown("### 🛠️ Configuration")
selected_model = os.getenv("LLM_MODEL", "gemini-3.5-flash")
st.sidebar.success(f"🤖 **Model Engine:** `{selected_model}`")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📌 Features
- ⚡ **1-Click Audit**: Single-pass full document reasoning.
- 🎯 **Risk Scoring**: High, Medium, Low breakdown per clause.
- ✍️ **Redline Generator**: Instant safer text suggestions.
- ⚠️ **Gap Detection**: Identifies missing legal clauses.
""")


# --- File Upload Section ---
uploaded_file = st.file_uploader("📂 Select or drag & drop a contract (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    # Save file to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    st.caption(f"📁 Loaded Document: **{uploaded_file.name}** ({round(len(uploaded_file.getvalue())/1024, 1)} KB)")

    if st.button("✨ Perform Legal Audit", type="primary", use_container_width=True):
        with st.spinner("🤖 Auditing contract structure, risk terms & compliance gaps..."):
            try:
                # Execute audit
                report = audit_entire_contract(tmp_file_path)
                st.session_state['report'] = report
                st.session_state['file_name'] = uploaded_file.name
                os.remove(tmp_file_path)
            except Exception as e:
                st.error(f"Audit Error: {str(e)}")


# --- Render Audit Results ---
if 'report' in st.session_state:
    report = st.session_state['report']
    file_name = st.session_state.get('file_name', 'Contract')

    # Count statistics for KPI Dashboard
    total_clauses = len(report.clauses_analysis)
    high_count = sum(1 for c in report.clauses_analysis if c.risk_score == "HIGH")
    med_count = sum(1 for c in report.clauses_analysis if c.risk_score == "MEDIUM")
    low_count = sum(1 for c in report.clauses_analysis if c.risk_score == "LOW")
    missing_count = len(report.missing_critical_clauses)

    st.markdown("---")

    # --- KPI Stats Banner ---
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#1E293B;">{total_clauses}</div>
            <div class="metric-label">Total Clauses</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#DC2626;">{high_count}</div>
            <div class="metric-label">🔴 High Risk</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#D97706;">{med_count}</div>
            <div class="metric-label">🟡 Medium Risk</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#16A34A;">{low_count}</div>
            <div class="metric-label">🟢 Low Risk</div>
        </div>
        """, unsafe_allow_html=True)

    with kpi5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-num" style="color:#2563EB;">{missing_count}</div>
            <div class="metric-label">⚠️ Gaps / Missing</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Tabbed Navigation ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive Summary",
        "🔍 Clause Redline Inspector",
        "⚠️ Missing Protections",
        "📥 Export Report"
    ])

    # --- TAB 1: EXECUTIVE SUMMARY ---
    with tab1:
        st.subheader("📋 Executive Risk Overview")
        
        if report.overall_risk_score == "HIGH":
            st.error("🔴 **OVERALL CONTRACT RATING: HIGH RISK** — Immediate redlining required before signing.")
        elif report.overall_risk_score == "MEDIUM":
            st.warning("🟡 **OVERALL CONTRACT RATING: MEDIUM RISK** — Moderate risks identified. Revision advised.")
        else:
            st.success("🟢 **OVERALL CONTRACT RATING: LOW RISK** — Standard terms. Safe to proceed.")

        st.markdown("#### **AI Analysis Summary:**")
        st.info(report.executive_summary)

    # --- TAB 2: CLAUSE REDLINE INSPECTOR ---
    with tab2:
        st.subheader("🔍 Clause-by-Clause Breakdown & Redlines")

        for idx, clause in enumerate(report.clauses_analysis, start=1):
            badge_class = "badge-high" if clause.risk_score == "HIGH" else "badge-med" if clause.risk_score == "MEDIUM" else "badge-low"
            badge_icon = "🔴" if clause.risk_score == "HIGH" else "🟡" if clause.risk_score == "MEDIUM" else "🟢"

            with st.expander(f"{badge_icon} **Clause {idx}: {clause.clause_title}** ({clause.clause_type})"):
                st.markdown(f"<span class='{badge_class}'>Risk Level: {clause.risk_score}</span>", unsafe_allow_html=True)
                st.markdown(f"**Legal Evaluation:**\n{clause.risk_explanation}")

                if clause.risk_score in ["HIGH", "MEDIUM"]:
                    st.markdown("#### ✍️ Recommended Redline Wording:")
                    st.code(clause.suggested_redline, language="text")

    # --- TAB 3: MISSING PROTECTIONS ---
    with tab3:
        st.subheader("⚠️ Missing Mandatory & Standard Legal Clauses")
        if report.missing_critical_clauses:
            for missing in report.missing_critical_clauses:
                st.markdown(f"""
                <div style="background:#FEF2F2; border-left: 4px solid #EF4444; padding: 12px 16px; border-radius: 6px; margin-bottom: 10px; color:#991B1B;">
                    <strong>❌ Missing Protection:</strong> {missing}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No critical standard clauses appear to be missing.")

    # --- TAB 4: EXPORT REPORT ---
    with tab4:
        st.subheader("📥 Export & Download Legal Audit Report")
        
        # Build Markdown Export string
        md_export = f"# Legal Audit Report — {file_name}\n"
        md_export += f"**Overall Rating:** {report.overall_risk_score}\n\n"
        md_export += f"## Executive Summary\n{report.executive_summary}\n\n"
        md_export += "## Clause Breakdown\n"
        
        for idx, c in enumerate(report.clauses_analysis, start=1):
            md_export += f"### Clause {idx}: {c.clause_title}\n"
            md_export += f"- **Category:** {c.clause_type}\n"
            md_export += f"- **Risk:** {c.risk_score}\n"
            md_export += f"- **Explanation:** {c.risk_explanation}\n"
            if c.risk_score in ["HIGH", "MEDIUM"]:
                md_export += f"- **Redline Suggestion:**\n```\n{c.suggested_redline}\n```\n"
            md_export += "\n"

        if report.missing_critical_clauses:
            md_export += "## Missing Clauses\n"
            for m in report.missing_critical_clauses:
                md_export += f"- {m}\n"

        st.download_button(
            label="📄 Download Full Audit Report (.md)",
            data=md_export,
            file_name=f"Legal_Audit_{file_name}.md",
            mime="text/markdown",
            type="primary"
        )