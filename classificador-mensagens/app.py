import os
import json
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="AI Message Triage")
st.title("AI Message Triage")
st.write("Classifique mensagens de atendimento e sugira uma resposta.")

message = st.text_area("Cole uma mensagem", height=150, placeholder="Ex.: Meu pedido está atrasado e preciso de ajuda.")
if st.button("Analisar mensagem", type="primary"):
    if not message.strip():
        st.warning("Digite uma mensagem primeiro.")
        st.stop()
    text = message.lower()
    urgent_terms = ["urgente", "hoje", "imediatamente", "bloqueado", "não consigo", "fraude", "cobrança indevida"]
    negative_terms = ["péssimo", "insatisfeito", "problema", "atrasado", "reclamação", "não funciona", "cancelar"]
    if any(t in text for t in ["pagamento", "cobrança", "fatura", "pix", "reembolso"]):
        category = "Financeiro"
    elif any(t in text for t in ["pedido", "entrega", "rastreamento", "atrasado"]):
        category = "Pedido e entrega"
    elif any(t in text for t in ["erro", "bug", "não funciona", "senha", "acesso"]):
        category = "Suporte técnico"
    else:
        category = "Geral"
    priority = "Alta" if any(t in text for t in urgent_terms) else "Normal"
    sentiment = "Negativo" if any(t in text for t in negative_terms) else "Neutro ou positivo"
    c1, c2, c3 = st.columns(3)
    c1.metric("Categoria", category)
    c2.metric("Prioridade sugerida", priority)
    c3.metric("Sentimento estimado", sentiment)
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "Você auxilia uma equipe de atendimento. Responda em português com JSON válido contendo as chaves resumo, resposta_sugerida e cuidados. Não prometa reembolso ou prazos sem confirmação."},
                    {"role": "user", "content": message}
                ],
                temperature=0.2,
            )
            raw = response.choices[0].message.content
            st.subheader("Sugestão da IA")
            try:
                data = json.loads(raw)
                st.write("**Resumo:**", data.get("resumo", ""))
                st.write("**Resposta sugerida:**", data.get("resposta_sugerida", ""))
                st.write("**Cuidados:**", data.get("cuidados", ""))
            except json.JSONDecodeError:
                st.write(raw)
        except Exception as exc:
            st.error(f"Falha na API: {exc}")
    else:
        st.info("Para sugestões generativas, configure OPENAI_API_KEY no arquivo .env. A classificação acima usa regras simples.")
