# SoftLearn — CLAUDE.md

Это главный файл-инструкция для Claude Code. Читай его перед любым действием в проекте.

---

## Что такое проект

**SoftLearn** — образовательная платформа для самоучек-программистов.

Главная проблема которую решает: самоучки теряются в море источников (YouTube, статьи, ChatGPT, форумы) и не знают по какому пути идти. SoftLearn даёт один чёткий структурированный путь — курс с определённым порядком без лишних ответвлений.

---

## Иерархия контента

```
Платформа
└── Направление (Course)          — Frontend, Backend, Fullstack, ...
    └── Стек (Stack)              — HTML&CSS, JS, TS, React, Next.js, ...
        └── Урок (Lesson)         — конкретная тема
            ├── Объяснение        — MDX контент + AI чат
            ├── Практика          — задачи для закрепления
            └── Тест-барьер       — нельзя перейти дальше без сдачи
```

---

## Пользовательский сценарий

```
1. Регистрация / Логин
        ↓
2. Онбординг: "Знаешь программирование?"
        ├── Нет  → начинает с первого стека (beginner)
        └── Да   → Вступительный тест (от лёгкого к сложному)
                        ↓
                   Уровень определён → нужные стеки разблокированы
        ↓
3. Выбор направления (можно несколько одновременно)
   Frontend / Backend / Fullstack / ...
        ↓
4. Страница курса — список стеков
   [HTML&CSS ✅] → [JS 🔒] → [TS 🔒] → [React 🔒] → [Next.js 🔒]
   Стек открывается только после сдачи теста предыдущего
   (или по результату вступительного теста)
        ↓
5. Внутри стека — список уроков
   [Урок 1 ✅] → [Урок 2 🔒] → [Урок 3 🔒] → ...
        ↓
6. Внутри урока:
   Объяснение → Практика → Тест-барьер → Следующий урок
```

---

## Монорепо структура

```
softlearn/
├── CLAUDE.md                  ← этот файл
├── .gitignore
├── frontend/                  ← Next.js 14
└── backend/                   ← FastAPI (Python)
```

---

## Технический стек

### Frontend (`/frontend`)
- **Next.js 14** — App Router, TypeScript, без `src/` директории
- **Tailwind CSS** — стили
- **shadcn/ui** — UI компоненты
- **Zustand** — глобальное состояние (прогресс, юзер)
- **KaTeX / react-katex** — рендеринг формул
- **CodeMirror 6** — редактор кода в задачах
- **Contentlayer + MDX** — контент уроков в файлах

### Backend (`/backend`)
- **FastAPI** — Python, слоистая архитектура
- **SQLAlchemy** — ORM
- **PostgreSQL** — основная БД
- **pgvector** — расширение PostgreSQL для RAG (Фаза 4)
- **Alembic** — миграции БД
- **Redis** — кэш и сессии
- **Google Gemini API** — основной AI (чат, объяснения, vision)
- **Ollama (локально)** — проверка кода и вычислений (модель: qwen2.5-coder)

---

## Архитектура бэкенда

Строго слоистая: `router → service → repository → database`

```
backend/
├── main.py                    ← точка входа, CORS, роутеры
├── .env                       ← секреты (не коммитить!)
├── core/
│   ├── config.py              ← настройки через pydantic-settings
│   └── database.py            ← SQLAlchemy engine, SessionLocal, Base
├── models/                    ← SQLAlchemy модели (таблицы БД)
│   ├── __init__.py
│   ├── user.py                ← User
│   ├── course.py              ← Course (направление)
│   ├── stack.py               ← Stack (стек внутри курса)
│   ├── lesson.py              ← Lesson (урок внутри стека)
│   ├── exercise.py            ← Exercise (задача)
│   ├── test.py                ← Test (тест-барьер)
│   ├── progress.py            ← UserProgress (прогресс по урокам)
│   ├── stack_progress.py      ← StackProgress (прогресс по стекам)
│   ├── test_result.py         ← TestResult
│   ├── chat_message.py        ← ChatMessage
│   └── placement_test.py      ← PlacementTest
├── schemas/                   ← Pydantic схемы (валидация I/O)
│   ├── __init__.py
│   ├── user.py
│   ├── course.py
│   ├── stack.py
│   ├── lesson.py
│   ├── progress.py
│   └── test_result.py
├── routers/                   ← API эндпоинты
│   ├── __init__.py
│   ├── auth.py                ← регистрация, логин, токены
│   ├── courses.py             ← курсы и стеки
│   ├── lessons.py             ← уроки
│   ├── progress.py            ← прогресс
│   ├── exercises.py           ← задачи
│   ├── tests.py               ← тесты-барьеры
│   ├── ai_chat.py             ← AI ассистент (Gemini)
│   └── placement.py           ← вступительный тест
├── services/                  ← вся бизнес-логика
│   ├── __init__.py
│   ├── auth_service.py        ← хэш паролей, JWT токены
│   ├── progress_service.py    ← логика разблокировки
│   ├── test_service.py        ← проверка тестов, подсчёт баллов
│   ├── ai_service.py          ← Gemini API, системный промпт
│   └── ollama_service.py      ← Ollama, проверка кода
└── repositories/              ← только запросы к БД
    ├── __init__.py
    ├── user_repo.py
    ├── course_repo.py
    ├── lesson_repo.py
    ├── progress_repo.py
    └── test_repo.py
```

---

## Архитектура фронтенда

```
frontend/
├── app/                            ← App Router
│   ├── layout.tsx                  ← корневой layout
│   ├── page.tsx                    ← лендинг / выбор направления
│   ├── (auth)/
│   │   ├── login/page.tsx          ← страница логина
│   │   └── register/page.tsx       ← страница регистрации
│   ├── onboarding/
│   │   └── page.tsx                ← опрос + вступительный тест
│   ├── courses/
│   │   └── [courseSlug]/
│   │       └── page.tsx            ← страница курса (список стеков)
│   ├── stacks/
│   │   └── [stackSlug]/
│   │       └── page.tsx            ← страница стека (список уроков)
│   ├── lessons/
│   │   └── [lessonSlug]/
│   │       ├── page.tsx            ← урок (объяснение + AI чат)
│   │       ├── practice/page.tsx   ← практика
│   │       └── test/page.tsx       ← тест-барьер
│   ├── placement/
│   │   └── [courseSlug]/page.tsx   ← вступительный тест
│   └── dashboard/
│       └── page.tsx                ← личный кабинет (прогресс)
├── components/
│   ├── course/                     ← карточки курсов и стеков
│   ├── lesson/                     ← контент урока + AI чат
│   ├── practice/                   ← MCQ, открытые задачи, код
│   ├── test/                       ← тест-барьер
│   └── ui/                         ← shadcn компоненты
├── lib/
│   ├── api.ts                      ← ВСЕ запросы к FastAPI отсюда
│   ├── auth.ts                     ← хелперы авторизации
│   └── utils.ts
├── store/
│   ├── auth.ts                     ← Zustand: юзер, токен
│   └── progress.ts                 ← Zustand: прогресс
└── content/                        ← MDX файлы уроков (Contentlayer)
    ├── html-css/
    │   ├── what-is-html.mdx
    │   └── ...
    ├── javascript/
    │   ├── variables.mdx
    │   └── ...
    └── typescript/
        └── ...
```

---

## Модели базы данных

### User
```
id            UUID PK
email         VARCHAR(255) UNIQUE
password_hash VARCHAR(255)
name          VARCHAR(100)
created_at    TIMESTAMP
```

### Course (направление)
```
id          UUID PK
title       VARCHAR(100)    — "Frontend разработчик"
slug        VARCHAR(50)     — "frontend"
description TEXT
icon        VARCHAR(50)     — эмодзи или иконка
order       INTEGER         — порядок на главной
created_at  TIMESTAMP
```

### Stack (стек внутри курса)
```
id          UUID PK
title       VARCHAR(100)    — "HTML & CSS"
slug        VARCHAR(50)     — "html-css"
description TEXT
order       INTEGER         — порядок внутри курса
course_id   UUID FK → Course
created_at  TIMESTAMP
```

### Lesson (урок внутри стека)
```
id          UUID PK
title       VARCHAR(200)
slug        VARCHAR(100)
content     TEXT            — MDX контент урока
order       INTEGER         — порядок внутри стека
stack_id    UUID FK → Stack
created_at  TIMESTAMP
updated_at  TIMESTAMP
```

### Exercise (задача для практики)
```
id          UUID PK
type        ENUM(mcq, open, code)
question    TEXT
answer      TEXT
options     JSON            — варианты для mcq: ["A","B","C","D"]
explanation TEXT            — объяснение правильного ответа
lesson_id   UUID FK → Lesson
order       INTEGER
```

### Test (тест-барьер урока)
```
id              UUID PK
lesson_id       UUID FK → Lesson   — один к одному
pass_threshold  INTEGER            — минимальный % (default: 70)
questions       JSON               — список вопросов теста
time_limit      INTEGER            — минуты (nullable)
```

### UserProgress (прогресс по уроку)
```
id              UUID PK
user_id         UUID FK → User
lesson_id       UUID FK → Lesson
status          ENUM(locked, in_progress, completed)
lesson_read     BOOLEAN  DEFAULT false
practice_done   BOOLEAN  DEFAULT false
updated_at      TIMESTAMP
```

### StackProgress (прогресс по стеку)
```
id          UUID PK
user_id     UUID FK → User
stack_id    UUID FK → Stack
status      ENUM(locked, in_progress, completed)
unlocked_at TIMESTAMP
```

### TestResult (результат теста)
```
id          UUID PK
user_id     UUID FK → User
test_id     UUID FK → Test
score       INTEGER         — 0–100
passed      BOOLEAN
mistakes    JSON            — [{question, user_answer, correct_answer}]
attempt     INTEGER
created_at  TIMESTAMP
```

### ChatMessage (история AI чата)
```
id          UUID PK
user_id     UUID FK → User
lesson_id   UUID FK → Lesson
role        ENUM(user, assistant)
content     TEXT
created_at  TIMESTAMP
```

### PlacementTest (вступительный тест)
```
id              UUID PK
user_id         UUID FK → User
course_id       UUID FK → Course
result_level    ENUM(beginner, intermediate, advanced)
score           INTEGER
answers         JSON
completed_at    TIMESTAMP
```

---

## API эндпоинты

Все роуты с префиксом `/api/`

### Авторизация
```
POST /api/auth/register          — регистрация {email, password, name}
POST /api/auth/login             — логин → JWT токен
GET  /api/auth/me                — данные текущего юзера
POST /api/auth/logout            — выход
```

### Курсы и стеки
```
GET  /api/courses                          — список всех направлений
GET  /api/courses/{slug}                   — детали курса
GET  /api/courses/{slug}/stacks            — стеки курса с прогрессом юзера
GET  /api/stacks/{slug}                    — детали стека
GET  /api/stacks/{slug}/lessons            — уроки стека с прогрессом
```

### Уроки
```
GET   /api/lessons/{slug}                  — контент урока
PATCH /api/lessons/{slug}/read             — отметить урок как прочитанный
```

### Прогресс
```
GET   /api/progress                        — весь прогресс юзера
GET   /api/progress/stacks                 — прогресс по стекам
PATCH /api/progress/lessons/{slug}         — обновить статус урока
```

### Практика
```
GET  /api/lessons/{slug}/exercises         — задачи урока
POST /api/exercises/{id}/check             — проверить ответ
```

### Тест-барьер
```
GET  /api/lessons/{slug}/test              — получить тест
POST /api/lessons/{slug}/test/submit       — отправить ответы → результат
GET  /api/lessons/{slug}/test/results      — история попыток
```

### AI чат (Gemini)
```
POST   /api/chat/{lesson_slug}             — сообщение (стриминг SSE)
GET    /api/chat/{lesson_slug}/history     — история диалога
DELETE /api/chat/{lesson_slug}/history     — очистить историю
POST   /api/chat/{lesson_slug}/image       — анализ фото (vision)
```

### Вступительный тест
```
GET  /api/placement/{course_slug}          — вопросы теста
POST /api/placement/{course_slug}/submit   — результат → разблокировка стеков
```

---

## Авторизация

- **JWT токены** (access token в заголовке `Authorization: Bearer <token>`)
- Пароли хэшируются через `bcrypt`
- Библиотеки: `python-jose`, `passlib[bcrypt]`
- Все защищённые эндпоинты требуют токен (через FastAPI Depends)
- На фронте токен хранится в Zustand store (`/store/auth.ts`) и добавляется в каждый запрос через `api.ts`

---

## AI интеграция

### Google Gemini API (`/backend/services/ai_service.py`)
- Модель: `gemini-2.0-flash`
- Используется для: AI-чат в уроке, объяснение по-другому, анализ фото задачи (vision)
- Стриминг через SSE (`Server-Sent Events`)
- Системный промпт ограничен контентом текущего урока

```python
SYSTEM_PROMPT = """
Ты AI-ассистент образовательной платформы SoftLearn.
Помогаешь пользователю разобраться с темой: {lesson_title}

Контент урока:
{lesson_content}

ПРАВИЛА:
- Отвечай ТОЛЬКО по теме этого урока
- Если вопрос не по теме — вежливо объясни это
- Объясняй просто, с примерами кода
- Можешь объяснить иначе если не понял
- Проверяй правильность рассуждений пользователя
"""
```

### Ollama (`/backend/services/ollama_service.py`)
- Модель: `qwen2.5-coder` — специализированная для кода
- Используется для: запуск и проверка кода пользователя, валидация ответов на задачи с кодом
- Endpoint: `http://localhost:11434`
- Запускается локально: `ollama run qwen2.5-coder`

---

## Contentlayer + MDX

Контент уроков — MDX файлы в `/frontend/content/`.

Каждый файл:
```mdx
---
title: "Что такое переменная в JavaScript"
slug: "js-variables"
stack: "javascript"
order: 1
---

## Что такое переменная

Переменная — это именованная ячейка памяти...

```javascript
let name = "Alice";
const age = 25;
```

<InfoBlock>
  Используй `const` по умолчанию, `let` когда значение меняется.
</InfoBlock>
```

---

## Переменные окружения

### `/backend/.env`
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/softlearn
REDIS_URL=redis://localhost:6379
GEMINI_API_KEY=твой_ключ_из_google_ai_studio
OLLAMA_URL=http://localhost:11434
SECRET_KEY=случайная_строка_для_jwt
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### `/frontend/.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Правила написания кода

### Общие
- Все запросы с фронта идут ТОЛЬКО через `/frontend/lib/api.ts`
- Никаких прямых `fetch()` в компонентах
- Проверка прогресса и разблокировки — только на сервере, не на клиенте
- Секреты только в `.env`, никогда в коде

### Бэкенд
- Роутер принимает запрос → вызывает сервис. Никакой логики в роутере
- Вся бизнес-логика в `services/`
- Все запросы к БД только через `repositories/`
- Каждый эндпоинт возвращает Pydantic схему — не SQLAlchemy объект
- Все защищённые роуты используют `Depends(get_current_user)`
- Префикс всех роутов: `/api/`

### Фронтенд
- Строгая типизация TypeScript везде
- Состояние через Zustand (`/store/`)
- Защищённые страницы проверяют токен через middleware
- Редактор кода — CodeMirror 6, не `<textarea>`
- Формулы — `react-katex`, не MathJax

### Git
- Коммит после каждой рабочей фичи
- Формат: `feat: добавлен POST /api/auth/register`

---

## Фазы разработки

### ✅ Фаза 0 (завершена)
- Структура папок создана
- Next.js и зависимости установлены
- Репозиторий на GitHub

### 🔄 Фаза 1 (текущая) — Скелет + Авторизация
1. `backend/core/database.py` — подключение к PostgreSQL
2. `backend/core/config.py` — pydantic-settings
3. `backend/models/` — User, Course, Stack, Lesson, UserProgress, StackProgress
4. `backend/routers/auth.py` — регистрация и логин (JWT)
5. `backend/routers/courses.py` — GET /api/courses, GET /api/courses/{slug}/stacks
6. `backend/main.py` — FastAPI + CORS + роутеры
7. `frontend/lib/api.ts` — базовый API клиент с токеном
8. `frontend/store/auth.ts` — Zustand auth store
9. `frontend/app/(auth)/` — страницы логина и регистрации
10. `frontend/app/courses/[courseSlug]/page.tsx` — страница курса со стеками

### Фаза 2 — Уроки + AI чат
- Contentlayer настройка
- MDX рендеринг с KaTeX
- Страница урока
- Gemini AI чат со стримингом
- Vision (анализ фото)

### Фаза 3 — Практика + Тест-барьер
- CodeMirror 6 редактор
- Три типа задач (MCQ, открытый, код)
- Тест-барьер и логика разблокировки стеков
- Ollama для проверки кода

### Фаза 4 — Вступительный тест + Онбординг
- Онбординг (вопрос про опыт)
- Вступительный тест от лёгкого к сложному
- Автоматическая разблокировка стеков по результату
- pgvector + RAG для AI
- Redis кэширование

### Фаза 5 — Полировка
- Dashboard с прогрессом
- Несколько направлений (Frontend, Backend, Fullstack)
- Мобильная адаптация
- Деплой

---

## Запуск локально

```bash
# Бэкенд
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000

# Фронтенд
cd frontend
npm run dev

# Ollama
ollama run qwen2.5-coder
```

---

## Текущий статус

Работаем над **Фазой 1**.
Следующий шаг: `backend/core/database.py` и `backend/core/config.py`
