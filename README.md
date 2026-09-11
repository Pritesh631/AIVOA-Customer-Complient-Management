# AIVOA – AI-Powered Customer Complaint Management System

A demo-ready pharmaceutical Customer Complaint QMS application built with React + Redux Toolkit, FastAPI, PostgreSQL/SQLite, LangGraph and Groq.

## Features
- Complaint creation from manual text or uploaded PDF/TXT/EML files
- AI extraction into a structured complaint form
- Complaint completeness checker
- AI summary
- AI risk classification with rationale
- Root-cause and CAPA recommendations
- Duplicate-complaint similarity check against saved complaints
- Complaint persistence
- Dashboard with complaint counts

## Stack
Frontend: React, Vite, Redux Toolkit, Inter
Backend: FastAPI, SQLAlchemy, LangGraph, Groq
Database: PostgreSQL (or SQLite for zero-config demo)

## Run backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
uvicorn app.main:app --reload --port 8000
```
Set `GROQ_API_KEY` in `.env`. Default model is `gemma2-9b-it` as requested by the assignment.

For a no-LLM demo, set `MOCK_AI=true`.

## Run frontend
```bash
cd frontend
npm install
npm run dev
```
Open the URL printed by Vite, normally http://localhost:5173.

## PostgreSQL
Set `DATABASE_URL` to a PostgreSQL URL. The default is SQLite, making local demonstration easier.

## Demo flow
1. Open Dashboard.
2. Go to New Complaint.
3. Paste a complaint or upload the sample complaint file.
4. Click Analyze with AI.
5. Review extracted fields and AI Copilot risk assessment.
6. Save complaint.
7. Open Complaint List and inspect the saved record.

## Architecture
Frontend -> FastAPI -> LangGraph -> Groq -> structured JSON -> database -> React.
