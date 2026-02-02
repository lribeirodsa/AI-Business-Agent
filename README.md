# AI Business Agent: PEP Investigation with LangGraph and Data Intelligence**

In today’s landscape of financial compliance and anti-corruption efforts, identifying **Politically Exposed Persons (PEPs)** and sanctioned individuals requires more than a simple database search. It demands an investigative AI agent capable of performing complex relational analysis and making autonomous decisions.

### **The Architecture of Thought: LangGraph**

Unlike traditional systems, this agent is built on **LangGraph**. While standard AI chains are linear, LangGraph allows for the creation of a **cyclic graph**. This means the agent can:

* Query a database.
* Assess if the results are ambiguous (e.g., homonyms/namesakes).
* Decide to seek additional sources before issuing a verdict.

### **The Data Arsenal: OpenSanctions, UN, and OFAC**

To ensure the surgical precision required in **Know Your Customer (KYC)** processes, the agent integrates via API with the world’s most robust sources:

* **OpenSanctions:** Acts as the central hub, consolidating global PEP data and international sanctions lists into a structured format.
* **UN Lists (Security Council):** Focused on individuals linked to global conflicts and terrorism.
* **OFAC (U.S. Department of the Treasury):** Essential for international financial system compliance, monitoring the SDN (Specially Designated Nationals) list.

---

### **The Agent’s Workflow**

The investigation process follows four critical stages:

1. **Entity Extraction:** The agent receives a name or document and normalizes the data (handling spelling variations and transliterations).
2. **Multi-Source Search:** Parallel requests are triggered across APIs. The agent doesn't just search for the name; it cross-references dates of birth and known political positions.
3. **Relationship Graph Analysis:** Leveraging OpenSanctions' capabilities, the agent identifies not only the target but also their **"Relatives and Close Associates" (RCA)**, expanding the investigation to prevent the use of "strawmen" or proxies.
4. **Risk Reporting:** Instead of a simple "Yes/No," the agent generates a reasoned justification, assigning a confidence score based on data similarity.

> **Note on Precision:** The use of Generative AI here is not to "invent" facts, but to interpret vast amounts of technical data and transform them into an executive summary for the human analyst.

---

### **Conclusion**

This agent does not replace the compliance analyst; it elevates them to the role of a high-level decision-maker. By automating the screening of OFAC, UN, and OpenSanctions lists through **LangGraph orchestration**, we reduce analysis time from hours to seconds, effectively mitigating reputational risks.

---

**Would you like me to adjust the tone to be more academic, or perhaps create a visual representation of the LangGraph logic for this specific use case?**


# Development

## Master Business Auditor & KYC Intelligence Platform
This project is a high-performance, multi-agent AI system built with LangGraph and Streamlit. It automates complex Due Diligence, Know Your Customer (KYC), and Compliance workflows by integrating global sanctions lists, corporate registries, and real-time intelligence.
 Project Evolution & Milestones

## The platform evolved through several iterations to reach its current state-of-the-art capability:

### Version 1: Core Multi-Agent Architecture
•	Objective: Establish the foundation using LangGraph.
•	Features: Initial agents for SEC data collection and OFAC sanctions screening.
•	Output: Basic PDF report and relationship graph.

### Version 2: Dynamic Input & Professional Reporting
•	Objective: Support dynamic inputs for any person or company.
•	Features: Added a classification agent to distinguish between individuals and corporations.
•	Output: Improved PDF layout with business-standard formatting.

### Version 3: KYC Risk Scoring & Audit Comments
•	Objective: Provide quantitative and qualitative risk analysis.
•	Features: Implementation of a KYC Risk Score algorithm (0-100) and an Audit Agent generating 5-10 detailed analytical comments.
•	Output: Risk-centric reports with color-coded alerts.

### Version 4: Global Expansion & English Localization
•	Objective: Adapt the system for international business use.
•	Features: Full translation of code, prompts, and reports into English.
•	Output: Global compliance report format.

### Version 5: News Intelligence & Real-time Correlation
•	Objective: Integrate current events into risk assessment.
•	Features: Added a News Intelligence Agent to fetch real-time headlines and correlate media sentiment with the risk score.
•	Output: Section dedicated to "Recent News & Media Sentiment".

### Version 6: Master Integration (OpenCorporates & OpenSanctions)
•	Objective: Maximum data coverage and accuracy.
•	Features: 
◦	Integration with OpenCorporates for official registry data.
◦	Integration with OpenSanctions (Global PEPS, Sanctions, and Watchlists).
◦	Integration with Wikipedia for historical and biographical context.
•	Accuracy: Enhanced name normalization algorithms to minimize false positives.

### Version 7: Master Streamlit UI
•	Objective: Professional user experience.
•	Features: Full web-based interface with real-time agent tracking, interactive metrics, and an integrated PDF download button.

### Key Components & Data Sources
Source	Description	Purpose
OFAC SDN	US Treasury Sanctions List	Legal Compliance
UN Security Council	UN Consolidated Sanctions	International Law
OpenSanctions	Global PEPs & Watchlists	Extended Due Diligence
OpenCorporates	Largest Open Database of Companies	Registry Verification
Wikipedia	Global Encyclopedia	Historical Context
Real-time News	Web-scraped Media	Sentiment & Recent Risk


### Technical Stack
•	Framework: LangGraph (Stateful Multi-Agent Orchestration)
•	AI Models: GPT-4o mini, GEMINI or Ollama (Logic, Analysis, and Synthesis)
•	Interface: Streamlit (Web Application)
•	Data Processing: BeautifulSoup4, Requests, XML Etree
•	Visualization: NetworkX, Matplotlib (Relationship Graphs)
•	Reporting: FPDF2 (Certified PDF Generation)

### How to Run
1	Install Dependencies:
pip install streamlit langgraph langchain-openai networkx matplotlib fpdf2 requests beautifulsoup4 wikipedia-api
2	Launch the Platform:
streamlit run master_business_auditor.py

### Output Examples
•	Certified PDF Report: A multi-page document containing the KYC Score, deep analytical audit findings, and evidence from all sources.
•	Network Graph: A visual representation of shareholders, associates, and related corporate entities.


### Developed as an ultimate tool for Compliance Officers, Legal Teams, and Business Analysts.
