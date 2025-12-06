# MedicalChatbot (starter)

This small skeleton provides a minimal project layout to build a medical
chatbot that uses a graph database (Neo4j) and LangChain for LLM orchestration.

Structure:

- `data/` — optional raw data files (csv, txt)
- `graph/` — scripts to populate and interact with Neo4j
- `langchain_pipeline/` — LangChain-based chatbot logic
- `requirements.txt` — Python dependencies
- `main.py` — small runner script

Quick start (Windows PowerShell):

```powershell
cd ".../GraphRag-minimaliste/MedicalChatbot"
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Configure Neo4j env vars (optional)
$env:NEO4J_URI = 'bolt://localhost:7687'
$env:NEO4J_USER = 'neo4j'
$env:NEO4J_PASSWORD = 'password'
python graph/build_graph.py
python main.py
```

Next steps:
- Implement retrieval and vector store in `langchain_pipeline/chatbot.py`.
- Expand `graph/build_graph.py` to load real medication/allergy data.
- Add tests and CI as needed.
