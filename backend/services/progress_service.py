from uuid import UUID

from sqlalchemy.orm import Session

from repositories import course_repo, lesson_repo, progress_repo
from schemas.progress import CourseProgressOut, ProgressOverviewOut, StackProgressEntryOut
from services.course_service import COMBINED_COURSE_SLUGS, get_stacks_for_course


def get_overview(db: Session, user_id: UUID) -> ProgressOverviewOut:
    courses = course_repo.get_all(db)
    courses_out: list[CourseProgressOut] = []
    stacks_completed_total = 0
    lessons_completed_total = 0

    for course in courses:
        stacks = get_stacks_for_course(db, course)
        stack_ids = [s.id for s in stacks]
        stack_progress_map = progress_repo.get_stack_progress_map(db, user_id, stack_ids)
        stacks_completed = sum(1 for status in stack_progress_map.values() if status == "completed")

        lesson_ids: list[UUID] = []
        for stack in stacks:
            lesson_ids.extend(l.id for l in lesson_repo.get_for_stack(db, stack.id))
        lessons_completed = progress_repo.count_completed_lessons(db, user_id, lesson_ids)

        courses_out.append(
            CourseProgressOut(
                course_id=course.id,
                course_title=course.title,
                course_slug=course.slug,
                course_icon=course.icon,
                stacks_completed=stacks_completed,
                stacks_total=len(stacks),
                lessons_completed=lessons_completed,
                lessons_total=len(lesson_ids),
            )
        )
        # виртуальные курсы (Fullstack) переиспользуют чужие стеки — не учитываем их в общем итоге,
        # чтобы не считать одни и те же стеки/уроки дважды
        if course.slug not in COMBINED_COURSE_SLUGS:
            stacks_completed_total += stacks_completed
            lessons_completed_total += lessons_completed

    return ProgressOverviewOut(
        courses=courses_out,
        stacks_completed_total=stacks_completed_total,
        lessons_completed_total=lessons_completed_total,
    )


def get_stack_progress_list(db: Session, user_id: UUID) -> list[StackProgressEntryOut]:
    rows = progress_repo.get_all_stack_progress(db, user_id)
    result = []
    for row in rows:
        stack = row.stack
        result.append(
            StackProgressEntryOut(
                course_title=stack.course.title,
                course_slug=stack.course.slug,
                stack_title=stack.title,
                stack_slug=stack.slug,
                status=row.status.value,
            )
        )
    return result
