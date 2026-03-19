import requests

API_URL = "https://router.huggingface.co/v1/chat/completions"

headers = {
    "Authorization": "Bearer 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"
}

def rewrite_query(query, memory):
    """
    Rewrites a user query into a self-contained query using chat history.
    """

    history = memory.get()

    # If no history, no need to rewrite
    if not history:
        return query

    messages = [
        {
            "role": "system",
            "content": """You are a query rewriting assistant.

Your job:
- Convert the user's query into a clear, standalone query
- Use conversation history for context
- DO NOT answer the question
- ONLY return the rewritten query
- Keep it concise and precise
"""
        }
    ]

    # Add last few messages only (avoid token overload)
    messages.extend(history[-4:])

    # Add rewrite instruction
    messages.append({
        "role": "user",
        "content": f"Rewrite this query to be fully self-contained:\n{query}"
    })

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={
                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                "messages": messages,
                "max_tokens": 50
            },
            timeout=20
        )

        if response.status_code != 200:
            print("⚠️ Rewrite failed, using original query")
            return query

        result = response.json()
        rewritten_query = result["choices"][0]["message"]["content"].strip()

        print("🔁 Rewritten Query:", rewritten_query)

        return rewritten_query

    except Exception as e:
        print("⚠️ Rewrite exception:", e)
        return query