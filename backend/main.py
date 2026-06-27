from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import ai_chat, auth, courses, exercises, lessons, onboarding, placement, progress, stacks, tests

app = FastAPI(title="SoftLearn API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(stacks.router)
app.include_router(lessons.router)
app.include_router(ai_chat.router)
app.include_router(exercises.router)
app.include_router(tests.router)
app.include_router(onboarding.router)
app.include_router(placement.router)
app.include_router(progress.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
