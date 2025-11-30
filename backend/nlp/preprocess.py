import re

def clean_text(text: str) -> str:
    """
    Cleans raw OCR text while KEEPING all medical information.
    Prevents over-cleaning which previously caused empty results.
    """

    if not text or not text.strip():
        return ""

    t = text.replace("\r", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{2,}", "\n", t)

    
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"\S+@\S+\.\S+", "", t)

    
    t = re.sub(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{3,4}\b", "", t)

    
    t = re.sub(r"(?i)page\s*\d+\s*(of\s*\d+)?", "", t)

    
    t = re.sub(r"(?i)(best regards[, ]*.*$)", "", t)

    
    t = re.sub(r"(?i)resultmed.*", "", t)

    
    t = re.sub(r"(?i)^icd[-\s:0-9a-zA-Z.]+$", "", t, flags=re.MULTILINE)
    t = re.sub(r"(?i)^cpt[-\s:0-9a-zA-Z.]+$", "", t, flags=re.MULTILINE)

    
    t = re.sub(r"(?i)\bmrn[: ]*\S+", "", t)
    t = re.sub(r"(?i)\bid[: ]*\S+", "", t)
    t = re.sub(r"(?i)age[: ]*\d+", "", t)

    
    t = re.sub(r"\b(\w+)( \1){2,}\b", r"\1", t)

    t = re.sub(r"\s+", " ", t).strip()

    if len(t.split()) < 12:  
        return text.strip()

    return t.strip()
