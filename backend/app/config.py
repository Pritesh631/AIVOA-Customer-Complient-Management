import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MOCK_AI = os.getenv("MOCK_AI", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aivoa.db")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173,http://localhost:5174")

def frontend_origins():
    origins = []
    for origin in FRONTEND_ORIGIN.split(","):
        value = origin.strip()
        if value:
            origins.append(value)
    defaults = [
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://heroic-kangaroo-9adecd.netlify.app",
    ]
    for value in defaults:
        if value not in origins:
            origins.append(value)
    return origins
