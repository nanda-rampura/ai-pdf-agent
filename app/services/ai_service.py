from app.core.config import client

def ask_llm(context: str, question: str):
    prompt = f"""
You are a precise assistant for answering questions from documents.

RULES:
- Use ONLY the provided context
- If answer is not in context, say: "I don't know"
- Do not guess
- Be concise

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content