
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import logging
import traceback
from typing import Tuple

from backend.utils.file_utils import save_file
from backend.ocr.image_ocr import extract_text_from_image
from backend.ocr.pdf_ocr import extract_text_from_pdf
from backend.nlp.preprocess import clean_text
from backend.nlp.summarize import summarize_text

router = APIRouter()
logger = logging.getLogger("medical_routes")


def _normalize_mode(raw_mode: str) -> str:
    
    if not raw_mode:
        return "patient"
    m = raw_mode.strip().lower()
    if "doctor" in m:
        return "doctor"
    if "patient" in m:
        return "patient"
    
    return "patient"


def _extract_text_from_file(path: str, filename: str) -> Tuple[str, str]:
    """
    Extract text from file path depending on extension.
    Returns tuple (extracted_text, error_message) where error_message is None on success.
    """
    try:
        ext = filename.lower()
        if ext.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff")):
            text = extract_text_from_image(path)
            return text or "", None
        elif ext.endswith(".pdf"):
            text = extract_text_from_pdf(path)
            return text or "", None
        else:
            return "", f"Unsupported file type: {filename}"
    except Exception as e:
        logger.exception("Error during text extraction")
        return "", f"Text extraction failed: {str(e)}"


@router.post("/process")
async def process_medical_report(
    file: UploadFile = File(...),
    mode: str = Form("patient")  
):
    """
    Endpoint: POST /api/process
    Expects multipart/form-data with:
      - file: image or pdf
      - mode: "For Doctor" / "For Patient" or "doctor" / "patient"
    Returns JSON with keys:
      - extracted_text
      - cleaned_text
      - summary
    """
    
    try:
        file_path = await save_file(file)
    except Exception as e:
        logger.exception("Failed to save uploaded file")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # 2. Extract text
    extracted_text, extract_err = _extract_text_from_file(file_path, file.filename)
    if extract_err:
        raise HTTPException(status_code=400, detail=extract_err)

    if not extracted_text or not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the file.")

    
    try:
        cleaned = clean_text(extracted_text)
    except Exception as e:
        logger.exception("Text cleaning failed")
        
        cleaned = extracted_text

    
    fallback_note = None
    if not cleaned or not cleaned.strip():
        fallback_note = "Cleaning removed all text; using raw extracted text as fallback."
        cleaned = extracted_text

    
    normalized_mode = _normalize_mode(mode)

    
    try:
        summary = summarize_text(cleaned, normalized_mode)
    except Exception as e:
        
        tb = traceback.format_exc()
        logger.error("Summarization failed: %s\n%s", e, tb)
        # return helpful error (do not leak internal stack in production; this is for dev)
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )

    
    response_payload = {
        "extracted_text": extracted_text,
        "cleaned_text": cleaned,
        "summary": summary
    }
    if fallback_note:
        response_payload["note"] = fallback_note

    return JSONResponse(content=response_payload)
