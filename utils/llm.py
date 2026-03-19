import requests
import os

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer hf_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
}

def generate_answer(context, query, memory):
    if not context:
        context = "No context available."

    # Build structured message
    messages = [
        {
            "role": "system",
            "content": """You are a precise and reliable AI assistant.

Rules:
- Answer ONLY using the provided context
- Do NOT use outside knowledge
- Keep answers concise and direct (1–3 lines unless asked otherwise)
- Do NOT explain your reasoning
- If the answer is not in the context, say:
  "The answer is not available in the provided context."
- Do NOT guess or hallucinate
- Always cite the page number from the context in parentheses, e.g. (Page 2)
- If the answer contains multiple points, format it as bullet points.
- Always maintain a neutral and factual tone.
- Never provide opinions or assumptions.
- Always ensure your answer is based solely on the provided context.
- If the context contains conflicting information, state:
  "The context contains conflicting information, unable to provide a definitive answer."
- Always prioritize accuracy and relevance in your answers.
"""
        }
    ]

    # 🧠 ADD MEMORY
    messages.extend(memory.get())

    # Add current query
    messages.append({
        "role": "user",
        "content": f"""
Context:
{context[:1500]}

Question:
{query}

Give a clear, structured answer.
"""
    })

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
                "messages": messages,
                "max_tokens": 200
            },
            timeout=30
        )

        if response.status_code != 200:
            return f"API Error: {response.text}"

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Exception: {str(e)}"