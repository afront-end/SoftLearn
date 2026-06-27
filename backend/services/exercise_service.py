from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.exercise import ExerciseType
from repositories import exercise_repo, lesson_repo
from schemas.exercise import ExerciseCheckOut, ExerciseOut
from services import ollama_service


def get_lesson_exercises(db: Session, lesson_slug: str) -> list[ExerciseOut]:
    lesson = lesson_repo.get_by_slug(db, lesson_slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")
    exercises = exercise_repo.get_for_lesson(db, lesson.id)
    return [ExerciseOut.model_validate(e) for e in exercises]


async def check_exercise(db: Session, exercise_id: UUID, user_answer: str) -> ExerciseCheckOut:
    exercise = exercise_repo.get_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    if exercise.type == ExerciseType.mcq:
        correct = user_answer.strip() == exercise.answer.strip()
    else:
        verdict = await ollama_service.judge_answer(exercise.question, exercise.answer, user_answer)
        correct = verdict["correct"]

    return ExerciseCheckOut(
        correct=correct,
        explanation=exercise.explanation,
        correct_answer=None if correct else exercise.answer,
    )
