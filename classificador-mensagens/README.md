# AI Message Triage

Classifica mensagens por categoria, prioridade e sentimento usando regras locais; opcionalmente usa um modelo de IA via API para sugerir resposta.

## Executar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Sem chave de API, a classificação é heurística e serve como baseline. Com `OPENAI_API_KEY` no `.env`, o app também sugere uma resposta. Não use a classificação como decisão automática de alto impacto.
