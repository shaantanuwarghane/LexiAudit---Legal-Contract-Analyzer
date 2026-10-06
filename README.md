# ⚖️ LexiAudit AI — Legal Contract Risk Analyzer & Compliance Auditor
**LexiAudit AI** is an intelligent, domain-specific AI application that automatically parses legal contracts (NDAs, MSAs, Vendor Agreements), evaluates clause-by-clause risks, generates safer redline text recommendations, and detects missing mandatory legal protections using Google Gemini LLM and LangChain.
---
## 🌟 Key Features
* **⚡ Single-Pass Batch Audit**: Uses structured Pydantic schemas to evaluate an entire contract in **1 single API call**, saving token quota and execution time.
* **🔍 Clause-by-Clause Risk Analysis**: Categorizes each clause and assigns a color-coded risk rating (**🔴 HIGH**, **🟡 MEDIUM**, **🟢 LOW**).
* **✍️ Automated Redline Generator**: Suggests precise, client-protective replacement text for high-risk or aggressive clauses.
* **⚠️ Compliance Gap Detection**: Identifies critical standard clauses missing from the agreement (e.g., *Equitable Relief*, *Severability*, *Exceptions to Confidentiality*).
* **🎨 Modern SaaS Web Dashboard**: Built with Streamlit, featuring real-time KPI metrics, dark mode header styling, tabbed navigation, and 1-click Markdown export.
* **📄 Multi-Format Document Reader**: Supports `.pdf`, `.docx`, and `.txt` contract uploads.
---
## 🏗️ Project Architecture
```text
                       ┌───────────────────────────────┐
                       │  Uploaded Document (.pdf/docx)│
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │   document_parser.py          │
                       │ (Extracts text & splits into  │
                       │  logical clause blocks)       │
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │   risk_analyzer.py            │
                       │ (Gemini AI + Pydantic Schema  │
                       │  1 API Call Structured Audit) │
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │   app.py (Streamlit Web UI)   │
                       │ (KPI Stats, Tabbed Inspector, │
                       │  Redlines, Markdown Export)   │
                       └───────────────┴───────────────┘

  

  
📁 Repository Structure

  
text
legal-contract-analyzer/
│
├── app.py                # Streamlit Web UI Dashboard
├── risk_analyzer.py      # Core LLM Risk Audit Engine (LangChain + Pydantic)
├── document_parser.py    # Document text extraction (PDF/DOCX/TXT) & Regex Splitter
├── list_models.py        # Diagnostic script to list available Gemini models
├── sample_contract.txt   # Sample contract file for testing
├── .env                  # API keys and environment variables
├── README.md             # Project documentation
└── venv/                 # Python Virtual Environment

  

  
🛠️ Tech Stack & Dependencies

  

  
Language: Python 3.10+

  
LLM Engine: Google Gemini (gemini-3.5-flash / gemini-2.0-flash) via langchain-google-genai

  
Structured Output: Pydantic

  
Web UI Framework: Streamlit

  
Document Parsing: pdfplumber, python-docx

  
Environment Management: python-dotenv

  

  

  
🚀 Quick Start & Installation

  
1. Prerequisites

  

Ensure you have Python 3.10+ installed and a free Gemini API key from Google AI Studio
.


  
2. Clone / Setup Project Folder

  
bash
git clone https://github.com/your-username/legal-contract-analyzer.git
cd legal-contract-analyzer

  
3. Create & Activate Virtual Environment

  
bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
# macOS/Linux
python -m venv venv
source venv/bin/activate

  
4. Install Dependencies

  
bash
pip install langchain langchain-google-genai pydantic pdfplumber python-docx streamlit python-dotenv

  
5. Configure Environment Variables

  

Create a .env file in the root directory:


  
env
GEMINI_API_KEY=your_actual_gemini_api_key_here
LLM_MODEL=gemini-3.5-flash

  

  
💻 Usage

  
Option A: Run via Terminal CLI

  

To test the analysis engine directly in your terminal:


  
bash
python risk_analyzer.py

  
Option B: Launch the Interactive Web Dashboard

  

To launch the full Streamlit Web UI:


  
bash
streamlit run app.py

  

Open your browser at http://localhost:8501.


  

  
📋 Sample Audit Output

  
text
=================================================================
 ⚖️  LEGAL AUDIT REPORT  |  Overall Rating: 🔴 HIGH RISK
=================================================================
📋 Executive Summary:
This Mutual NDA contains severe risks, notably a $100 liability cap rendering 
the agreement practically unenforceable. It also lacks standard confidentiality 
exceptions and includes an unusual indemnification clause.
-----------------------------------------------------------------
🔍 CLAUSE-BY-CLAUSE RISK BREAKDOWN
-----------------------------------------------------------------
[Clause 3] 3. LIMITATION OF LIABILITY
  • Category:     Limitation of Liability
  • Risk Level:   🔴 HIGH
  • Explanation:  $100 liability cap makes the contract toothless for data leaks.
  • ✍️ Redline Recommendation:
    THE TOTAL AGGREGATE LIABILITY OF EITHER PARTY SHALL NOT EXCEED $1,000,000, 
    EXCEPT THAT THERE SHALL BE NO CAP ON LIABILITY FOR BREACHES OF CONFIDENTIALITY.
-----------------------------------------------------------------
⚠️ MISSING MANDATORY / STANDARD CLAUSES
-----------------------------------------------------------------
  ❌ Exceptions to Confidentiality
  ❌ Equitable Relief / Injunctive Relief
  ❌ Return or Destruction of Confidential Information

  

  
🛡️ Legal Disclaimer

  

LexiAudit AI is an AI-assisted tool built for informational and educational contract review purposes only. It does not constitute formal legal advice. Always consult a qualified attorney for legal contract negotiations.
