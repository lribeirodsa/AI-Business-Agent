import os
import json
import requests
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns 
from typing import List, TypedDict, Dict
from pydantic import BaseModel, Field
from fpdf import FPDF
from dotenv import load_dotenv

# LangGraph & LangChain
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

# Global styling for professional visuals
sns.set_theme(style="whitegrid")

# --- 1. SCHEMAS ---
class Connection(BaseModel):
    source: str
    relationship: str
    target: str
    entity_type: str

class ComplianceOutput(BaseModel):
    target_name: str
    risk_score: int
    sanctions_summary: str
    pep_and_political_links: str
    geopolitical_currency_analysis: str
    adverse_media_report: str
    ubo_analysis: str
    operational_recommendations: str
    connections: List[Connection]

class InvestigationState(TypedDict):
    target: str
    raw_intelligence: str
    structured_report: Dict
    pdf_path: str
    graph_path: str

# --- 2. INTELLIGENCE TOOLS ---

def get_serper_intel(query: str, site_filter: str = "") -> str:
    url = "https://google.serper.dev/search"
    search_query = f"{site_filter} {query}".strip()
    payload = json.dumps({"q": search_query, "num": 5, "gl": "us", "hl": "en"})
    headers = {'X-API-KEY': os.getenv("SERPER_API_KEY"), 'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
        return "\n".join([res.get('snippet') for res in response.json().get('organic', [])])
    except: return "Intelligence feed currently unavailable."

def check_opensanctions(query: str) -> str:
    api_key = os.getenv("OS_API_KEY")
    url = "https://api.opensanctions.org/match/default"
    payload = {"queries": {"q1": {"schema": "LegalEntity", "properties": {"name": [query]}}}}
    headers = {"Authorization": f"ApiKey {api_key}", "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        res = response.json().get('responses', {}).get('q1', {}).get('results', [])
        return "\n".join([f"Match: {r['caption']} ({round(r['score']*100)}%)" for r in res[:3]])
    except: return "Sanctions search match failed."

# --- 3. NODES ---
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

def research_node(state: InvestigationState):
    st.toast(f"🔍 Searching global databases for {state['target']}...")
    wiki = get_serper_intel(state['target'], "site:wikipedia.org")
    corp = get_serper_intel(state['target'], "site:opencorporates.com")
    sanctions = check_opensanctions(state['target'])
    news = get_serper_intel(f"{state['target']} adverse media fraud money laundering")
    intel = f"WIKI: {wiki}\nCORP: {corp}\nSANCTIONS: {sanctions}\nNEWS: {news}"
    return {"raw_intelligence": intel}

def analyst_node(state: InvestigationState):
    st.toast("🧠 Analyzing risks and mapping network...")
    # UPDATED PROMPT: Demanding 5-10 lines of detailed agent analysis per section
    prompt = f"""
    You are a Senior AML/KYC Compliance Officer. Analyze the following data for {state['target']}: 
    {state['raw_intelligence']}

    INSTRUCTIONS:
    1. For EVERY section of the report, you MUST write a minimum of 5 to 10 lines of deep, technical analysis.
    2. Do not be generic. Mention specific risks, potential red flags, and the geopolitical context of the findings.
    3. Evaluate the target's corporate structure, reputation in the media, and any possible hidden ownership links.
    4. Provide actionable and detailed Operational Recommendations based on the severity of the findings.
    
    Return ONLY a JSON matching the ComplianceOutput schema. Use English.
    """
    structured_llm = llm.with_structured_output(ComplianceOutput)
    report = structured_llm.invoke([HumanMessage(content=prompt)])
    return {"structured_report": report.dict()}

def document_factory_node(state: InvestigationState):
    st.toast("📄 Generating visual graph and PDF...")
    data = state['structured_report']
    target_clean = state['target'].replace(" ", "_")
    
    # Graph Generation with Seaborn Styling
    G = nx.DiGraph()
    for c in data['connections']:
        G.add_edge(c['source'][:20], c['target'][:20], label=c['relationship'])
    
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, k=1.0)
    nx.draw(G, pos, with_labels=True, 
            node_color=sns.color_palette("viridis", len(G.nodes())), 
            node_size=2500, font_size=8, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    graph_fn = f"graph_{target_clean}.png"
    plt.savefig(graph_fn, dpi=300, bbox_inches='tight')
    plt.close()
    
    # PDF Generation
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    def clean(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')

    pdf.set_font("Arial", "B", 18)
    pdf.cell(190, 15, "GLOBAL COMPLIANCE DOSSIER", 0, 1, "C")
    pdf.line(10, 28, 200, 28)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f"TARGET: {clean(data['target_name'])} | RISK SCORE: {data['risk_score']}/100", 0, 1)
    pdf.ln(5)

    sections = [
        ("Sanctions Summary", data['sanctions_summary']),
        ("Political Exposure", data['pep_and_political_links']),
        ("Currency & Geopolitical", data['geopolitical_currency_analysis']),
        ("Adverse Media", data['adverse_media_report']),
        ("UBO Analysis", data['ubo_analysis']),
        ("Recommendations", data['operational_recommendations'])
    ]

    for title, text in sections:
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(190, 8, clean(title), 0, 1, fill=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(190, 6, clean(text))
        pdf.ln(4)
    
    if os.path.exists(graph_fn):
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "Relationship Network Graph", 0, 1, "C")
        pdf.image(graph_fn, x=10, y=30, w=190)

    pdf_fn = f"report_{target_clean}.pdf"
    pdf.output(pdf_fn)
    return {"pdf_path": pdf_fn, "graph_path": graph_fn}

# --- 4. WORKFLOW COMPILATION ---
workflow = StateGraph(InvestigationState)
workflow.add_node("research", research_node)
workflow.add_node("analyze", analyst_node)
workflow.add_node("generate", document_factory_node)
workflow.set_entry_point("research")
workflow.add_edge("research", "analyze")
workflow.add_edge("analyze", "generate")
workflow.add_edge("generate", END)
app_graph = workflow.compile()

# --- 5. STREAMLIT INTERFACE ---
st.set_page_config(page_title="Intelligence AI", layout="wide", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Intelligence AI: Global Compliance")
st.caption("Advanced Due Diligence powered by LangGraph & GPT-4o-mini")

with st.sidebar:
    st.header("Search Parameters")
    target_input = st.text_input("Enter Entity Name or ID:", placeholder="e.g. Petrobras or John Smith")
    process_btn = st.button("Run Investigation", use_container_width=True, type="primary")
    st.divider()
    st.markdown("### Resources\n- Serper (Wiki/Corp/News)\n- OpenSanctions Match API\n- OFAC / UN / PEP Lists")

if process_btn and target_input:
    with st.status("Initializing Investigation...", expanded=True) as status:
        final_state = app_graph.invoke({"target": target_input})
        status.update(label="Investigation Complete!", state="complete", expanded=False)
    
    report_data = final_state['structured_report']
    
    # Original First Code Layout
    tab1, tab2 = st.tabs(["📊 Analytical Dossier", "🕸️ Relationship Graph"])
    
    with tab1:
        c1, c2 = st.columns([1, 1])
        with c1:
            st.metric("Risk Level", f"{report_data['risk_score']}%")
            st.subheader("Legal & Sanctions")
            st.write(report_data['sanctions_summary'])
        with c2:
            st.subheader("Geopolitical & Currency")
            st.write(report_data['geopolitical_currency_analysis'])
            
        st.divider()
        st.subheader("Detailed Adverse Media & UBO")
        st.write(report_data['adverse_media_report'])
        st.write(report_data['ubo_analysis'])
        
        with open(final_state['pdf_path'], "rb") as f:
            st.download_button(
                label="📄 Download Comprehensive PDF Report",
                data=f,
                file_name=final_state['pdf_path'],
                mime="application/pdf",
                use_container_width=True
            )
    
    with tab2:
        st.image(final_state['graph_path'], caption="Neural Relationship Mapping")
    
    st.divider()
else:
    st.info("Input a name and click 'Run Investigation' to generate the dossier.")