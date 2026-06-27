from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories import course_repo, lesson_repo, progress_repo, test_repo
from schemas.test_result import TestOut, TestResultOut, TestSubmitIn


def get_lesson_test(db: Session, lesson_slug: str) -> TestOut:
    lesson = lesson_repo.get_by_slug(db, lesson_slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")

    test = test_repo.get_for_lesson(db, lesson.id)
    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден")

    questions = [{"question": q["question"], "options": q["options"]} for q in test.questions]
    return TestOut(id=test.id, pass_threshold=test.pass_threshold, time_limit=test.time_limit, questions=questions)


def submit_test(db: Session, lesson_slug: str, user_id: UUID, payload: TestSubmitIn) -> TestResultOut:
    lesson = lesson_repo.get_by_slug(db, lesson_slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")

    test = test_repo.get_for_lesson(db, lesson.id)
    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден")

    questions = test.questions
    if len(payload.answers) != len(questions):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Количество ответов не совпадает с количеством вопросов")

    mistakes = []
    correct_count = 0
    for question, user_answer in zip(questions, payload.answers):
        if user_answer.strip() == question["answer"].strip():
            correct_count += 1
        else:
            mistakes.append(
                {
                    "question": question["question"],
                    "user_answer": user_answer,
                    "correct_answer": question["answer"],
                }
            )

    score = round(correct_count / len(questions) * 100)
    passed = score >= test.pass_threshold
    attempt = test_repo.get_attempt_count(db, user_id, test.id) + 1

    result = test_repo.add_result(db, user_id, test.id, score, passed, mistakes, attempt)

    if passed:
        _unlock_progress_after_pass(db, user_id, lesson)

    return TestResultOut.model_validate(result)


def get_test_results(db: Session, lesson_slug: str, user_id: UUID) -> list[TestResultOut]:
    lesson = lesson_repo.get_by_slug(db, lesson_slug)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Урок не найден")
    test = test_repo.get_for_lesson(db, lesson.id)
    if not test:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Тест не найден")
    results = test_repo.get_results(db, user_id, test.id)
    return [TestResultOut.model_validate(r) for r in results]


def _unlock_progress_after_pass(db: Session, user_id: UUID, lesson) -> None:
    progress_repo.complete_lesson(db, user_id, lesson.id)

    siblings = lesson_repo.get_for_stack(db, lesson.stack_id)
    idx = next((i for i, l in enumerate(siblings) if l.id == lesson.id), None)
    if idx is None:
        return

    if idx + 1 < len(siblings):
        next_lesson = siblings[idx + 1]
        if not progress_repo.get_lesson_progress(db, user_id, next_lesson.id):
            progress_repo.unlock_lesson(db, user_id, next_lesson.id)
        return

    # last lesson in the stack passed -> complete the stack and unlock the next one
    progress_repo.complete_stack(db, user_id, lesson.stack_id)
    next_stack = course_repo.get_next_stack(db, lesson.stack)
    if next_stack:
        stack_progress_map = progress_repo.get_stack_progress_map(db, user_id, [next_stack.id])
        if next_stack.id not in stack_progress_map:
            progress_repo.unlock_stack(db, user_id, next_stack.id)
