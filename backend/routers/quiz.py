from fastapi import APIRouter, Depends

from models.user import User
from schemas.quiz import QuizQuestionOut, QuizResultOut, QuizSubmitIn
from services import auth_service, quiz_service

router = APIRouter(prefix="/api/quiz", tags=["quiz"])


@router.get("/career-path", response_model=list[QuizQuestionOut])
def get_career_path_questions(current_user: User = Depends(auth_service.get_current_user)):
    return quiz_service.get_questions()


@router.post("/career-path/submit", response_model=QuizResultOut)
async def submit_career_path(
    payload: QuizSubmitIn,
    current_user: User = Depends(auth_service.get_current_user),
):
    return await quiz_service.submit_quiz(payload.answers)
