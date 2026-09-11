import json
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from .config import GROQ_API_KEY, GROQ_MODEL, MOCK_AI

class GraphState(TypedDict, total=False):
    complaint: dict
    result: dict

def mock_result(c: dict) -> dict:
    desc = c.get("description", "")
    missing = [k for k in ["customer_name", "product_name", "batch_number", "complaint_date"] if not c.get(k)]
    high_terms = ["serious", "hospital", "death", "injury", "ineffective", "contamination", "adverse"]
    high = any(t in desc.lower() for t in high_terms)
    risk = "High" if high else ("Medium" if missing else "Low")
    score = 85 if risk == "High" else (55 if risk == "Medium" else 20)
    return {"extracted": c, "summary": desc[:500], "completeness_score": max(0, 100-len(missing)*15),
            "missing_fields": missing, "risk_level": risk, "risk_score": score,
            "risk_rationale": "Potential patient/product impact requires QA review." if high else "No immediate high-severity signal detected from the provided information.",
            "root_cause_recommendations": ["Review batch manufacturing and packaging records", "Check complaint trend and retain samples"],
            "capa_recommendations": ["Open investigation if confirmed", "Trend similar complaints and define preventive action"],
            "duplicate_risk": "Low", "duplicate_reason": "No prior-complaint comparison was supplied to the mock analyzer."}

def analyze_node(state: GraphState):
    c = state["complaint"]
    if MOCK_AI or not GROQ_API_KEY:
        return {"result": mock_result(c)}
    llm = ChatGroq(model=GROQ_MODEL, temperature=0, api_key=GROQ_API_KEY)
    system = SystemMessage(content="""You are a pharmaceutical QMS customer-complaint copilot. Analyze the complaint conservatively. Never invent facts. Return ONLY valid JSON with keys: extracted (object), summary (string), completeness_score (integer 0-100), missing_fields (array), risk_level (Low|Medium|High|Critical), risk_score (integer 0-100), risk_rationale (string), root_cause_recommendations (array of strings), capa_recommendations (array of strings), duplicate_risk (Low|Medium|High), duplicate_reason (string). Risk is a triage aid, not a final QA decision.""")
    prompt = HumanMessage(content="Complaint data:\n" + json.dumps(c, ensure_ascii=False))
    raw = llm.invoke([system, prompt]).content
    text = raw.strip().replace("```json", "").replace("```", "").strip()
    return {"result": json.loads(text)}

def build_graph():
    g = StateGraph(GraphState)
    g.add_node("analyze", analyze_node)
    g.add_edge(START, "analyze")
    g.add_edge("analyze", END)
    return g.compile()

GRAPH = build_graph()

def analyze_complaint(complaint: dict) -> dict:
    return GRAPH.invoke({"complaint": complaint})["result"]
