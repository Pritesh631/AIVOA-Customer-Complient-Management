import io, uuid
from fastapi import FastAPI, Depends, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pypdf import PdfReader
from .config import frontend_origins
from .db import Base, engine, get_db
from .models import Complaint
from .schemas import ComplaintInput, AIAnalysis, ComplaintResponse
from .ai import analyze_complaint

Base.metadata.create_all(bind=engine)
app = FastAPI(title="AIVOA Complaint QMS API", version="1.0.0")
allowed_origins = frontend_origins()
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def number():
    return "CC-" + uuid.uuid4().hex[:8].upper()

def to_response(x):
    return ComplaintResponse(id=x.id, complaint_number=x.complaint_number, source=x.source, customer_name=x.customer_name or "", product_name=x.product_name or "", batch_number=x.batch_number or "", dosage_form=x.dosage_form or "", market=x.market or "", complaint_date=x.complaint_date or "", description=x.description, summary=x.summary, risk_level=x.risk_level, risk_score=x.risk_score, risk_rationale=x.risk_rationale, ai_analysis=x.ai_analysis, status=x.status, created_at=x.created_at.isoformat())

@app.get("/api/health")
def health(): return {"status": "ok"}

@app.get("/api/complaints", response_model=list[ComplaintResponse])
def list_complaints(db: Session = Depends(get_db)):
    return [to_response(x) for x in db.query(Complaint).order_by(Complaint.created_at.desc()).all()]

@app.get("/api/complaints/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: int, db: Session = Depends(get_db)):
    x = db.get(Complaint, complaint_id)
    if not x: raise HTTPException(404, "Complaint not found")
    return to_response(x)

@app.post("/api/analyze", response_model=AIAnalysis)
def analyze(payload: ComplaintInput):
    return analyze_complaint(payload.model_dump())

@app.post("/api/analyze-file", response_model=AIAnalysis)
async def analyze_file(file: UploadFile = File(...)):
    data = await file.read()
    text = ""
    name = (file.filename or "").lower()
    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
        text = "\n".join((p.extract_text() or "") for p in reader.pages)
    else:
        text = data.decode("utf-8", errors="ignore")
    if not text.strip(): raise HTTPException(400, "Could not extract text from file")
    return analyze_complaint({"source": "Uploaded File", "description": text[:12000]})

@app.post("/api/complaints", response_model=ComplaintResponse)
def create(payload: ComplaintInput, db: Session = Depends(get_db)):
    data = payload.model_dump()
    result = analyze_complaint(data)
    x = Complaint(complaint_number=number(), **data, summary=result.get("summary"), risk_level=result.get("risk_level"), risk_score=result.get("risk_score"), risk_rationale=result.get("risk_rationale"), ai_analysis=result, status="Open")
    db.add(x); db.commit(); db.refresh(x)
    return to_response(x)
