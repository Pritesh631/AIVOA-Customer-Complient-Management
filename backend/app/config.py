import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "gemma2-9b-it")
MOCK_AI = os.getenv("MOCK_AI", "false").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aivoa.db")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
