import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
# Note: If using OpenAI: from langchain_openai import ChatOpenAI

from document_parser import extract_text_from_file

# Load API key from .env file
load_dotenv()


# 1. Schema for an individual clause analysis
class ClauseAnalysis(BaseModel):
    clause_title: str = Field(description="Title or heading of the contract clause")
    clause_type: str = Field(description="Category (e.g., Limitation of Liability, Indemnification, Termination, Confidentiality, Governing Law, Other)")
    risk_score: str = Field(description="Risk level: 'HIGH', 'MEDIUM', or 'LOW'")
    risk_explanation: str = Field(description="Concise legal analysis of risks, unfair burdens, or liabilities in this clause")
    suggested_redline: str = Field(description="Recommended revised clause text to protect our client. Return 'No changes needed' if risk is LOW.")


# 2. Top-level Schema for the ENTIRE Contract Report (Single API Call Container)
class ContractAuditReport(BaseModel):
    overall_risk_score: str = Field(description="Overall risk level for the entire contract: 'HIGH', 'MEDIUM', or 'LOW'")
    executive_summary: str = Field(description="Brief 2-3 sentence executive summary of the contract's risk profile")
    clauses_analysis: list[ClauseAnalysis] = Field(description="Detailed analysis for every clause identified in the contract")
    missing_critical_clauses: list[str] = Field(description="List of standard/mandatory clauses that are missing from this contract (e.g. Confidentiality Exceptions, Severability, Assignment)")


# 3. Batch Audit Function (1 API Call)
def audit_entire_contract(file_path: str) -> ContractAuditReport:
    """Extracts contract text and audits the ENTIRE document in 1 single Gemini API call."""
    print(f"\n📑 Extracting contract text from: {file_path}...")
    contract_text = extract_text_from_file(file_path)

    # Initialize Gemini model (Using gemini-2.5-flash or your configured Gemini model)
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1
    )
    # For OpenAI:
    # llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.1)

    # Force LLM to structure response as ContractAuditReport
    structured_llm = llm.with_structured_output(ContractAuditReport)

    prompt = f"""You are a senior corporate attorney auditing a contract on behalf of our client.
Read the entire contract below, break it down clause-by-clause, and evaluate it for legal risks, one-sided terms, extreme caps, or missing standard protections.

--- CONTRACT TEXT START ---
{contract_text}
--- CONTRACT TEXT END ---

Perform a complete legal audit and populate all fields in the required schema.
"""
    print("🤖 Sending entire contract to Gemini for audit (1 API Call)...")
    return structured_llm.invoke(prompt)


# 4. Main Runner & Report Renderer
if __name__ == "__main__":
    report = audit_entire_contract("sample_contract.txt")

    # Format Overall Badge
    overall_badge = "🔴 HIGH RISK" if report.overall_risk_score == "HIGH" else "🟡 MEDIUM RISK" if report.overall_risk_score == "MEDIUM" else "🟢 LOW RISK"

    print("\n" + "="*65)
    print(f" ⚖️  LEGAL AUDIT REPORT  |  Overall Rating: {overall_badge}")
    print("="*65)
    print(f"\n📋 Executive Summary:\n{report.executive_summary}\n")

    print("-" * 65)
    print("🔍 CLAUSE-BY-CLAUSE RISK BREAKDOWN")
    print("-" * 65)

    for idx, c in enumerate(report.clauses_analysis, start=1):
        badge = "🔴 HIGH" if c.risk_score == "HIGH" else "🟡 MEDIUM" if c.risk_score == "MEDIUM" else "🟢 LOW"
        print(f"\n[Clause {idx}] {c.clause_title}")
        print(f"  • Category:     {c.clause_type}")
        print(f"  • Risk Level:   {badge}")
        print(f"  • Explanation:  {c.risk_explanation}")
        if c.risk_score in ["HIGH", "MEDIUM"]:
            print(f"  • ✍️ Redline Recommendation:\n    {c.suggested_redline}")

    if report.missing_critical_clauses:
        print("\n" + "-" * 65)
        print("⚠️ MISSING MANDATORY / STANDARD CLAUSES")
        print("-" * 65)
        for missing in report.missing_critical_clauses:
            print(f"  ❌ {missing}")
            
    print("\n" + "="*65)
    print("✅ Audit Complete!")
    print("="*65 + "\n")