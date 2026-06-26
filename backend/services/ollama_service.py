import json
from collections.abc import AsyncIterator

import httpx

from core.config import settings

SYSTEM_PROMPT_TEMPLATE = """Ты AI-ассистент образовательной платформы SoftLearn.
Помогаешь пользователю разобраться с темой: {lesson_title}

Контент урока:
{lesson_content}

ПРАВИЛА:
- Отвечай ТОЛЬКО по теме этого урока
- Если вопрос не по теме — вежливо объясни это и предложи вернуться к теме урока
- Объясняй просто, с примерами кода
- Можешь объяснить иначе, если пользователь не понял с первого раза
- Проверяй правильность рассуждений пользователя"""


async def stream_chat(
    lesson_title: str,
    lesson_content: str,
    history: list[dict[str, str]],
) -> AsyncIterator[str]:
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(lesson_title=lesson_title, lesson_content=lesson_content or "")
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
