from fastapi import HTTPException, status

from schemas.quiz import QuizQuestionOut, QuizResultOut
from services import ollama_service

# Направления, которые показываем в Career Path Quiz.
# course_slug указывает на реальный Course в БД (None — направление пока недоступно для старта).
DIRECTIONS: dict[str, dict] = {
    "frontend": {
        "title": "Frontend",
        "icon": "🎨",
        "description": "Создаёшь то, что видит и с чем взаимодействует пользователь: интерфейсы, анимации, вёрстка.",
        "course_slug": "frontend",
    },
    "backend": {
        "title": "Backend",
        "icon": "⚙️",
        "description": "Пишешь серверную логику, базы данных и API — то, что работает «под капотом» приложения.",
        "course_slug": "backend",
    },
    "fullstack": {
        "title": "Fullstack",
        "icon": "🧩",
        "description": "Совмещаешь frontend и backend — строишь продукт от интерфейса до базы данных целиком.",
        "course_slug": "fullstack",
    },
    "data_ai": {
        "title": "Data & AI",
        "icon": "📊",
        "description": "Работаешь с данными, статистикой и моделями машинного обучения, ищешь закономерности.",
        "course_slug": None,
    },
    "mobile": {
        "title": "Mobile",
        "icon": "📱",
        "description": "Разрабатываешь приложения для смартфонов на iOS и Android.",
        "course_slug": None,
    },
    "devops": {
        "title": "DevOps",
        "icon": "🛠️",
        "description": "Настраиваешь серверы, облако, CI/CD — отвечаешь за то, чтобы всё стабильно работало и деплоилось.",
        "course_slug": None,
    },
    "qa": {
        "title": "QA",
        "icon": "🔍",
        "description": "Находишь и предотвращаешь ошибки, продумываешь тест-кейсы, следишь за качеством продукта.",
        "course_slug": None,
    },
}

# Каждый вопрос — это (текст, список вариантов), где каждый вариант — (текст, [направления, которые он усиливает]).
QUESTION_BANK: list[tuple[str, list[tuple[str, list[str]]]]] = [
    (
        "Что тебе интереснее: то, что видит пользователь, или то, что происходит «под капотом»?",
        [
            ("Хочу создавать интерфейсы, дизайн, анимации", ["frontend"]),
            ("Хочу писать серверную логику и работать с базами данных", ["backend"]),
            ("Интересно и то, и другое — хочу строить продукт целиком", ["fullstack"]),
            ("Мне интереснее работать с числами, данными и моделями", ["data_ai"]),
        ],
    ),
    (
        "Какой проект тебе хотелось бы сделать первым?",
        [
            ("Сайт или веб-приложение с красивым интерфейсом", ["frontend"]),
            ("API и сервер для приложения", ["backend", "fullstack"]),
            ("Мобильное приложение для телефона", ["mobile"]),
            ("Скрипт, который анализирует данные и делает прогноз", ["data_ai"]),
        ],
    ),
    (
        "Что ближе по складу ума?",
        [
            ("Визуальное мышление, чувство стиля", ["frontend"]),
            ("Логика, алгоритмы, структуры данных", ["backend", "data_ai"]),
            ("Системное мышление, люблю автоматизацию процессов", ["devops"]),
            ("Внимание к деталям, люблю находить ошибки", ["qa"]),
        ],
    ),
    (
        "Как ты относишься к серверам, облаку, Docker и CI/CD?",
        [
            ("Звучит увлекательно, хочу настраивать инфраструктуру", ["devops"]),
            ("Не очень — мне больше про дизайн и код интерфейса", ["frontend"]),
            ("Интересно, но как часть серверной разработки", ["backend", "fullstack"]),
            ("Интереснее тестирование, чем инфраструктура", ["qa"]),
        ],
    ),
    (
        "Какая задача звучит увлекательнее?",
        [
            ("Найти баг в приложении и продумать тест-кейсы", ["qa"]),
            ("Обучить модель находить закономерности в данных", ["data_ai"]),
            ("Сделать приложение для iOS и Android", ["mobile"]),
            ("Сверстать адаптивный, красивый лендинг", ["frontend"]),
        ],
    ),
    (
        "Какой результат работы приносит тебе больше удовольствия?",
        [
            ("Пользователи хвалят удобный и красивый интерфейс", ["frontend"]),
            ("Система работает быстро, надёжно и без сбоев", ["backend", "devops"]),
            ("Приложение помогает людям прямо с телефона", ["mobile"]),
            ("Найденная закономерность в данных меняет решение", ["data_ai"]),
        ],
    ),
]


def get_questions() -> list[QuizQuestionOut]:
    return [
        QuizQuestionOut(question=question, options=[text for text, _ in options])
        for question, options in QUESTION_BANK
    ]


EXPLANATION_PROMPT = """Пользователь прошёл Career Path Quiz на образовательной платформе SoftLearn,
чтобы понять, какое IT-направление ему подходит.

Рекомендованное направление: {direction_title}
Описание направления: {direction_description}
Баллы по всем направлениям (чем больше, тем больше ответов пользователя указывали на это направление): {scores}

Напиши короткое (3-5 предложений), дружелюбное объяснение на русском языке, почему пользователю подходит
{direction_title}, основываясь на распределении баллов. Не упоминай слово "баллы" буквально, говори о его
склонностях и ответах. Не задавай вопросов, не предлагай решать задачи."""


async def submit_quiz(answers: list[int]) -> QuizResultOut:
    if len(answers) != len(QUESTION_BANK):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Количество ответов не совпадает с количеством вопросов",
        )

    scores: dict[str, int] = {slug: 0 for slug in DIRECTIONS}
    for answer_index, (_, options) in zip(answers, QUESTION_BANK):
        if answer_index < 0 or answer_index >= len(options):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректный ответ")
        _, directions = options[answer_index]
        for slug in directions:
            scores[slug] += 1

    top_slug = max(DIRECTIONS.keys(), key=lambda slug: scores[slug])
    direction = DIRECTIONS[top_slug]

    explanation = await ollama_service.complete(
        "Ты дружелюбный карьерный консультант образовательной платформы SoftLearn.",
        EXPLANATION_PROMPT.format(
            direction_title=direction["title"],
            direction_description=direction["description"],
            scores=scores,
        ),
    )

    return QuizResultOut(
        direction_slug=top_slug,
        direction_title=direction["title"],
        direction_icon=direction["icon"],
        description=direction["description"],
        course_slug=direction["course_slug"],
        scores=scores,
        explanation=explanation or direction["description"],
    )
