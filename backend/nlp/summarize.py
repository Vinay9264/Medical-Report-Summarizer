
import os
import re


from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")


_groq_llm = None


def clean_and_strip_pii(text: str) -> str:
    
    t = text
    t = t.replace("\r", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{2,}", "\n\n", t)
    #t = re.sub(r"https?://\S+", "", t)
    #t = re.sub(r"\S+@\S+\.\S+", "", t)
    #t = re.sub(r"\+?\d[\d\- ]{7,}\d", "", t)
    #t = re.sub(r"(?i)electronically signed.*", "", t)
    #t = re.sub(r"(?i)this report was electronically signed.*", "", t)
    #t = re.sub(r"(?i)page \d+ of \d+", "", t)
    #t = re.sub(r"(?i)result ?med.*", "", t)
    #t = re.sub(r"(?i)best regards.*", "", t)
    #t = re.sub(r"(?i)icd[- ]?\d+.*", "", t)
    #t = re.sub(r"(?i)cpt.*", "", t)
    #t = re.sub(r"(?i)mrn[: ]?\S+", "", t)
    #t = re.sub(r"(?i)\bid[: ]+\S+", "", t)
    #t = re.sub(r"(?i)born[: ].*", "", t)
    #t = re.sub(r"(?i)age[: ]?\d+\w*", "", t)
    t = re.sub(r"(?:\b[a-z]{1,2}\b[\W]?){6,}", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"([.!?])\s+", r"\1\n\n", t)
    return t.strip()


def _init_groq_llm():
    
    global _groq_llm
    if _groq_llm:
        return _groq_llm
    if not GROQ_API_KEY:
        raise RuntimeError("Missing GROQ_API_KEY environment variable.")
    _groq_llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
    return _groq_llm


def summarize_doctor(text: str) -> str:
    llm = _init_groq_llm()
    prompt = f"""
You are a clinical doctor specializing in summarizing medical procedure reports.

Rules:
- NO patient name, age, DOB, MRN, or signatures.
- NO administrative text.
- Extract only medical details.
- If context implies something, infer it logically.
- Use bullet points.

Report:
{text}
"""
    result = llm.invoke(prompt)
    return result.content.strip()


def summarize_patient(text: str) -> str:
    llm = _init_groq_llm()
    prompt = f"""
Explain the medical report in simple, patient-friendly language.

Rules:
- No names, ages, MRN, or signatures.
- No medical codes.
- Use 3–5 sentences max.
- Explain: what happened, why, results, and next steps.

Report:
{text}
"""
    result = llm.invoke(prompt)
    return result.content.strip()


def summarize_text(text: str, mode: str = "patient") -> str:
    
    cleaned = clean_and_strip_pii(text)
    print("CLEANED_DEBUG_OUTPUT:\n", cleaned)

    if mode.lower().strip() == "doctor":
        return summarize_doctor(cleaned)
    else:
        return summarize_patient(cleaned)


if __name__ == "__main__":
    sample = "Patient underwent laparoscopic appendectomy due to acute appendicitis. No complications noted."
    print("Doctor summary:\n", summarize_text(sample, "doctor"))
    print("\nPatient summary:\n", summarize_text(sample, "patient"))