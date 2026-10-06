import os
import re
import pdfplumber
from docx import Document


def extract_text_from_file(file_path: str) -> str:
    """Extracts raw text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    else:
        raise ValueError(f"Unsupported file format: {ext}")


def split_into_clauses(contract_text: str) -> list[dict]:
    """
    Splits contract text into logical clause blocks using numbered headings
    (e.g., '1. CONFIDENTIAL INFORMATION', 'SECTION 2.', 'ARTICLE III').
    """
    # Normalize Windows line endings \r\n to \n
    normalized_text = contract_text.replace("\r\n", "\n")

    # Regex matches newlines followed by headings like "1. ", "2) ", "SECTION 1", "ARTICLE I"
    heading_pattern = r"\n(?=(?:\d+[\.\)]|\bSECTION\s+\d+|\bARTICLE\s+[IVXLCDM]+)\s+)"
    
    raw_chunks = re.split(heading_pattern, normalized_text, flags=re.IGNORECASE)
    
    clauses = []
    for chunk in raw_chunks:
        clean_chunk = chunk.strip()
        if not clean_chunk:
            continue
        
        # Split into title line (first line) and body content
        lines = clean_chunk.split("\n")
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else clean_chunk
        
        clauses.append({
            "clause_number": len(clauses) + 1,
            "title": title,
            "content": body if body else clean_chunk
        })

    return clauses


# --- Test Code ---
if __name__ == "__main__":
    file_path = "sample_contract.txt"
    print(f"Reading contract from: {file_path}")
    raw_text = extract_text_from_file(file_path)
    
    clauses = split_into_clauses(raw_text)
    print(f"\n✅ Total Clauses Extracted: {len(clauses)}\n")
    
    for c in clauses:
        print(f"--- [Clause {c['clause_number']}] {c['title']} ---")
        print(f"{c['content'][:120]}...\n")