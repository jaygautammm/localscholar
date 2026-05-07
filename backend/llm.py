from openai import OpenAI

from config import LM_STUDIO_BASE_URL, LM_STUDIO_API_KEY, LM_STUDIO_MODEL


client = OpenAI(
    base_url=LM_STUDIO_BASE_URL,
    api_key=LM_STUDIO_API_KEY
)


def ask_local_llm(question, context, model=None):
    """
    Ask local LM Studio model using retrieved RAG context.
    """
    selected_model = model or LM_STUDIO_MODEL

    system_prompt = """
You are LocalScholar, a careful RAG-based research assistant.

You must answer using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. If the answer is not supported by the context, say:
   "I don't know based on the provided document."
3. Cite sources using this format:
   (Source 1, Chapter: ..., Pages: ...)
4. Do not invent page numbers, chapters, quotes, or claims.
5. If multiple sources support the answer, mention them briefly.
6. Keep the answer clear and useful for a student.
"""

    user_prompt = f"""
Question:
{question}

Retrieved Context:
{context}

Answer:
"""

    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content