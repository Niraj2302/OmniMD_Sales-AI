from langgraph.graph import StateGraph, END
from agents.state import ProspectState
from rag.text_pipeline import retrieve_text
from rag.ocr_pipeline import retrieve_ocr

def research_node(state: ProspectState):
    p_id = state["prospect_id"]
    text_context = retrieve_text(f"Information about prospect {p_id}")
    ocr_context = retrieve_ocr(f"Business card data for {p_id}")

    return {
        "retrieved_context": [text_context, ocr_context]
    }

def scoring_node(state: ProspectState):
    signals = state.get("gathered_signals", {})
    intent = str(signals.get("intent", "")).lower()
    role = str(signals.get("linkedin", "")).lower()

    score = 50
    if "high" in intent:
        score += 30
    elif "medium" in intent:
        score += 10

    if any(title in role for title in ["vp", "ceo", "cto", "director", "head", "founder"]):
        score += 20

    score = min(score, 100)

    if score >= 90:
        action = "Call Now"
    elif score >= 75:
        action = "Send Personalized Email"
    elif score >= 50:
        action = "Reach out on LinkedIn"
    else:
        action = "Review & Research"

    return {
        "score": score,
        "next_action": action,
        "rationale": f"Scored {score} based on {intent} signals and {role} seniority.",
        "needs_human_review": score < 75
    }

workflow = StateGraph(ProspectState)

workflow.add_node("research", research_node)
workflow.add_node("scoring", scoring_node)

workflow.set_entry_point("research")
workflow.add_edge("research", "scoring")
workflow.add_edge("scoring", END)

app_graph = workflow.compile()