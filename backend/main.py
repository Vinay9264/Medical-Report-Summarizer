from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.medical_routes import router as medical_router

app = FastAPI(
    title="Medical Report Summarizer API",
    description="OCR → Clean → Summarize with doctor/patient mode",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Medical Summarizer Backend Running 🚀"}


app.include_router(medical_router, prefix="", tags=["Medical Processing"])
