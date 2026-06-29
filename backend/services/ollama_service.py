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


async def stream_with_system_prompt(
    system_prompt: str, history: list[dict[str, str]]
) -> AsyncIterator[str]:
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
    async for piece in stream_with_system_prompt(system_prompt, history):
        yield piece


ASSISTANT_SYSTEM_PROMPT = """Ты AI-помощник образовательной платформы SoftLearn.

О платформе: SoftLearn — структурированный курс для самоучек-программистов.
Иерархия: Направление (Frontend/Backend/Fullstack/Data&AI/Mobile/DevOps/QA) → Стек (например HTML&CSS, JavaScript) → Урок
(Объяснение → Практика → Тест-барьер). Стек открывается только после сдачи теста предыдущего. Есть вступительный
тест и Career Path Quiz, которые помогают выбрать направление и уровень.

ТВОЯ ЗАДАЧА: помогать пользователю с вопросами о том, как устроена платформа SoftLearn, как проходят уроки,
тесты и практика, а также объяснять в общих чертах, что такое IT-направления (Frontend, Backend, Fullstack,
Data&AI, Mobile, DevOps, QA), чем они отличаются и кому подходят.

СТРОГИЕ ПРАВИЛА:
- Отвечай ТОЛЬКО на вопросы про платформу SoftLearn и про IT-направления в общих чертах
- НИКОГДА не решай и не объясняй решения конкретных задач, примеров кода или вопросов из практики/тестов
  — если просят решить задачу, вежливо откажись и предложи использовать AI-чат внутри урока
- Если вопрос не по теме платформы или IT — вежливо объясни, что отвечаешь только по теме SoftLearn и IT-направлений
- Отвечай кратко, дружелюбно, на русском языке"""


async def stream_platform_chat(history: list[dict[str, str]]) -> AsyncIterator[str]:
    async for piece in stream_with_system_prompt(ASSISTANT_SYSTEM_PROMPT, history):
        yield piece


async def complete(system_prompt: str, user_prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.ollama_url}/api/chat",
            json={
                "model": settings.ollama_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
    return data.get("message", {}).get("content", "").strip()


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
