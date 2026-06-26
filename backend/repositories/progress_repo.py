from uuid import UUID

from sqlalchemy.orm import Session

from models.progress import ProgressStatus
from models.stack_progress import StackProgress


def get_stack_progress_map(db: Session, user_id: UUID, stack_ids: list[UUID]) -> dict[UUID, str]:
    rows = (
        db.query(StackProgress)
        .filter(StackProgress.user_id == user_id, StackProgress.stack_id.in_(stack_ids))
        .all()
    )
    return {row.stack_id: row.status.value for row in rows}


def unlock_stack(db: Session, user_id: UUID, stack_id: UUID) -> StackProgress:
    progress = StackProgress(user_id=user_id, stack_id=stack_id, status=ProgressStatus.in_progress)
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress
