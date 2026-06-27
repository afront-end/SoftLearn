import json
from collections.abc import AsyncIterator

import httpx

from core.config import settings

SYSTEM_PROMPT_TEMPLATE = """Ты AI-ассистент образовательной платформы SoftLearn.
Помогаешь пользователю разобраться с темой: {lesson_title}

Контент урока:
{lesson_content}
{rag_section}
ПРАВИЛА:
- Отвечай ТОЛЬКО по теме этого урока
- Если вопрос не по теме — вежливо объясни это и предложи вернуться к теме урока
- Объясняй просто, с примерами кода
- Можешь объяснить иначе, если пользователь не понял с первого раза
- Проверяй правильность рассуждений пользователя
- Дополнительный контекст из других уроков можно использовать только чтобы лучше связать текущую тему с уже пройденным материалом"""

RAG_SECTION_TEMPLATE = """
Дополнительный контекст из связанных уроков платформы (используй только если это помогает объяснить текущую тему):
{chunks}
"""


async def stream_chat(
    lesson_title: str,
    lesson_content: str,
    history: list[dict[str, str]],
    rag_chunks: list[str] | None = None,
) -> AsyncIterator[str]:
    rag_section = ""
    if rag_chunks:
        rag_section = RAG_SECTION_TEMPLATE.format(chunks="\n---\n".join(rag_chunks))

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        lesson_title=lesson_title, lesson_content=lesson_content or "", rag_section=rag_section
    )
    messages = [{"role": "system", "content": system_prompt}, *history]

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            f"{settings.ollama_url}/api/chat",
            json={"model": settings.ollama_model, "messages": messages, "stream": True},
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                content = chunk.get("message", {}).get("content", "")
                if content:
                    yield content
                if chunk.get("done"):
                    break


JUDGE_PROMPT_TEMPLATE = """Ты проверяешь ответ ученика на учебное задание.

Вопрос: {question}
Правильный/ожидаемый ответ: {expected_answer}
Ответ ученика: {user_answer}

Оцени, верен ли ответ ученика по смыслу (не требуй точного совпадения текста,
для кода — не требуй идентичного форматирования, важна правильная логика).

Ответь СТРОГО в формате JSON без markdown и без пояснений вокруг:
{{"correct": true или false, "explanation": "короткое объяснение на русском"}}"""


async def judge_answer(question: str, expected_answer: str, user_answer: str) -> dict:
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        question=question, expected_answer=expected_answer, user_answer=user_answer
    )

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.ollama_url}/api/generate",
            json={"model": settings.ollama_model, "prompt": prompt, "stream": False, "format": "json"},
        )
        response.raise_for_status()
        data = response.json()

    try:
        parsed = json.loads(data.get("response", "{}"))
        return {
            "correct": bool(parsed.get("correct", False)),
            "explanation": parsed.get("explanation"),
        }
    except (json.JSONDecodeError, TypeError):
        return {"correct": False, "explanation": None}


async def embed_text(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.ollama_url}/api/embed",
            json={"model": settings.ollama_embedding_model, "input": text},
        )
        response.raise_for_status()
        data = response.json()
    return data["embeddings"][0]
