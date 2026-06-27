"""Строит pgvector-эмбеддинги для всех уроков (для RAG в AI-чате).

Запуск: python scripts/index_lessons.py
Требует запущенную Ollama с моделью OLLAMA_EMBEDDING_MODEL (по умолчанию nomic-embed-text).
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.database import SessionLocal
from models.lesson import Lesson
from services import rag_service


async def main():
    db = SessionLocal()
    try:
        lessons = db.query(Lesson).all()
        for lesson in lessons:
            count = await rag_service.index_lesson(db, lesson)
            print(f"  {lesson.title}: {count} чанков")
        print(f"Готово. Проиндексировано уроков: {len(lessons)}")
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())
