from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.placement_test import PlacementLevel
from models.progress import ProgressStatus
from repositories import course_repo, placement_repo, progress_repo
from schemas.placement import PlacementQuestionOut, PlacementResultOut, PlacementSubmitIn

# Вопросы идут от простого к сложному, каждый привязан к стеку, который он проверяет.
# Курс должен содержать ровно эти стеки (по slug), иначе вопросы для стека пропускаются.
QUESTION_BANK: dict[str, list[dict]] = {
    "frontend": [
        {
            "stack_slug": "html-css",
            "question": "Какой тег HTML используют для основного уникального контента страницы?",
            "options": ["<div>", "<main>", "<span>", "<section>"],
            "answer": "<main>",
        },
        {
            "stack_slug": "html-css",
            "question": "Что делает CSS-свойство box-sizing: border-box?",
            "options": [
                "Убирает border",
                "Включает padding и border в заданную width/height",
                "Добавляет тень элементу",
                "Меняет порядок margin и padding",
            ],
            "answer": "Включает padding и border в заданную width/height",
        },
        {
            "stack_slug": "javascript",
            "question": "Какое ключевое слово объявляет переменную, которую нельзя переназначить?",
            "options": ["var", "let", "const", "function"],
            "answer": "const",
        },
        {
            "stack_slug": "javascript",
            "question": "Какой метод массива возвращает новый массив, применяя функцию к каждому элементу?",
            "options": ["filter", "map", "reduce", "forEach"],
            "answer": "map",
        },
    ],
    "backend": [
        {
            "stack_slug": "python-basics",
            "question": "Какой тип данных в Python является неизменяемым (immutable)?",
            "options": ["list", "dict", "tuple", "set"],
            "answer": "tuple",
        },
        {
            "stack_slug": "python-basics",
            "question": "Что выведет код, если в функции нет оператора return?",
            "options": ["0", "''", "None", "Ошибку"],
            "answer": "None",
        },
        {
            "stack_slug": "fastapi",
            "question": "На какой библиотеке валидации данных построен FastAPI?",
            "options": ["marshmallow", "Pydantic", "attrs", "Cerberus"],
            "answer": "Pydantic",
        },
        {
            "stack_slug": "fastapi",
            "question": "Какой механизм FastAPI используют для внедрения зависимостей (например, сессии БД)?",
            "options": ["Depends", "Inject", "Provide", "UseDependency"],
            "answer": "Depends",
        },
    ],
}


def _get_questions(course_slug: str) -> list[dict]:
    questions = QUESTION_BANK.get(course_slug)
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вступительный тест для этого курса недоступен")
    return questions


def get_questions(course_slug: str) -> list[PlacementQuestionOut]:
    return [PlacementQuestionOut(question=q["question"], options=q["options"]) for q in _get_questions(course_slug)]


def submit_placement(db: Session, course_slug: str, user_id: UUID, payload: PlacementSubmitIn) -> PlacementResultOut:
    course = course_repo.get_by_slug(db, course_slug)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Курс не найден")

    questions = _get_questions(course_slug)
    if len(payload.answers) != len(questions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Количество ответов не совпадает с количеством вопросов"
        )

    correct_count = sum(
        1 for q, a in zip(questions, payload.answers) if a.strip() == q["answer"].strip()
    )
    score = round(correct_count / len(questions) * 100)

    stack_slugs = list(dict.fromkeys(q["stack_slug"] for q in questions))
    stacks = course_repo.get_stacks_for_course(db, course.id)
    stacks_by_slug = {s.slug: s for s in stacks}

    mastered_slugs: list[str] = []
    for slug in stack_slugs:
        stack_questions = [q for q in questions if q["stack_slug"] == slug]
        answers_for_stack = [
            payload.answers[i] for i, q in enumerate(questions) if q["stack_slug"] == slug
        ]
        all_correct = all(
            a.strip() == q["answer"].strip() for q, a in zip(stack_questions, answers_for_stack)
        )
        if all_correct:
            mastered_slugs.append(slug)
        else:
            break  # stacks идут от простого к сложному — останавливаемся на первом провале

    unlocked_stacks: list[str] = []
    for slug in stack_slugs:
        stack = stacks_by_slug.get(slug)
        if not stack:
            continue
        if slug in mastered_slugs:
            progress_repo.set_stack_status(db, user_id, stack.id, ProgressStatus.completed)
        else:
            progress_repo.set_stack_status(db, user_id, stack.id, ProgressStatus.in_progress)
            unlocked_stacks.append(slug)
            break

    if len(mastered_slugs) == 0:
        result_level = PlacementLevel.beginner
    elif len(mastered_slugs) == len(stack_slugs):
        result_level = PlacementLevel.advanced
    else:
        result_level = PlacementLevel.intermediate

    result = placement_repo.add_result(db, user_id, course.id, result_level, score, payload.answers)

    return PlacementResultOut(
        id=result.id,
        result_level=result.result_level.value,
        score=result.score,
        unlocked_stacks=unlocked_stacks or mastered_slugs,
        completed_at=result.completed_at,
    )
