"""Заполняет БД реальным контентом для курсов Frontend и Backend.

Запуск: python scripts/seed.py
Источники для контента: developer.mozilla.org (HTML/CSS/JS), docs.python.org,
fastapi.tiangolo.com — факты проверены через веб-поиск перед написанием.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.database import Base, SessionLocal, engine
from models.course import Course
from models.exercise import Exercise, ExerciseType
from models.lesson import Lesson
from models.stack import Stack
from models.test import Test

COURSES = [
    {
        "title": "Frontend разработчик",
        "slug": "frontend",
        "description": "Путь от верстки до интерактивных интерфейсов: HTML, CSS, JavaScript.",
        "icon": "🎨",
        "order": 1,
        "stacks": [
            {
                "title": "HTML & CSS",
                "slug": "html-css",
                "description": "Структура страницы и её оформление.",
                "order": 1,
                "lessons": [
                    {
                        "title": "Что такое HTML и семантическая разметка",
                        "slug": "html-intro",
                        "order": 1,
                        "youtube_url": "https://www.youtube.com/watch?v=W4MIiV4nZDY",
                        "duration_minutes": 15,
                        "content": """## Что такое HTML

HTML (HyperText Markup Language) — язык разметки, который описывает структуру
веб-страницы с помощью элементов (тегов). Каждый элемент сообщает браузеру,
что это за часть контента: заголовок, абзац, изображение, список и т.д.

## Семантические элементы

Семантические теги, в отличие от `<div>` и `<span>`, явно описывают смысл
содержимого — это помогает браузерам, поисковикам и программам экранного
доступа понимать структуру страницы.

- `<header>` — шапка страницы или секции (логотип, навигация, заголовок)
- `<nav>` — блок навигационных ссылок
- `<main>` — основной контент страницы (только один на странице)
- `<section>` — тематическая секция контента
- `<article>` — самостоятельный, независимый блок (статья, пост, карточка товара)
- `<footer>` — подвал страницы или секции

## Пример

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <title>Моя страница</title>
  </head>
  <body>
    <header>
      <h1>SoftLearn</h1>
      <nav>
        <a href="/courses">Курсы</a>
      </nav>
    </header>
    <main>
      <article>
        <h2>Первый урок</h2>
        <p>Учимся писать семантический HTML.</p>
      </article>
    </main>
    <footer>
      <p>&copy; 2026 SoftLearn</p>
    </footer>
  </body>
</html>
```

Почему это важно: семантическая разметка улучшает доступность (screen readers
понимают структуру), SEO (поисковики точнее индексируют контент) и читаемость
кода для других разработчиков.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какой тег используют для основного уникального контента страницы?",
                                "options": ["<div>", "<main>", "<span>", "<section>"],
                                "answer": "<main>",
                                "explanation": "<main> обозначает основной контент и должен встречаться один раз на странице.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Объясните своими словами, почему семантический HTML лучше, чем верстка на одних <div>.",
                                "answer": "Семантические теги передают смысл контента браузеру, поисковикам и screen reader'ам, улучшая доступность и SEO.",
                                "explanation": "Главное — упомянуть доступность (accessibility) и/или SEO.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите разметку страницы с <header>, <nav>, <main> и <footer>.",
                                "answer": "<header>...</header><nav>...</nav><main>...</main><footer>...</footer>",
                                "explanation": "Важен порядок и использование именно семантических тегов, а не <div>.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какой тег предназначен для навигационных ссылок?",
                                    "options": ["<nav>", "<menu>", "<links>", "<header>"],
                                    "answer": "<nav>",
                                },
                                {
                                    "question": "Сколько элементов <main> может быть на странице?",
                                    "options": ["Сколько угодно", "Один", "Два", "Ноль"],
                                    "answer": "Один",
                                },
                                {
                                    "question": "Какой тег используют для независимого самостоятельного блока контента (например, статьи)?",
                                    "options": ["<article>", "<section>", "<div>", "<aside>"],
                                    "answer": "<article>",
                                },
                                {
                                    "question": "Что из этого НЕ является семантическим элементом?",
                                    "options": ["<footer>", "<section>", "<div>", "<article>"],
                                    "answer": "<div>",
                                },
                                {
                                    "question": "Зачем нужна семантическая разметка?",
                                    "options": [
                                        "Только для красоты кода",
                                        "Для доступности и SEO",
                                        "Она ускоряет загрузку CSS",
                                        "Без неё браузер не отрендерит страницу",
                                    ],
                                    "answer": "Для доступности и SEO",
                                },
                            ],
                        },
                    },
                    {
                        "title": "CSS и блочная модель (box model)",
                        "slug": "css-box-model",
                        "order": 2,
                        "youtube_url": "https://www.youtube.com/watch?v=oHDvqBv62JY",
                        "duration_minutes": 12,
                        "content": """## Что такое CSS

CSS (Cascading Style Sheets) описывает, как должны выглядеть HTML-элементы:
цвета, отступы, размеры, расположение на странице.

## Блочная модель (box model)

Каждый HTML-элемент представляется браузером как прямоугольная коробка,
состоящая из четырёх слоёв (снаружи внутрь):

- **margin** — внешний отступ, пространство вокруг границы элемента, не входит
  в размер самого элемента
- **border** — граница вокруг padding и содержимого
- **padding** — внутренний отступ вокруг контента
- **content** — сам контент (текст, изображение и т.д.)

## box-sizing

По умолчанию `width` и `height` задают размер только content-области, а
border и padding добавляются сверху. Чтобы border и padding включались в
заданную ширину/высоту, используют:

```css
* {
  box-sizing: border-box;
}
```

## Пример

```css
.card {
  width: 300px;
  padding: 16px;
  border: 1px solid #ddd;
  margin: 12px;
  box-sizing: border-box;
}
```

С `box-sizing: border-box` итоговая ширина `.card` останется 300px, включая
padding и border — это самый предсказуемый способ верстать макет.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Что находится между content и border?",
                                "options": ["margin", "padding", "outline", "gap"],
                                "answer": "padding",
                                "explanation": "Порядок снаружи внутрь: margin → border → padding → content.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Зачем используют box-sizing: border-box?",
                                "answer": "Чтобы padding и border включались в заданную ширину/высоту элемента, а не добавлялись сверху.",
                                "explanation": "Ключевая мысль — предсказуемость итогового размера элемента.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите CSS-класс .box шириной 200px, с padding 10px и border 2px solid black, используя box-sizing: border-box.",
                                "answer": ".box { width: 200px; padding: 10px; border: 2px solid black; box-sizing: border-box; }",
                                "explanation": "Главное — указать все четыре свойства и box-sizing.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какой слой находится снаружи border?",
                                    "options": ["padding", "margin", "content", "outline"],
                                    "answer": "margin",
                                },
                                {
                                    "question": "Margin влияет на итоговый размер самого элемента?",
                                    "options": ["Да, увеличивает width", "Нет, только на пространство вокруг", "Да, уменьшает height", "Margin — это синоним padding"],
                                    "answer": "Нет, только на пространство вокруг",
                                },
                                {
                                    "question": "Что делает box-sizing: border-box?",
                                    "options": [
                                        "Убирает border",
                                        "Включает padding и border в заданную width/height",
                                        "Добавляет тень элементу",
                                        "Меняет порядок margin и padding",
                                    ],
                                    "answer": "Включает padding и border в заданную width/height",
                                },
                                {
                                    "question": "По умолчанию (content-box) что добавляется к width сверху?",
                                    "options": ["Ничего", "padding и border", "только margin", "только border"],
                                    "answer": "padding и border",
                                },
                                {
                                    "question": "Padding находится...",
                                    "options": ["снаружи margin", "между border и content", "внутри content", "между margin и border"],
                                    "answer": "между border и content",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Flexbox: гибкая раскладка элементов",
                        "slug": "css-flexbox",
                        "order": 3,
                        "youtube_url": "https://www.youtube.com/watch?v=JJSoEo8JSnc",
                        "duration_minutes": 18,
                        "content": """## Что такое Flexbox

Flexbox (Flexible Box Layout) — модель CSS для расположения элементов в
строку или столбец с гибким распределением свободного места. Включается на
родительском элементе через `display: flex`.

## Основные свойства контейнера

```css
.container {
  display: flex;
  flex-direction: row;       /* row | column | row-reverse | column-reverse */
  justify-content: center;   /* выравнивание по главной оси */
  align-items: center;       /* выравнивание по поперечной оси */
  gap: 16px;                 /* расстояние между элементами */
}
```

- `flex-direction` задаёт главную ось — строка или столбец
- `justify-content` распределяет элементы вдоль главной оси (`flex-start`,
  `center`, `space-between`, `space-around`)
- `align-items` выравнивает элементы по поперечной оси (`stretch`, `center`,
  `flex-start`, `flex-end`)

## Свойства элементов

```css
.item {
  flex-grow: 1;    /* насколько элемент растягивается, заполняя пространство */
  flex-shrink: 1;  /* насколько элемент сжимается при нехватке места */
  flex-basis: 200px; /* базовый размер элемента */
}
```

Сокращённая запись: `flex: 1 1 200px;` (grow shrink basis).

## Пример: карточки в ряд

```css
.cards {
  display: flex;
  gap: 20px;
}
.card {
  flex: 1;
}
```

Все `.card` займут равную часть доступной ширины `.cards`.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какое свойство выравнивает элементы вдоль главной оси flex-контейнера?",
                                "options": ["align-items", "justify-content", "flex-direction", "gap"],
                                "answer": "justify-content",
                                "explanation": "justify-content работает по главной оси, align-items — по поперечной.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Чем отличаются align-items и justify-content?",
                                "answer": "justify-content выравнивает элементы по главной оси (направление flex-direction), align-items — по поперечной (перпендикулярной) оси.",
                                "explanation": "Ключевое — разные оси выравнивания.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите CSS для .row: flex-контейнер с элементами в ряд, расстоянием 12px и центрированием по обеим осям.",
                                "answer": ".row { display: flex; justify-content: center; align-items: center; gap: 12px; }",
                                "explanation": "Важны display: flex, justify-content: center, align-items: center.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Каким свойством включают flexbox на контейнере?",
                                    "options": ["display: flex", "position: flex", "flex: on", "layout: flex"],
                                    "answer": "display: flex",
                                },
                                {
                                    "question": "Какое значение flex-direction располагает элементы в столбец?",
                                    "options": ["row", "column", "wrap", "stack"],
                                    "answer": "column",
                                },
                                {
                                    "question": "Что задаёт flex-grow?",
                                    "options": [
                                        "Насколько элемент сжимается",
                                        "Насколько элемент растягивается, заполняя свободное место",
                                        "Цвет фона элемента",
                                        "Порядок элемента",
                                    ],
                                    "answer": "Насколько элемент растягивается, заполняя свободное место",
                                },
                                {
                                    "question": "Какое свойство задаёт расстояние между flex-элементами?",
                                    "options": ["margin", "gap", "padding", "space"],
                                    "answer": "gap",
                                },
                                {
                                    "question": "Сокращённая запись flex: 1 1 200px означает:",
                                    "options": [
                                        "grow shrink basis",
                                        "basis grow shrink",
                                        "только basis",
                                        "только grow",
                                    ],
                                    "answer": "grow shrink basis",
                                },
                            ],
                        },
                    },
                    {
                        "title": "CSS Grid: раскладка по сетке",
                        "slug": "css-grid",
                        "order": 4,
                        "youtube_url": "https://www.youtube.com/watch?v=hs3piaN4b5I",
                        "duration_minutes": 15,
                        "content": """## Что такое CSS Grid

CSS Grid — двумерная система раскладки: позволяет располагать элементы
одновременно по строкам и столбцам, в отличие от одномерного Flexbox.

## Создание сетки

```css
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto;
  gap: 16px;
}
```

`repeat(3, 1fr)` создаёт три равные колонки. `fr` — доля свободного места
(fraction unit).

## Размещение элементов

```css
.item {
  grid-column: 1 / 3;  /* занимает колонки с 1 по 2 */
  grid-row: 1 / 2;
}
```

## Адаптивная сетка без media-запросов

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
```

`auto-fit` с `minmax` автоматически меняет количество колонок в зависимости
от ширины контейнера — карточки минимум 200px, но растягиваются, заполняя
ряд.

## Когда Grid, а когда Flexbox

Flexbox удобен для одномерных раскладок (навигация, ряд карточек). Grid —
для двумерных макетов (страница целиком: шапка, сайдбар, контент, подвал).""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Чем Grid принципиально отличается от Flexbox?",
                                "options": [
                                    "Grid двумерный (строки и колонки), Flexbox одномерный",
                                    "Grid работает только в столбик",
                                    "Flexbox новее, чем Grid",
                                    "Между ними нет разницы",
                                ],
                                "answer": "Grid двумерный (строки и колонки), Flexbox одномерный",
                                "explanation": "Grid управляет и строками, и колонками одновременно.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Что делает grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))?",
                                "answer": "Создаёт адаптивное число колонок шириной минимум 200px, которые растягиваются и заполняют доступное пространство без media-запросов.",
                                "explanation": "Ключевое — auto-fit + minmax дают адаптивность без @media.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите CSS для .grid: сетка из 2 равных колонок с gap 10px.",
                                "answer": ".grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }",
                                "explanation": "Важны display: grid и repeat(2, 1fr).",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какая единица измерения означает долю свободного места в Grid?",
                                    "options": ["px", "fr", "em", "%"],
                                    "answer": "fr",
                                },
                                {
                                    "question": "Какое свойство включает CSS Grid на контейнере?",
                                    "options": ["display: grid", "grid: on", "layout: grid", "position: grid"],
                                    "answer": "display: grid",
                                },
                                {
                                    "question": "Что создаёт repeat(3, 1fr)?",
                                    "options": [
                                        "3 равные колонки",
                                        "1 колонку шириной 3fr",
                                        "3 строки",
                                        "Ошибку синтаксиса",
                                    ],
                                    "answer": "3 равные колонки",
                                },
                                {
                                    "question": "Для какой задачи Grid подходит лучше, чем Flexbox?",
                                    "options": [
                                        "Ряд кнопок в навигации",
                                        "Двумерный макет всей страницы",
                                        "Центрирование одного элемента",
                                        "Анимация при наведении",
                                    ],
                                    "answer": "Двумерный макет всей страницы",
                                },
                                {
                                    "question": "Что задаёт grid-column: 1 / 3?",
                                    "options": [
                                        "Элемент занимает колонки с 1 по 2",
                                        "Элемент находится в 3 колонке",
                                        "Элемент занимает 3 строки",
                                        "Ошибка синтаксиса",
                                    ],
                                    "answer": "Элемент занимает колонки с 1 по 2",
                                },
                            ],
                        },
                    },
                    {
                        "title": "CSS переменные и псевдоклассы",
                        "slug": "css-variables-pseudo",
                        "order": 5,
                        "youtube_url": "https://www.youtube.com/watch?v=GcNyynkoTYY",
                        "duration_minutes": 14,
                        "content": """## CSS custom properties (переменные)

CSS переменные (custom properties) позволяют хранить значения в одном месте
и использовать их по всему файлу через `var()`.

```css
:root {
  --color-primary: #6366f1;
  --spacing-md: 16px;
  --border-radius: 8px;
}

.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
}
```

Объявляйте глобальные переменные в `:root` — они доступны везде в документе.
Переменные можно переопределять внутри компонентов для тем (светлая/тёмная).

## Псевдоклассы

Псевдоклассы применяют стили в зависимости от состояния элемента или его
позиции в DOM — без добавления лишних классов в HTML.

```css
a:hover   { color: var(--color-primary); }
input:focus { outline: 2px solid var(--color-primary); }
button:disabled { opacity: 0.5; cursor: not-allowed; }

li:first-child  { font-weight: bold; }
li:last-child   { border-bottom: none; }
li:nth-child(2n) { background: #f5f5f5; }  /* чётные строки */
p:not(.special) { color: #666; }            /* все кроме .special */
```

## Псевдоэлементы

```css
.quote::before { content: "«"; color: var(--color-primary); }
.quote::after  { content: "»"; color: var(--color-primary); }

p::first-line  { font-weight: bold; }
```

`::before` и `::after` создают виртуальный элемент внутри реального —
удобны для декоративных деталей без лишнего HTML.

## Пример: тёмная тема через переменные

```css
:root {
  --bg: #ffffff;
  --text: #111111;
}

[data-theme="dark"] {
  --bg: #1a1a1a;
  --text: #f0f0f0;
}

body {
  background: var(--bg);
  color: var(--text);
}
```

При добавлении атрибута `data-theme="dark"` на `<html>` все цвета меняются
автоматически — без дублирования стилей.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Где принято объявлять глобальные CSS-переменные?",
                                "options": [":root", "body", "html", "*"],
                                "answer": ":root",
                                "explanation": ":root соответствует корневому <html> и имеет максимальную специфичность среди псевдоклассов, что делает его стандартным местом для глобальных переменных.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Чем псевдоэлемент ::before отличается от псевдокласса :hover?",
                                "answer": "::before создаёт виртуальный DOM-элемент внутри реального, добавляя контент через CSS. :hover — это состояние элемента при наведении курсора, к которому применяют стили. Одно создаёт элемент, другое реагирует на состояние.",
                                "explanation": "Ключевое: ::before/::after создают элементы; :hover/:focus/:disabled реагируют на состояние.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Объявите CSS-переменную --color-main со значением #ff6b6b в :root и примените её к цвету текста .title.",
                                "answer": ":root { --color-main: #ff6b6b; }\n.title { color: var(--color-main); }",
                                "explanation": "Важны объявление в :root и применение через var().",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Как обратиться к CSS-переменной --spacing в свойстве?",
                                    "options": ["$(--spacing)", "var(--spacing)", "&spacing", "#spacing"],
                                    "answer": "var(--spacing)",
                                },
                                {
                                    "question": "Какой псевдокласс применяет стиль при наведении курсора?",
                                    "options": [":focus", ":active", ":hover", ":visited"],
                                    "answer": ":hover",
                                },
                                {
                                    "question": "li:nth-child(2n) выбирает...",
                                    "options": ["Только второй li", "Все нечётные li", "Все чётные li", "Каждый третий li"],
                                    "answer": "Все чётные li",
                                },
                                {
                                    "question": "Что создаёт ::before?",
                                    "options": [
                                        "Стиль для предыдущего элемента",
                                        "Виртуальный элемент перед содержимым",
                                        "Псевдокласс для состояния",
                                        "Новый HTML-тег",
                                    ],
                                    "answer": "Виртуальный элемент перед содержимым",
                                },
                                {
                                    "question": "p:not(.special) применяет стиль к...",
                                    "options": [
                                        "Только .special абзацам",
                                        "Всем абзацам, кроме .special",
                                        "Всем элементам, кроме p",
                                        "Ничему — синтаксическая ошибка",
                                    ],
                                    "answer": "Всем абзацам, кроме .special",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Адаптивная верстка: медиазапросы",
                        "slug": "css-responsive",
                        "order": 6,
                        "youtube_url": "https://www.youtube.com/watch?v=bn-DQznEZGk",
                        "duration_minutes": 16,
                        "content": """## Viewport и meta-тег

Первым делом добавляем в `<head>` тег viewport, чтобы мобильный браузер
не масштабировал страницу:

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

Без него мобильный браузер отрисует страницу в "десктопном" режиме и уменьшит.

## @media запросы

Медиазапросы применяют CSS только при определённых условиях.

```css
/* Mobile-first: базовый — мобильный */
.container {
  padding: 16px;
}

@media (min-width: 768px) {
  .container { padding: 32px; }  /* планшеты */
}

@media (min-width: 1200px) {
  .container { padding: 64px; }  /* десктопы */
}
```

## Mobile-first vs Desktop-first

**Mobile-first** (`min-width`) — начинаем с мобильного стиля, расширяем.
**Desktop-first** (`max-width`) — начинаем с десктопа, перегружаем для мобильных.

Рекомендуется mobile-first: мобильный трафик преобладает, браузер загружает
меньше CSS на слабых устройствах.

## Адаптивная типографика с clamp()

```css
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
}
```

`clamp(min, ideal, max)` автоматически масштабирует шрифт между минимальным
и максимальным значением в зависимости от ширины экрана — без медиазапросов.

## Адаптивная сетка

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}
```

На маленьком экране будет 1 колонка, на большом — столько, сколько влезет.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какой подход в медиазапросах рекомендуется использовать?",
                                "options": ["Desktop-first (max-width)", "Mobile-first (min-width)", "Оба одинаково", "Только clamp()"],
                                "answer": "Mobile-first (min-width)",
                                "explanation": "Mobile-first удобен, потому что мобильный трафик преобладает и браузер загружает меньше CSS на слабых устройствах.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Зачем нужен тег <meta name='viewport'> на мобильных устройствах?",
                                "answer": "Без него мобильный браузер считает ширину страницы десктопной (~980px) и уменьшает всё в масштаб — текст становится нечитаемым. Тег сообщает браузеру использовать реальную ширину устройства.",
                                "explanation": "Ключевое — без viewport браузер масштабирует страницу как десктопную.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите медиазапрос, меняющий font-size у body с 14px (мобильный) до 16px при ширине от 768px.",
                                "answer": "body { font-size: 14px; }\n@media (min-width: 768px) {\n  body { font-size: 16px; }\n}",
                                "explanation": "Важны mobile-first подход и правильный синтаксис @media (min-width:...).",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какой синтаксис применяет стиль при ширине экрана от 768px?",
                                    "options": [
                                        "@media (min-width: 768px)",
                                        "@media (max-width: 768px)",
                                        "@screen (768px)",
                                        "@responsive (min: 768px)",
                                    ],
                                    "answer": "@media (min-width: 768px)",
                                },
                                {
                                    "question": "Что делает clamp(1rem, 2vw, 2rem) для font-size?",
                                    "options": [
                                        "Фиксирует размер на 2vw всегда",
                                        "Масштабирует шрифт от 1rem до 2rem в зависимости от ширины",
                                        "Применяет только на мобильных",
                                        "Это не валидный CSS",
                                    ],
                                    "answer": "Масштабирует шрифт от 1rem до 2rem в зависимости от ширины",
                                },
                                {
                                    "question": "Mobile-first использует...",
                                    "options": ["max-width в медиазапросах", "min-width в медиазапросах", "только px единицы", "только vw единицы"],
                                    "answer": "min-width в медиазапросах",
                                },
                                {
                                    "question": "Зачем нужен meta viewport?",
                                    "options": [
                                        "Для SEO оптимизации",
                                        "Чтобы мобильный браузер использовал реальную ширину устройства",
                                        "Для подключения CSS файла",
                                        "Он нужен только для десктопов",
                                    ],
                                    "answer": "Чтобы мобильный браузер использовал реальную ширину устройства",
                                },
                                {
                                    "question": "grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)) делает сетку...",
                                    "options": [
                                        "Всегда с 1 колонкой",
                                        "Всегда с 4 колонками",
                                        "Адаптивной — количество колонок зависит от ширины контейнера",
                                        "Это не работает без медиазапросов",
                                    ],
                                    "answer": "Адаптивной — количество колонок зависит от ширины контейнера",
                                },
                            ],
                        },
                    },
                ],
            },
            {
                "title": "JavaScript",
                "slug": "javascript",
                "description": "Логика и интерактивность веб-страниц.",
                "order": 2,
                "lessons": [
                    {
                        "title": "Переменные: let, const и var",
                        "slug": "js-variables",
                        "order": 1,
                        "youtube_url": "https://www.youtube.com/watch?v=VlZxmKLnBCk",
                        "duration_minutes": 14,
                        "content": """## Объявление переменных

В JavaScript есть три способа объявить переменную: `var`, `let` и `const`.

## var

`var` — самый старый способ. Переменные `var` имеют функциональную область
видимости (function scope), а не блочную, и поднимаются (hoisting) с
инициализацией `undefined`. Их можно переобъявлять и менять.

## let

`let` имеет блочную область видимости (block scope) — доступна только внутри
`{ }`, где объявлена. Значение можно менять, но нельзя повторно объявить в
той же области видимости.

## const

`const` — тоже блочная область видимости, но значение нельзя переназначить
после инициализации, и объявлять `const` без значения нельзя.

```javascript
let age = 25;
age = 26; // ок

const name = "Alice";
name = "Bob"; // ошибка: Assignment to constant variable

if (true) {
  var x = 1;
  let y = 2;
}
console.log(x); // 1 — var "вытекает" из блока
console.log(y); // ReferenceError — let доступна только в блоке
```

## Что использовать

По умолчанию используйте `const`. Если значение переменной будет меняться —
используйте `let`. От `var` в новом коде стоит отказаться.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какая переменная не может быть переназначена после инициализации?",
                                "options": ["var", "let", "const", "все одинаковы"],
                                "answer": "const",
                                "explanation": "const запрещает повторное присваивание.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "В чём разница в области видимости между var и let?",
                                "answer": "var имеет функциональную область видимости, let — блочную (видна только внутри { }, где объявлена).",
                                "explanation": "Ключевое слово — block scope vs function scope.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Объявите константу PI со значением 3.14 и переменную radius, которую можно менять.",
                                "answer": "const PI = 3.14;\nlet radius = 5;",
                                "explanation": "PI должна быть const, radius — let.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какую область видимости имеет let?",
                                    "options": ["Блочную", "Функциональную", "Глобальную всегда", "Модульную"],
                                    "answer": "Блочную",
                                },
                                {
                                    "question": "Можно ли переобъявить let-переменную в той же области видимости?",
                                    "options": ["Да", "Нет", "Только если это число", "Только внутри функции"],
                                    "answer": "Нет",
                                },
                                {
                                    "question": "const обязательно нужно...",
                                    "options": [
                                        "оставлять без значения",
                                        "инициализировать при объявлении",
                                        "объявлять внутри var",
                                        "переобъявлять каждый раз",
                                    ],
                                    "answer": "инициализировать при объявлении",
                                },
                                {
                                    "question": "Чем var инициализируется при hoisting?",
                                    "options": ["null", "undefined", "0", "ничем, будет ошибка"],
                                    "answer": "undefined",
                                },
                                {
                                    "question": "Какую переменную рекомендуют использовать по умолчанию?",
                                    "options": ["var", "let", "const", "любую"],
                                    "answer": "const",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Функции в JavaScript",
                        "slug": "js-functions",
                        "order": 2,
                        "youtube_url": "https://www.youtube.com/watch?v=gigtS01tZin",
                        "duration_minutes": 16,
                        "content": """## Функции

Функция — это блок кода, который можно вызывать многократно. В JavaScript
есть несколько способов объявить функцию.

## Function Declaration

```javascript
function sum(a, b) {
  return a + b;
}
```

Такие функции поднимаются (hoisting) — их можно вызвать до объявления в коде.

## Function Expression

```javascript
const sum = function (a, b) {
  return a + b;
};
```

## Стрелочные функции (arrow functions)

```javascript
const sum = (a, b) => a + b;
```

Стрелочные функции не имеют своего `this` — они берут `this` из окружающего
контекста, что удобно внутри методов и колбэков.

## Параметры по умолчанию и rest

```javascript
function greet(name = "Гость") {
  return `Привет, ${name}!`;
}

function sumAll(...numbers) {
  return numbers.reduce((acc, n) => acc + n, 0);
}
```

Функции — основной инструмент для повторного использования логики и
разбиения программы на понятные части.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какой тип функции не имеет собственного this?",
                                "options": ["Function Declaration", "Function Expression", "Arrow function", "Все имеют свой this"],
                                "answer": "Arrow function",
                                "explanation": "Стрелочные функции берут this из внешнего контекста.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Чем отличается function declaration от function expression?",
                                "answer": "Declaration поднимается (hoisting) и доступна до объявления в коде, expression — нет.",
                                "explanation": "Ключевое слово — hoisting.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите стрелочную функцию multiply, перемножающую два числа.",
                                "answer": "const multiply = (a, b) => a * b;",
                                "explanation": "Должна быть именно arrow function.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какие функции можно вызвать раньше их объявления в коде?",
                                    "options": ["Arrow function", "Function Expression", "Function Declaration", "Никакие"],
                                    "answer": "Function Declaration",
                                },
                                {
                                    "question": "Как записать параметр со значением по умолчанию?",
                                    "options": ["function f(a = 1)", "function f(a := 1)", "function f(a == 1)", "function f(default a = 1)"],
                                    "answer": "function f(a = 1)",
                                },
                                {
                                    "question": "Что собирает rest-параметр (...args)?",
                                    "options": ["Только первый аргумент", "Все переданные аргументы в массив", "Только именованные параметры", "Ничего, это синтаксическая ошибка"],
                                    "answer": "Все переданные аргументы в массив",
                                },
                                {
                                    "question": "this в стрелочной функции...",
                                    "options": ["всегда undefined", "берётся из внешнего контекста", "всегда window", "задаётся через аргумент"],
                                    "answer": "берётся из внешнего контекста",
                                },
                                {
                                    "question": "Как объявить function expression?",
                                    "options": [
                                        "function sum(a,b) { return a+b; }",
                                        "const sum = function(a,b) { return a+b; }",
                                        "sum => a + b",
                                        "def sum(a, b): return a+b",
                                    ],
                                    "answer": "const sum = function(a,b) { return a+b; }",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Массивы и их методы",
                        "slug": "js-arrays",
                        "order": 3,
                        "youtube_url": "https://www.youtube.com/watch?v=R8rmfD9Y5-c",
                        "duration_minutes": 20,
                        "content": """## Массивы в JavaScript

Массив — упорядоченная коллекция значений любого типа.

```javascript
const fruits = ["яблоко", "банан", "вишня"];
fruits.length;       // 3
fruits[0];            // "яблоко"
```

## Методы, не изменяющие массив

```javascript
const numbers = [1, 2, 3, 4, 5];

numbers.map(n => n * 2);          // [2, 4, 6, 8, 10] — новый массив
numbers.filter(n => n % 2 === 0); // [2, 4] — только чётные
numbers.reduce((sum, n) => sum + n, 0); // 15 — свёртка к одному значению
numbers.find(n => n > 3);         // 4 — первый подходящий элемент
numbers.includes(3);              // true
```

`map`, `filter`, `reduce` — основные методы функционального стиля: они не
меняют исходный массив, а возвращают новый результат.

## Методы, изменяющие массив

```javascript
const arr = [1, 2, 3];
arr.push(4);     // добавляет в конец, arr = [1, 2, 3, 4]
arr.pop();       // удаляет последний элемент
arr.splice(1, 1); // удаляет 1 элемент с индекса 1
```

## Деструктуризация и spread

```javascript
const [first, second] = fruits;
const merged = [...fruits, "груша"]; // новый массив с добавленным элементом
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какой метод массива возвращает новый массив с результатом применения функции к каждому элементу?",
                                "options": ["filter", "map", "reduce", "forEach"],
                                "answer": "map",
                                "explanation": "map преобразует каждый элемент и возвращает новый массив той же длины.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Чем filter отличается от map?",
                                "answer": "map преобразует каждый элемент в новый, возвращая массив той же длины; filter отбирает элементы по условию, возвращая массив, который может быть короче исходного.",
                                "explanation": "Ключевое — map трансформирует, filter отбирает.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Используя reduce, посчитайте сумму массива numbers = [1, 2, 3, 4].",
                                "answer": "const sum = numbers.reduce((acc, n) => acc + n, 0);",
                                "explanation": "Важно использовать reduce с начальным значением 0.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какой метод добавляет элемент в конец массива?",
                                    "options": ["push", "pop", "shift", "unshift"],
                                    "answer": "push",
                                },
                                {
                                    "question": "Что возвращает filter?",
                                    "options": [
                                        "Новый массив с отфильтрованными элементами",
                                        "Одно число",
                                        "Изменённый исходный массив",
                                        "true или false",
                                    ],
                                    "answer": "Новый массив с отфильтрованными элементами",
                                },
                                {
                                    "question": "Какой метод сворачивает массив в одно значение?",
                                    "options": ["map", "filter", "reduce", "find"],
                                    "answer": "reduce",
                                },
                                {
                                    "question": "Что делает spread-оператор [...arr]?",
                                    "options": [
                                        "Удаляет элементы массива",
                                        "Разворачивает элементы массива, например для копирования",
                                        "Сортирует массив",
                                        "Превращает массив в строку",
                                    ],
                                    "answer": "Разворачивает элементы массива, например для копирования",
                                },
                                {
                                    "question": "Какой метод изменяет исходный массив, удаляя элементы?",
                                    "options": ["map", "splice", "filter", "find"],
                                    "answer": "splice",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Работа с DOM",
                        "slug": "js-dom",
                        "order": 4,
                        "youtube_url": "https://www.youtube.com/watch?v=y17RuWkWdn8",
                        "duration_minutes": 22,
                        "content": """## Что такое DOM

DOM (Document Object Model) — представление HTML-документа как дерева
объектов, с которым можно взаимодействовать через JavaScript.

## Поиск элементов

```javascript
document.getElementById("title");
document.querySelector(".card");       // первый подходящий элемент
document.querySelectorAll(".card");    // все подходящие элементы (NodeList)
```

`querySelector`/`querySelectorAll` принимают любой CSS-селектор и более
универсальны, чем `getElementById`.

## Изменение содержимого и стилей

```javascript
const title = document.querySelector("h1");
title.textContent = "Новый заголовок";
title.style.color = "blue";
title.classList.add("active");
```

## Обработка событий

```javascript
const button = document.querySelector("button");
button.addEventListener("click", () => {
  console.log("Кнопка нажата");
});
```

`addEventListener` — основной способ подписаться на событие (`click`,
`input`, `submit` и т.д.), в отличие от устаревшего атрибута `onclick`.

## Создание элементов

```javascript
const li = document.createElement("li");
li.textContent = "Новый пункт";
document.querySelector("ul").appendChild(li);
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какой метод выбирает ВСЕ элементы, подходящие под CSS-селектор?",
                                "options": ["querySelector", "querySelectorAll", "getElementById", "getElementsByName"],
                                "answer": "querySelectorAll",
                                "explanation": "querySelector возвращает только первый найденный элемент, querySelectorAll — все.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Как правильно подписаться на клик по кнопке и почему это лучше атрибута onclick?",
                                "answer": "Через button.addEventListener('click', handler). Это позволяет добавлять несколько обработчиков на один элемент и разделяет HTML и логику JS.",
                                "explanation": "Ключевое — addEventListener, разделение разметки и логики.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Найдите элемент с id 'app' и установите ему textContent равным 'Готово'.",
                                "answer": "document.getElementById('app').textContent = 'Готово';",
                                "explanation": "Важно использовать getElementById и textContent.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Что означает аббревиатура DOM?",
                                    "options": ["Document Object Model", "Data Object Map", "Direct Output Method", "Document Order Markup"],
                                    "answer": "Document Object Model",
                                },
                                {
                                    "question": "Какой метод создаёт новый HTML-элемент?",
                                    "options": ["document.createElement", "document.newElement", "document.makeElement", "document.addElement"],
                                    "answer": "document.createElement",
                                },
                                {
                                    "question": "Как добавить созданный элемент в DOM-дерево?",
                                    "options": ["element.append()", "parent.appendChild(element)", "element.insert()", "document.add(element)"],
                                    "answer": "parent.appendChild(element)",
                                },
                                {
                                    "question": "Каким способом рекомендуют подписываться на события вместо атрибута onclick?",
                                    "options": ["addEventListener", "onEvent", "bindClick", "setHandler"],
                                    "answer": "addEventListener",
                                },
                                {
                                    "question": "Какое свойство меняет текст внутри элемента?",
                                    "options": ["innerHTML только", "textContent", "value всегда", "name"],
                                    "answer": "textContent",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Объекты и деструктуризация",
                        "slug": "js-objects",
                        "order": 5,
                        "youtube_url": "https://www.youtube.com/watch?v=PTV04PCKG8k",
                        "duration_minutes": 18,
                        "content": """## Объекты в JavaScript

Объект — коллекция свойств вида `ключ: значение`. Значением может быть
любой тип: число, строка, массив, функция, другой объект.

```javascript
const user = {
  name: "Алиса",
  age: 25,
  address: { city: "Москва" },
  greet() {
    return `Привет, я ${this.name}`;
  },
};

user.name;          // "Алиса"  — точечная нотация
user["age"];        // 25       — скобочная нотация
user.greet();       // "Привет, я Алиса"
```

## Деструктуризация объектов

Позволяет извлекать значения в переменные одной строкой:

```javascript
const { name, age } = user;
const { name: userName } = user;          // переименование → userName
const { city = "Неизвестно" } = user.address; // значение по умолчанию
```

## Spread и rest

```javascript
const defaults = { theme: "dark", lang: "ru" };
const settings = { ...defaults, lang: "en" };
// { theme: "dark", lang: "en" } — lang перезаписан

const { name, ...rest } = user;
// rest = { age: 25, address: {...} }
```

## Методы Object

```javascript
Object.keys(user);    // ["name", "age", "address", "greet"]
Object.values(user);  // ["Алиса", 25, {...}, ƒ]
Object.entries(user); // [["name", "Алиса"], ["age", 25], ...]

for (const [key, value] of Object.entries(user)) {
  console.log(`${key}: ${value}`);
}
```

`Object.entries` удобен, чтобы пройтись по объекту как по массиву.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Что происходит, если одно и то же свойство указано в объекте дважды при spread?",
                                "options": [
                                    "Ошибка синтаксиса",
                                    "Последнее значение перезаписывает первое",
                                    "Первое значение перезаписывает последнее",
                                    "Создаётся массив из двух значений",
                                ],
                                "answer": "Последнее значение перезаписывает первое",
                                "explanation": "При spread { ...defaults, lang: 'en' } lang из defaults заменяется на 'en'.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Что возвращает Object.entries(obj) и как его использовать?",
                                "answer": "Object.entries возвращает массив пар [ключ, значение]. Используют в for...of для итерации по объекту или в map/filter для трансформации: Object.entries(obj).map(([k, v]) => ...).",
                                "explanation": "Ключевое — массив [ключ, значение], удобен для итерации.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Деструктурируйте объект { name: 'Bob', score: 95 } в переменные name и score.",
                                "answer": "const { name, score } = { name: 'Bob', score: 95 };",
                                "explanation": "Имена переменных должны совпадать с ключами объекта.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Как получить доступ к свойству ключ которого хранится в переменной?",
                                    "options": ["obj.variable", "obj[variable]", "obj->variable", "obj::variable"],
                                    "answer": "obj[variable]",
                                },
                                {
                                    "question": "const { a: x } = obj; что это делает?",
                                    "options": [
                                        "Создаёт obj.a и obj.x",
                                        "Деструктурирует obj.a в переменную x",
                                        "Деструктурирует obj.x в переменную a",
                                        "Синтаксическая ошибка",
                                    ],
                                    "answer": "Деструктурирует obj.a в переменную x",
                                },
                                {
                                    "question": "Что возвращает Object.keys(obj)?",
                                    "options": ["Массив значений", "Массив ключей", "Массив пар [ключ, значение]", "Количество ключей"],
                                    "answer": "Массив ключей",
                                },
                                {
                                    "question": "const { b = 10 } = {}; что будет в b?",
                                    "options": ["undefined", "null", "10", "Ошибка"],
                                    "answer": "10",
                                },
                                {
                                    "question": "Метод объекта — это...",
                                    "options": [
                                        "Только Math.round и подобные",
                                        "Функция, сохранённая как свойство объекта",
                                        "Отдельный класс",
                                        "Прототип объекта",
                                    ],
                                    "answer": "Функция, сохранённая как свойство объекта",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Асинхронность: Promise и async/await",
                        "slug": "js-async",
                        "order": 6,
                        "youtube_url": "https://www.youtube.com/watch?v=Dn8hZ1nlWJQ",
                        "duration_minutes": 25,
                        "content": """## Зачем нужна асинхронность

JavaScript однопоточный: сетевые запросы, таймеры и файловые операции
выполняются через Event Loop, не блокируя остальной код. Без правильного
управления порядок выполнения непредсказуем.

## Callback (устаревший подход)

```javascript
setTimeout(() => {
  console.log("через 1 секунду");
}, 1000);
```

Колбэки — простейший способ, но вложенные колбэки превращаются в
"callback hell" — нечитаемую пирамиду вложенностей.

## Promise

Promise — объект с тремя состояниями: pending → fulfilled или rejected.

```javascript
const promise = new Promise((resolve, reject) => {
  setTimeout(() => resolve("данные"), 1000);
});

promise
  .then(data => console.log(data))
  .catch(err => console.error(err))
  .finally(() => console.log("всегда"));
```

## async/await

Синтаксический сахар над Promise — делает асинхронный код похожим на
синхронный:

```javascript
async function loadUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error("Ошибка сервера");
    const user = await response.json();
    return user;
  } catch (error) {
    console.error("Ошибка:", error.message);
  }
}
```

- `async` перед функцией — она всегда возвращает Promise
- `await` останавливает выполнение функции до разрешения Promise

## Параллельные запросы

```javascript
const [users, posts] = await Promise.all([
  fetch("/api/users").then(r => r.json()),
  fetch("/api/posts").then(r => r.json()),
]);
```

`Promise.all` запускает все Promise параллельно и ждёт их завершения.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Что делает await внутри async-функции?",
                                "options": [
                                    "Создаёт новый поток выполнения",
                                    "Приостанавливает выполнение функции до разрешения Promise",
                                    "Вызывает функцию синхронно",
                                    "Всегда возвращает undefined",
                                ],
                                "answer": "Приостанавливает выполнение функции до разрешения Promise",
                                "explanation": "await ждёт Promise, не блокируя остальной код вне функции.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "В чём разница между Promise.all и последовательными await?",
                                "answer": "Promise.all запускает все Promise одновременно и ждёт всех — быстрее при независимых запросах. Последовательные await ждут каждый по очереди — нужно, если следующий запрос зависит от результата предыдущего.",
                                "explanation": "Ключевое — параллельность vs последовательность, зависимость между запросами.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите async-функцию getData, которая делает GET-запрос к '/api/data' и возвращает JSON.",
                                "answer": "async function getData() {\n  const response = await fetch('/api/data');\n  return response.json();\n}",
                                "explanation": "Важны async, await fetch, и вызов .json().",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Функция с ключевым словом async...",
                                    "options": [
                                        "Запускается в отдельном потоке",
                                        "Всегда возвращает Promise",
                                        "Не может использовать return",
                                        "Выполняется быстрее обычной",
                                    ],
                                    "answer": "Всегда возвращает Promise",
                                },
                                {
                                    "question": "Что перехватывает .catch() в цепочке Promise?",
                                    "options": ["Только ошибки сети", "Любой reject или брошенный Error", "Только TypeError", "HTTP-статусы 4xx"],
                                    "answer": "Любой reject или брошенный Error",
                                },
                                {
                                    "question": "Promise.all([p1, p2]) завершается когда...",
                                    "options": [
                                        "Выполнится первый из p1 или p2",
                                        "Выполнятся оба p1 и p2",
                                        "Только p1 завершится",
                                        "Через фиксированный таймаут",
                                    ],
                                    "answer": "Выполнятся оба p1 и p2",
                                },
                                {
                                    "question": "await можно использовать...",
                                    "options": [
                                        "В любой функции",
                                        "Только внутри async-функции",
                                        "Только в стрелочных функциях",
                                        "Только на верхнем уровне файла",
                                    ],
                                    "answer": "Только внутри async-функции",
                                },
                                {
                                    "question": "Что вернёт fetch('/api/data')?",
                                    "options": ["JSON-объект сразу", "Promise<Response>", "строку", "undefined"],
                                    "answer": "Promise<Response>",
                                },
                            ],
                        },
                    },
                ],
            },
        ],
    },
    {
        "title": "Backend разработчик",
        "slug": "backend",
        "description": "Серверная логика, API и работа с базами данных на Python.",
        "icon": "⚙️",
        "order": 2,
        "stacks": [
            {
                "title": "Python основы",
                "slug": "python-basics",
                "description": "Переменные, типы данных и функции в Python.",
                "order": 1,
                "lessons": [
                    {
                        "title": "Переменные и типы данных в Python",
                        "slug": "python-variables",
                        "order": 1,
                        "youtube_url": "https://www.youtube.com/watch?v=qscPCmMzByM",
                        "duration_minutes": 15,
                        "content": """## Переменные в Python

Python — динамически типизированный язык: тип переменной определяется
значением, а не объявлением. Объявлять тип явно не нужно.

```python
age = 25          # int
price = 9.99      # float
name = "Alice"    # str
is_active = True  # bool
```

## Основные типы данных

- **int** — целые числа
- **float** — числа с плавающей точкой
- **str** — строки (текст)
- **bool** — логический тип (True/False)
- **list** — изменяемый упорядоченный список значений: `[1, 2, 3]`
- **tuple** — неизменяемый упорядоченный набор значений: `(1, 2, 3)`
- **dict** — словарь "ключ-значение": `{"name": "Alice", "age": 25}`
- **set** — неупорядоченная коллекция уникальных значений: `{1, 2, 3}`

## Проверка типа

```python
type(age)        # <class 'int'>
isinstance(age, int)  # True
```

## f-строки

Самый удобный способ форматировать строки — f-строки:

```python
name = "Alice"
age = 25
print(f"{name} — {age} лет")
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какой тип данных является неизменяемым (immutable)?",
                                "options": ["list", "dict", "tuple", "set"],
                                "answer": "tuple",
                                "explanation": "tuple нельзя изменить после создания, в отличие от list, dict, set.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Что значит, что Python — динамически типизированный язык?",
                                "answer": "Тип переменной определяется значением во время выполнения, а не объявляется заранее, и может меняться при переназначении.",
                                "explanation": "Главное — тип привязан к значению, а не к имени переменной.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Создайте f-строку, которая выводит 'Привет, <имя>!' для переменной name.",
                                "answer": 'print(f"Привет, {name}!")',
                                "explanation": "Важно использовать f-строку с подстановкой переменной.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какой тип данных хранит пары ключ-значение?",
                                    "options": ["list", "tuple", "dict", "set"],
                                    "answer": "dict",
                                },
                                {
                                    "question": "Нужно ли явно указывать тип переменной в Python?",
                                    "options": ["Да, всегда", "Нет, тип определяется значением", "Только для чисел", "Только для строк"],
                                    "answer": "Нет, тип определяется значением",
                                },
                                {
                                    "question": "Какой тип данных содержит только уникальные значения без порядка?",
                                    "options": ["list", "set", "tuple", "dict"],
                                    "answer": "set",
                                },
                                {
                                    "question": "Как проверить тип переменной x?",
                                    "options": ["typeof(x)", "type(x)", "x.type()", "kind(x)"],
                                    "answer": "type(x)",
                                },
                                {
                                    "question": "Какой синтаксис f-строки правильный?",
                                    "options": ['f"{name}"', '"{name}"f', "f(name)", "%name%"],
                                    "answer": 'f"{name}"',
                                },
                            ],
                        },
                    },
                    {
                        "title": "Функции в Python",
                        "slug": "python-functions",
                        "order": 2,
                        "youtube_url": "https://www.youtube.com/watch?v=Vh29sJFAYCg",
                        "duration_minutes": 18,
                        "content": """## Объявление функций

```python
def greet(name):
    return f"Привет, {name}!"

print(greet("Алиса"))
```

## Параметры по умолчанию

```python
def greet(name="Гость"):
    return f"Привет, {name}!"
```

## *args и **kwargs

```python
def sum_all(*numbers):
    return sum(numbers)

def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
```

`*args` собирает позиционные аргументы в tuple, `**kwargs` — именованные
аргументы в dict.

## Аннотации типов

Python поддерживает необязательные аннотации типов — они не проверяются во
время выполнения, но помогают читать код и работают с инструментами вроде
mypy и FastAPI:

```python
def sum(a: int, b: int) -> int:
    return a + b
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Во что собирает аргументы *args?",
                                "options": ["dict", "tuple", "list", "set"],
                                "answer": "tuple",
                                "explanation": "*args собирает позиционные аргументы в tuple.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Зачем нужны аннотации типов в Python, если они не проверяются интерпретатором?",
                                "answer": "Они улучшают читаемость кода и позволяют инструментам (mypy, IDE, FastAPI) проверять и использовать типы статически.",
                                "explanation": "Ключевая мысль — типы помогают инструментам и читаемости, а не runtime-проверке.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите функцию multiply(a, b), которая возвращает произведение и имеет аннотации типов int.",
                                "answer": "def multiply(a: int, b: int) -> int:\n    return a * b",
                                "explanation": "Важны аннотации параметров и возвращаемого значения.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Во что собирает аргументы **kwargs?",
                                    "options": ["list", "tuple", "dict", "set"],
                                    "answer": "dict",
                                },
                                {
                                    "question": "Как задать параметр со значением по умолчанию?",
                                    "options": ["def f(a=1):", "def f(a:=1):", "def f(a==1):", "def f(default a=1):"],
                                    "answer": "def f(a=1):",
                                },
                                {
                                    "question": "Проверяются ли аннотации типов интерпретатором Python во время выполнения?",
                                    "options": ["Да, всегда", "Нет, по умолчанию не проверяются", "Только в функциях", "Только для int"],
                                    "answer": "Нет, по умолчанию не проверяются",
                                },
                                {
                                    "question": "Как объявить функцию без аргументов, возвращающую None?",
                                    "options": ["def f(): pass", "function f() {}", "def f() => None", "f = def(): None"],
                                    "answer": "def f(): pass",
                                },
                                {
                                    "question": "Что вернёт функция, если в ней нет return?",
                                    "options": ["0", "''", "None", "Ошибку"],
                                    "answer": "None",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Списки, циклы и условия",
                        "slug": "python-lists-loops",
                        "order": 3,
                        "youtube_url": "https://www.youtube.com/watch?v=YFbF1YBhHc4",
                        "duration_minutes": 20,
                        "content": """## Списки (list)

```python
fruits = ["яблоко", "банан", "вишня"]
fruits.append("груша")    # добавить элемент
fruits[0]                  # "яблоко"
fruits[-1]                  # последний элемент
len(fruits)                 # 4
```

## Цикл for

```python
for fruit in fruits:
    print(fruit)

for i in range(5):       # 0, 1, 2, 3, 4
    print(i)
```

## List comprehension

Питоничный способ построить список из другого списка:

```python
squares = [n ** 2 for n in range(5)]          # [0, 1, 4, 9, 16]
evens = [n for n in range(10) if n % 2 == 0]  # [0, 2, 4, 6, 8]
```

## Условия

```python
age = 18
if age >= 18:
    print("Взрослый")
elif age >= 13:
    print("Подросток")
else:
    print("Ребёнок")
```

## while

```python
count = 0
while count < 3:
    print(count)
    count += 1
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Что вернёт range(5) при использовании в цикле for?",
                                "options": ["Числа от 1 до 5", "Числа от 0 до 4", "Числа от 0 до 5", "Список [5]"],
                                "answer": "Числа от 0 до 4",
                                "explanation": "range(5) генерирует 5 чисел начиная с 0: 0,1,2,3,4.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Что такое list comprehension и зачем его используют?",
                                "answer": "Это компактный синтаксис для построения списка из итерируемого объекта в одну строку, например [n**2 for n in range(5)]. Используется для краткости и читаемости вместо обычного цикла с append.",
                                "explanation": "Главное — краткая запись построения списка вместо цикла с append.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите list comprehension, создающий список квадратов чисел от 1 до 5.",
                                "answer": "squares = [n ** 2 for n in range(1, 6)]",
                                "explanation": "Важно использовать range(1, 6), чтобы включить число 5.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Как получить последний элемент списка fruits?",
                                    "options": ["fruits[-1]", "fruits[last]", "fruits.end()", "fruits[0]"],
                                    "answer": "fruits[-1]",
                                },
                                {
                                    "question": "Какой оператор добавляет элемент в конец списка?",
                                    "options": [".append()", ".add()", ".push()", ".insert()"],
                                    "answer": ".append()",
                                },
                                {
                                    "question": "Что делает [n for n in range(10) if n % 2 == 0]?",
                                    "options": [
                                        "Возвращает все числа от 0 до 9",
                                        "Возвращает только чётные числа от 0 до 9",
                                        "Возвращает только нечётные числа",
                                        "Вызывает ошибку",
                                    ],
                                    "answer": "Возвращает только чётные числа от 0 до 9",
                                },
                                {
                                    "question": "Когда выполняется блок else в конструкции if/elif/else?",
                                    "options": [
                                        "Всегда",
                                        "Когда ни одно условие if/elif не выполнилось",
                                        "Только если if выполнился",
                                        "Никогда не выполняется",
                                    ],
                                    "answer": "Когда ни одно условие if/elif не выполнилось",
                                },
                                {
                                    "question": "Цикл while выполняется, пока...",
                                    "options": [
                                        "Условие истинно (True)",
                                        "Условие ложно (False)",
                                        "Ровно 10 раз",
                                        "Список не пуст всегда",
                                    ],
                                    "answer": "Условие истинно (True)",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Классы и ООП в Python",
                        "slug": "python-classes",
                        "order": 4,
                        "youtube_url": "https://www.youtube.com/watch?v=ZDa-Z5JzLYM",
                        "duration_minutes": 22,
                        "content": """## Объявление класса

```python
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, я {self.name}"

user = User("Алиса", 25)
print(user.greet())  # Привет, я Алиса
```

`__init__` — конструктор, вызывается автоматически при создании объекта.
`self` — ссылка на сам объект, обязательный первый параметр методов.

## Наследование

```python
class Admin(User):
    def __init__(self, name: str, age: int, level: int):
        super().__init__(name, age)
        self.level = level

    def greet(self) -> str:
        return f"{super().greet()}, я админ уровня {self.level}"
```

`super()` обращается к методам родительского класса. `Admin` переопределяет
`greet`, но всё равно может вызвать родительскую реализацию.

## Атрибуты класса vs атрибуты экземпляра

```python
class Counter:
    total = 0  # атрибут класса — общий для всех экземпляров

    def __init__(self):
        Counter.total += 1
        self.id = Counter.total  # атрибут экземпляра — свой у каждого объекта
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Какой метод вызывается автоматически при создании объекта класса?",
                                "options": ["__main__", "__init__", "__new__", "__call__"],
                                "answer": "__init__",
                                "explanation": "__init__ — конструктор, инициализирующий атрибуты нового объекта.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Зачем нужен super() в дочернем классе?",
                                "answer": "Чтобы обратиться к методам родительского класса, например вызвать родительский __init__ или переопределённый метод, не дублируя его код.",
                                "explanation": "Ключевое — доступ к реализации родителя без дублирования кода.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите класс Animal с конструктором, принимающим name, и методом speak(), возвращающим f'{name} издаёт звук'.",
                                "answer": "class Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return f'{self.name} издаёт звук'",
                                "explanation": "Важны __init__ с self.name и метод speak с self.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Что такое self в методах класса?",
                                    "options": [
                                        "Ссылка на родительский класс",
                                        "Ссылка на сам объект (экземпляр)",
                                        "Имя класса",
                                        "Необязательный параметр",
                                    ],
                                    "answer": "Ссылка на сам объект (экземпляр)",
                                },
                                {
                                    "question": "Как объявить, что класс Admin наследуется от User?",
                                    "options": ["class Admin(User):", "class Admin extends User:", "class Admin -> User:", "class Admin use User:"],
                                    "answer": "class Admin(User):",
                                },
                                {
                                    "question": "Атрибут класса (объявленный без self) общий для...",
                                    "options": [
                                        "Только одного экземпляра",
                                        "Всех экземпляров класса",
                                        "Только дочерних классов",
                                        "Ничего, это ошибка",
                                    ],
                                    "answer": "Всех экземпляров класса",
                                },
                                {
                                    "question": "Что делает super().__init__(name, age) в дочернем классе?",
                                    "options": [
                                        "Создаёт новый объект родителя",
                                        "Вызывает конструктор родительского класса для текущего объекта",
                                        "Удаляет родительский класс",
                                        "Ничего не делает",
                                    ],
                                    "answer": "Вызывает конструктор родительского класса для текущего объекта",
                                },
                                {
                                    "question": "Как создать экземпляр класса User с аргументами 'Алиса', 25?",
                                    "options": ["User('Алиса', 25)", "new User('Алиса', 25)", "User.create('Алиса', 25)", "User->new('Алиса', 25)"],
                                    "answer": "User('Алиса', 25)",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Словари и работа с данными",
                        "slug": "python-dicts",
                        "order": 5,
                        "youtube_url": "https://www.youtube.com/watch?v=daefaLgNkw0",
                        "duration_minutes": 16,
                        "content": """## Словари (dict)

Словарь — коллекция пар ключ-значение с быстрым поиском O(1) по ключу.

```python
user = {
    "name": "Алиса",
    "age": 25,
    "active": True,
}

user["name"]               # "Алиса"
user.get("email", "—")     # "—" (не вызывает KeyError)
user["email"] = "a@b.com"  # добавление нового ключа
del user["active"]          # удаление ключа
"name" in user              # True — проверка ключа
```

## Методы словаря

```python
user.keys()    # dict_keys(["name", "age", "email"])
user.values()  # dict_values(["Алиса", 25, "a@b.com"])
user.items()   # dict_items([("name", "Алиса"), ...])

for key, value in user.items():
    print(f"{key}: {value}")
```

## Dict comprehension

```python
squares = {n: n**2 for n in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

active_users = {k: v for k, v in users.items() if v["active"]}
```

## Counter из collections

```python
from collections import Counter

words = ["python", "java", "python", "go", "python"]
counter = Counter(words)
counter["python"]        # 3
counter.most_common(2)   # [("python", 3), ("java", 1)]
```

`Counter` — словарь для подсчёта элементов. Незаменим при анализе данных
и частотных задачах.

## defaultdict

```python
from collections import defaultdict

groups = defaultdict(list)
for name, group in students:
    groups[group].append(name)  # не нужно проверять groups[group] exists
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Чем user.get('key', 'default') лучше user['key']?",
                                "options": [
                                    "Он быстрее",
                                    "Не вызывает KeyError, возвращает значение по умолчанию",
                                    "Создаёт ключ автоматически",
                                    "Работает только со строками",
                                ],
                                "answer": "Не вызывает KeyError, возвращает значение по умолчанию",
                                "explanation": "get() безопаснее при неизвестных ключах — не бросает исключение.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Для чего используют Counter из модуля collections?",
                                "answer": "Counter — это словарь-подкласс для подсчёта элементов в итерируемом объекте. Используют для частотного анализа: подсчёт слов, символов, элементов. Метод most_common(n) возвращает n самых частых.",
                                "explanation": "Ключевое — частотный подсчёт, most_common().",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Создайте dict comprehension: словарь, где ключ — слово, значение — его длина, для списка ['hello', 'world', 'python'].",
                                "answer": "words = ['hello', 'world', 'python']\nlengths = {word: len(word) for word in words}",
                                "explanation": "Формат: {ключ: значение for элемент in итерируемый}.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Что произойдёт при обращении к отсутствующему ключу через d['key']?",
                                    "options": ["Вернёт None", "Вернёт 0", "Поднимет KeyError", "Создаст ключ автоматически"],
                                    "answer": "Поднимет KeyError",
                                },
                                {
                                    "question": "Что возвращает d.items()?",
                                    "options": ["Список ключей", "Список значений", "Список пар (ключ, значение)", "Словарь наоборот"],
                                    "answer": "Список пар (ключ, значение)",
                                },
                                {
                                    "question": "Как удалить ключ 'x' из словаря d?",
                                    "options": ["d.remove('x')", "del d['x']", "d.delete('x')", "d.pop_key('x')"],
                                    "answer": "del d['x']",
                                },
                                {
                                    "question": "Counter(['a','b','a','c','a']).most_common(1) вернёт...",
                                    "options": ["['a']", "[('a', 3)]", "3", "{'a': 3}"],
                                    "answer": "[('a', 3)]",
                                },
                                {
                                    "question": "Dict comprehension {k: v for k, v in d.items() if v > 0} делает...",
                                    "options": [
                                        "Копирует словарь",
                                        "Создаёт новый словарь только с положительными значениями",
                                        "Сортирует по значению",
                                        "Изменяет исходный словарь",
                                    ],
                                    "answer": "Создаёт новый словарь только с положительными значениями",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Исключения и обработка ошибок",
                        "slug": "python-exceptions",
                        "order": 6,
                        "youtube_url": "https://www.youtube.com/watch?v=NIWwJbo-9_8",
                        "duration_minutes": 18,
                        "content": """## Что такое исключения

Когда Python встречает ошибку при выполнении, он возбуждает исключение
(exception). Необработанное исключение останавливает программу.

```python
result = 10 / 0   # ZeroDivisionError
name = int("abc") # ValueError
lst[10]           # IndexError
```

## try / except / else / finally

```python
try:
    result = 10 / int(input("Делитель: "))
except ValueError:
    print("Введите число")
except ZeroDivisionError:
    print("Делить на ноль нельзя")
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
else:
    print(f"Результат: {result}")   # если ошибки не было
finally:
    print("Выполняется всегда")     # всегда, с ошибкой или без
```

`Exception` — базовый класс большинства исключений. Перехватывайте более
конкретные исключения раньше, чтобы не скрывать ошибки.

## raise: возбудить исключение вручную

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Делитель не может быть нулём")
    return a / b
```

## Собственные исключения

```python
class InsufficientFundsError(Exception):
    def __init__(self, amount: float):
        super().__init__(f"Недостаточно средств: {amount} руб.")
        self.amount = amount

try:
    raise InsufficientFundsError(500)
except InsufficientFundsError as e:
    print(e.amount)  # 500
```

Собственные исключения улучшают читаемость кода и позволяют программно
реагировать на конкретные ошибки (например, в API).""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Блок finally выполняется...",
                                "options": [
                                    "Только если исключения не было",
                                    "Только если исключение было",
                                    "Всегда, с исключением или без",
                                    "Только после блока else",
                                ],
                                "answer": "Всегда, с исключением или без",
                                "explanation": "finally нужен для обязательной очистки ресурсов: закрытие файлов, подключений и т.д.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Зачем создавать собственные классы исключений вместо использования Exception?",
                                "answer": "Собственные исключения позволяют различать типы ошибок, нести дополнительные данные (например, сумму при ошибке баланса) и перехватывать их точечно — не нужно разбирать текст сообщения.",
                                "explanation": "Ключевое — типизация ошибок, структурированные данные об ошибке.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите функцию safe_divide(a, b), которая при b=0 возбуждает ValueError с сообщением 'Деление на ноль'.",
                                "answer": "def safe_divide(a, b):\n    if b == 0:\n        raise ValueError('Деление на ноль')\n    return a / b",
                                "explanation": "Важны проверка условия и raise ValueError с сообщением.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какое исключение возникнет при int('abc')?",
                                    "options": ["TypeError", "ValueError", "KeyError", "RuntimeError"],
                                    "answer": "ValueError",
                                },
                                {
                                    "question": "В каком порядке нужно перечислять except-блоки?",
                                    "options": [
                                        "От общего к конкретному",
                                        "От конкретного к общему",
                                        "Порядок не важен",
                                        "Все в одном блоке через запятую",
                                    ],
                                    "answer": "От конкретного к общему",
                                },
                                {
                                    "question": "Что делает ключевое слово raise?",
                                    "options": [
                                        "Перехватывает исключение",
                                        "Возбуждает (бросает) исключение",
                                        "Подавляет исключение",
                                        "Логирует исключение",
                                    ],
                                    "answer": "Возбуждает (бросает) исключение",
                                },
                                {
                                    "question": "Блок else в try/except выполняется когда...",
                                    "options": [
                                        "Всегда",
                                        "Только если исключения не было",
                                        "Только если исключение было",
                                        "Только после finally",
                                    ],
                                    "answer": "Только если исключения не было",
                                },
                                {
                                    "question": "Как создать собственный класс исключения?",
                                    "options": [
                                        "class MyError: pass",
                                        "class MyError(Exception): pass",
                                        "exception MyError: pass",
                                        "class MyError extends Exception: pass",
                                    ],
                                    "answer": "class MyError(Exception): pass",
                                },
                            ],
                        },
                    },
                ],
            },
            {
                "title": "FastAPI",
                "slug": "fastapi",
                "description": "Создание REST API на Python с FastAPI.",
                "order": 2,
                "lessons": [
                    {
                        "title": "Введение в FastAPI",
                        "slug": "fastapi-intro",
                        "order": 1,
                        "youtube_url": "https://www.youtube.com/watch?v=0sOvCWFmrtA",
                        "duration_minutes": 20,
                        "content": """## Что такое FastAPI

FastAPI — современный веб-фреймворк для Python для создания API. Он
построен на Starlette (ASGI) и Pydantic (валидация данных) и автоматически
генерирует интерактивную документацию (Swagger UI).

## Минимальное приложение

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Привет, мир!"}
```

Запуск: `uvicorn main:app --reload`

## Path Operations

Каждая функция, отмеченная декоратором `@app.get`, `@app.post` и т.д.,
называется path operation — она привязана к HTTP-методу и пути.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

## Автоматическая документация

FastAPI сам генерирует документацию по адресам `/docs` (Swagger UI) и
`/redoc`, используя типы и Pydantic-схемы, описанные в коде.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "На какой библиотеке валидации данных построен FastAPI?",
                                "options": ["marshmallow", "Pydantic", "attrs", "Cerberus"],
                                "answer": "Pydantic",
                                "explanation": "FastAPI использует Pydantic для валидации и сериализации данных.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Что такое path operation в FastAPI?",
                                "answer": "Функция, отмеченная декоратором вроде @app.get или @app.post, которая обрабатывает запросы к определённому пути и HTTP-методу.",
                                "explanation": "Ключевое — связь декоратора с HTTP-методом и путём.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите path operation GET /ping, возвращающую {\"pong\": True}.",
                                "answer": '@app.get("/ping")\ndef ping():\n    return {"pong": True}',
                                "explanation": "Важен правильный декоратор и возвращаемое значение.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Какой командой запускают FastAPI-приложение в режиме разработки?",
                                    "options": ["python main.py", "uvicorn main:app --reload", "flask run", "fastapi start"],
                                    "answer": "uvicorn main:app --reload",
                                },
                                {
                                    "question": "По какому адресу FastAPI генерирует Swagger-документацию по умолчанию?",
                                    "options": ["/swagger", "/docs", "/api-docs", "/openapi"],
                                    "answer": "/docs",
                                },
                                {
                                    "question": "На каком ASGI-фреймворке построен FastAPI?",
                                    "options": ["Starlette", "Flask", "Django", "Tornado"],
                                    "answer": "Starlette",
                                },
                                {
                                    "question": "Каким декоратором описывают GET-эндпоинт?",
                                    "options": ["@app.route", "@app.get", "@app.endpoint", "@get.app"],
                                    "answer": "@app.get",
                                },
                                {
                                    "question": "Что генерирует FastAPI автоматически на основе кода?",
                                    "options": ["Тесты", "Документацию API", "Базу данных", "Frontend"],
                                    "answer": "Документацию API",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Path и Query параметры",
                        "slug": "fastapi-params",
                        "order": 2,
                        "youtube_url": "https://www.youtube.com/watch?v=GxpG-4WBDMQ",
                        "duration_minutes": 18,
                        "content": """## Path параметры

Path-параметры объявляются прямо в пути с помощью `{}` и обязательны.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

FastAPI автоматически проверит, что `item_id` — целое число, и вернёт ошибку
422, если это не так.

## Query параметры

Любой параметр функции, который не объявлен в пути, FastAPI считает query
параметром. Если у него есть значение по умолчанию — он необязателен.

```python
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

Запрос `GET /items/?skip=5&limit=20` вернёт `{"skip": 5, "limit": 20}`.

## Комбинация

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, detail: bool = False):
    return {"item_id": item_id, "detail": detail}
```

`GET /items/1?detail=true` → `{"item_id": 1, "detail": true}`.

Типизация параметров даёт автоматическую валидацию и преобразование типов —
если передать нечисловой `item_id`, FastAPI сам вернёт понятную ошибку.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Параметр функции, который не указан в пути, FastAPI считает...",
                                "options": ["Path параметром", "Query параметром", "Заголовком", "Телом запроса"],
                                "answer": "Query параметром",
                                "explanation": "Всё, что не часть пути — query параметр (если не указано иное, например через Body).",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Что произойдёт, если передать в path-параметр item_id: int строку 'abc'?",
                                "answer": "FastAPI вернёт ошибку валидации 422 Unprocessable Entity, так как значение нельзя преобразовать в int.",
                                "explanation": "Ключевое — автоматическая валидация и код 422.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите эндпоинт GET /users/{user_id} с query-параметром active: bool = True.",
                                "answer": '@app.get("/users/{user_id}")\ndef read_user(user_id: int, active: bool = True):\n    return {"user_id": user_id, "active": active}',
                                "explanation": "Важны типы user_id (path) и active (query, со значением по умолчанию).",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Path-параметры в FastAPI...",
                                    "options": ["Всегда необязательны", "Всегда обязательны", "Можно сделать опциональными как query", "Не поддерживают типизацию"],
                                    "answer": "Всегда обязательны",
                                },
                                {
                                    "question": "Что делает query-параметр необязательным?",
                                    "options": ["Указание типа", "Значение по умолчанию", "Расположение в URL", "Декоратор @optional"],
                                    "answer": "Значение по умолчанию",
                                },
                                {
                                    "question": "Какой код ошибки вернёт FastAPI при неверном типе параметра?",
                                    "options": ["404", "500", "422", "400"],
                                    "answer": "422",
                                },
                                {
                                    "question": "В пути GET /items/{item_id}, item_id — это:",
                                    "options": ["Query параметр", "Path параметр", "Заголовок", "Cookie"],
                                    "answer": "Path параметр",
                                },
                                {
                                    "question": "Как вызвать /items/?skip=5&limit=20 с точки зрения клиента?",
                                    "options": [
                                        "Передать skip и limit в теле запроса",
                                        "Передать skip и limit как query-параметры в URL",
                                        "Это невозможно без path-параметров",
                                        "Передать через заголовки",
                                    ],
                                    "answer": "Передать skip и limit как query-параметры в URL",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Pydantic-модели и тело запроса",
                        "slug": "fastapi-pydantic",
                        "order": 3,
                        "youtube_url": "https://www.youtube.com/watch?v=pkyrQ-HQJHI",
                        "duration_minutes": 22,
                        "content": """## Зачем нужны Pydantic-модели

Pydantic-модели описывают форму данных (JSON), которые приходят в теле
запроса (`POST`, `PUT`, `PATCH`), и автоматически валидируют их.

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # значение по умолчанию — поле необязательно

@app.post("/items/")
def create_item(item: Item):
    return item
```

Если клиент отправит JSON без поля `price` или с `price` нечислового типа,
FastAPI вернёт `422 Unprocessable Entity` с описанием ошибки — без единой
строчки ручной валидации в коде.

## Вложенные модели

```python
class Address(BaseModel):
    city: str
    street: str

class User(BaseModel):
    name: str
    address: Address
```

FastAPI рекурсивно валидирует вложенные объекты и сам генерирует под них
JSON Schema для документации в `/docs`.

## response_model

```python
@app.post("/items/", response_model=Item)
def create_item(item: Item) -> Item:
    return item
```

`response_model` гарантирует, что в ответе будут только описанные поля —
даже если функция вернёт объект с дополнительными атрибутами, лишние поля
отфильтруются.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Что произойдёт, если в теле POST-запроса не передать обязательное поле Pydantic-модели?",
                                "options": [
                                    "Поле станет None автоматически",
                                    "FastAPI вернёт ошибку валидации 422",
                                    "Сервер упадёт с 500",
                                    "Запрос выполнится без этого поля",
                                ],
                                "answer": "FastAPI вернёт ошибку валидации 422",
                                "explanation": "Без значения по умолчанию поле обязательно — его отсутствие даёт 422.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Зачем использовать response_model в path operation?",
                                "answer": "Чтобы гарантировать, что в ответе клиенту будут только описанные в модели поля, отфильтровав лишние, и чтобы FastAPI сгенерировал точную документацию ответа.",
                                "explanation": "Ключевое — фильтрация полей ответа и точная документация.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Создайте Pydantic-модель Product с полями name: str и price: float, и эндпоинт POST /products принимающий её.",
                                "answer": "class Product(BaseModel):\n    name: str\n    price: float\n\n@app.post('/products')\ndef create_product(product: Product):\n    return product",
                                "explanation": "Важны корректные типы полей и параметр функции с аннотацией Product.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "От какого класса наследуются Pydantic-модели в FastAPI?",
                                    "options": ["BaseModel", "Model", "Schema", "DataModel"],
                                    "answer": "BaseModel",
                                },
                                {
                                    "question": "Поле с значением по умолчанию в Pydantic-модели становится:",
                                    "options": ["Обязательным", "Необязательным", "Игнорируется", "Только для чтения"],
                                    "answer": "Необязательным",
                                },
                                {
                                    "question": "Может ли Pydantic-модель содержать другую модель как поле?",
                                    "options": ["Нет, только примитивы", "Да, вложенные модели валидируются рекурсивно", "Только списки примитивов", "Только через Optional"],
                                    "answer": "Да, вложенные модели валидируются рекурсивно",
                                },
                                {
                                    "question": "Зачем нужен response_model?",
                                    "options": [
                                        "Чтобы ускорить запрос",
                                        "Чтобы отфильтровать и задокументировать поля ответа",
                                        "Чтобы заменить Pydantic на dict",
                                        "Он обязателен для всех эндпоинтов",
                                    ],
                                    "answer": "Чтобы отфильтровать и задокументировать поля ответа",
                                },
                                {
                                    "question": "В какой части запроса передаются данные, валидируемые Pydantic-моделью при POST?",
                                    "options": ["В query-параметрах", "В пути URL", "В теле запроса (body)", "В заголовках"],
                                    "answer": "В теле запроса (body)",
                                },
                            ],
                        },
                    },
                    {
                        "title": "Dependency Injection в FastAPI",
                        "slug": "fastapi-dependencies",
                        "order": 4,
                        "youtube_url": "https://www.youtube.com/watch?v=C0bOJPJ6BRE",
                        "duration_minutes": 24,
                        "content": """## Что такое Depends

`Depends` — механизм внедрения зависимостей в FastAPI: функция-зависимость
выполняется перед основным обработчиком, и её результат передаётся как
аргумент.

```python
from fastapi import Depends

def get_query_token(token: str):
    return token

@app.get("/items/")
def read_items(token: str = Depends(get_query_token)):
    return {"token": token}
```

## Типичный пример: подключение к базе данных

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

Зависимость с `yield` гарантирует, что код после `yield` (закрытие сессии)
выполнится всегда, даже если в обработчике произошла ошибка — похоже на
`try/finally`.

## Зависимости для авторизации

```python
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # декодирование токена, поиск пользователя
    ...

@app.get("/profile")
def profile(user: User = Depends(get_current_user)):
    return user
```

Так любой защищённый эндпоинт получает текущего пользователя одной строкой,
а логика проверки токена не дублируется в каждом обработчике.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Когда выполняется функция-зависимость, переданная через Depends?",
                                "options": [
                                    "После выполнения основного обработчика",
                                    "Перед выполнением основного обработчика",
                                    "Только при ошибке",
                                    "Никогда автоматически, нужно вызывать вручную",
                                ],
                                "answer": "Перед выполнением основного обработчика",
                                "explanation": "FastAPI вызывает зависимость до path operation и передаёт результат как аргумент.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Почему зависимость get_db использует yield, а не return?",
                                "answer": "yield позволяет выполнить код после передачи сессии (закрытие db.close()) после того, как обработчик завершит работу — гарантированно, даже при исключении, аналогично try/finally.",
                                "explanation": "Ключевое — гарантированная очистка ресурсов после использования.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите зависимость get_current_user(user: User = Depends(get_current_user)) для эндпоинта GET /me, возвращающего текущего пользователя.",
                                "answer": "@app.get('/me')\ndef me(user: User = Depends(get_current_user)):\n    return user",
                                "explanation": "Важно использовать Depends(get_current_user) как тип параметра эндпоинта.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Каким классом/функцией оборачивают зависимость в параметре эндпоинта?",
                                    "options": ["Depends", "Inject", "Provide", "UseDependency"],
                                    "answer": "Depends",
                                },
                                {
                                    "question": "Зачем использовать Depends(get_db) вместо создания сессии прямо в обработчике?",
                                    "options": [
                                        "Это единственный способ создать сессию",
                                        "Чтобы переиспользовать логику получения и закрытия сессии во всех эндпоинтах",
                                        "Это ускоряет запросы к БД",
                                        "Depends обязателен в FastAPI",
                                    ],
                                    "answer": "Чтобы переиспользовать логику получения и закрытия сессии во всех эндпоинтах",
                                },
                                {
                                    "question": "Что используется в зависимости, чтобы гарантировать очистку ресурсов после запроса?",
                                    "options": ["return", "yield", "raise", "pass"],
                                    "answer": "yield",
                                },
                                {
                                    "question": "Может ли одна зависимость зависеть от другой через Depends?",
                                    "options": ["Нет, только одна зависимость на эндпоинт", "Да, зависимости можно вкладывать друг в друга", "Только для аутентификации", "Только при использовании middleware"],
                                    "answer": "Да, зависимости можно вкладывать друг в друга",
                                },
                                {
                                    "question": "Для чего обычно используют Depends(get_current_user)?",
                                    "options": [
                                        "Чтобы подключиться к Redis",
                                        "Чтобы получить и проверить авторизованного пользователя в защищённом эндпоинте",
                                        "Чтобы создать таблицу в БД",
                                        "Чтобы сгенерировать документацию",
                                    ],
                                    "answer": "Чтобы получить и проверить авторизованного пользователя в защищённом эндпоинте",
                                },
                            ],
                        },
                    },
                    {
                        "title": "SQLAlchemy: подключение базы данных",
                        "slug": "fastapi-sqlalchemy",
                        "order": 5,
                        "youtube_url": "https://www.youtube.com/watch?v=GxpG-4WBDMQ",
                        "duration_minutes": 28,
                        "content": """## SQLAlchemy в FastAPI

SQLAlchemy — самый популярный ORM для Python: позволяет работать с
базой данных через Python-объекты, не писать SQL вручную.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://user:password@localhost/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## Модель (таблица)

```python
from sqlalchemy import Column, Integer, String, Float

class Item(Base):
    __tablename__ = "items"

    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
```

`Base.metadata.create_all(bind=engine)` создаёт таблицы в БД.

## Зависимость get_db

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## CRUD-операции

```python
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Не найдено")
    return item

@app.post("/items/", status_code=201)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404)
    db.delete(item)
    db.commit()
```

## Alembic: миграции схемы

```bash
alembic init alembic
alembic revision --autogenerate -m "create items table"
alembic upgrade head
```

Alembic отслеживает изменения моделей и генерирует SQL-миграции автоматически.""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Что делает db.refresh(item) после db.commit()?",
                                "options": [
                                    "Откатывает транзакцию",
                                    "Обновляет объект данными из БД (в том числе auto-generated id)",
                                    "Удаляет объект из сессии",
                                    "Начинает новую транзакцию",
                                ],
                                "answer": "Обновляет объект данными из БД (в том числе auto-generated id)",
                                "explanation": "После commit() id и другие auto-generated поля появляются только в БД — refresh() подтягивает их в объект.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Зачем get_db использует yield и try/finally вместо простого return?",
                                "answer": "yield позволяет выполнить код после завершения запроса (db.close()) — finally гарантирует закрытие сессии даже при исключении в обработчике. С return сессия никогда не закроется при ошибке.",
                                "explanation": "Ключевое — гарантированное освобождение ресурса при любом исходе.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите SQLAlchemy-запрос, возвращающий все Item с price > 100.",
                                "answer": "items = db.query(Item).filter(Item.price > 100).all()",
                                "explanation": "Важны db.query(Model), .filter() и .all().",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Что такое ORM?",
                                    "options": [
                                        "Open Routing Module",
                                        "Object-Relational Mapper — работа с БД через объекты Python",
                                        "Online Request Manager",
                                        "Output Response Model",
                                    ],
                                    "answer": "Object-Relational Mapper — работа с БД через объекты Python",
                                },
                                {
                                    "question": "db.query(Item).first() возвращает...",
                                    "options": ["Список всех Item", "Первый Item или None", "Количество записей", "ID первой записи"],
                                    "answer": "Первый Item или None",
                                },
                                {
                                    "question": "Для чего нужен alembic upgrade head?",
                                    "options": [
                                        "Запускает FastAPI сервер",
                                        "Применяет все не применённые миграции к БД",
                                        "Создаёт новую миграцию",
                                        "Откатывает последнюю миграцию",
                                    ],
                                    "answer": "Применяет все не применённые миграции к БД",
                                },
                                {
                                    "question": "Что нужно вызвать после db.add(obj), чтобы запись попала в БД?",
                                    "options": ["db.push()", "db.save()", "db.commit()", "db.apply()"],
                                    "answer": "db.commit()",
                                },
                                {
                                    "question": "autoflush=False в sessionmaker означает...",
                                    "options": [
                                        "Отключает автоматический commit",
                                        "Не сбрасывает изменения в БД до явного flush/commit",
                                        "Отключает кэш SQLAlchemy",
                                        "Запрещает UPDATE-запросы",
                                    ],
                                    "answer": "Не сбрасывает изменения в БД до явного flush/commit",
                                },
                            ],
                        },
                    },
                    {
                        "title": "JWT авторизация в FastAPI",
                        "slug": "fastapi-jwt",
                        "order": 6,
                        "youtube_url": "https://www.youtube.com/watch?v=7neUG4KkNAM",
                        "duration_minutes": 30,
                        "content": """## Что такое JWT

JWT (JSON Web Token) — стандарт для передачи аутентификационных данных.
Структура: `заголовок.полезная_нагрузка.подпись` (base64url, разделённые `.`).

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyQGEuY29tIn0.xSIG...
```

Сервер подписывает токен секретным ключом и не хранит сессии — клиент
сам несёт все данные.

## Хэширование паролей

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

Никогда не храните пароли открытым текстом — только bcrypt-хэш.

## Создание и проверка токена

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "super-secret-key"
ALGORITHM  = "HS256"

def create_access_token(data: dict, expires_minutes: int = 60) -> str:
    payload = {**data, "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

## Защищённые маршруты

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    try:
        payload = decode_token(token)
        user = db.query(User).filter(User.email == payload["sub"]).first()
        if not user:
            raise HTTPException(401, "Пользователь не найден")
        return user
    except JWTError:
        raise HTTPException(401, "Неверный токен")

@app.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return current_user
```

## Логин: выдача токена

```python
@app.post("/api/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Неверные данные")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
```""",
                        "exercises": [
                            {
                                "type": ExerciseType.mcq,
                                "question": "Почему нельзя хранить пароли в открытом виде в БД?",
                                "options": [
                                    "Они занимают слишком много места",
                                    "При утечке БД злоумышленник получит пароли всех пользователей",
                                    "Это нарушает синтаксис SQLAlchemy",
                                    "FastAPI автоматически шифрует их при хранении",
                                ],
                                "answer": "При утечке БД злоумышленник получит пароли всех пользователей",
                                "explanation": "bcrypt-хэш необратим — даже при утечке БД пароли защищены.",
                            },
                            {
                                "type": ExerciseType.open,
                                "question": "Чем JWT-авторизация отличается от сессионной (server-side sessions)?",
                                "answer": "JWT: все данные хранятся в токене у клиента, сервер не держит состояния — масштабируется горизонтально. Сессии: сервер хранит состояние (в Redis/DB), клиент хранит только ID сессии — легче инвалидировать.",
                                "explanation": "Ключевое — stateless (JWT) vs stateful (sessions), плюсы и минусы масштабируемости и инвалидации.",
                            },
                            {
                                "type": ExerciseType.code,
                                "question": "Напишите функцию create_token(email: str), создающую JWT с полем 'sub' равным email и сроком 30 минут.",
                                "answer": "def create_token(email: str) -> str:\n    payload = {\n        'sub': email,\n        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)\n    }\n    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')",
                                "explanation": "Важны поля sub (subject) и exp (expiration) в payload.",
                            },
                        ],
                        "test": {
                            "pass_threshold": 70,
                            "time_limit": 10,
                            "questions": [
                                {
                                    "question": "Из скольких частей состоит JWT токен?",
                                    "options": ["1", "2", "3", "4"],
                                    "answer": "3",
                                },
                                {
                                    "question": "Какой алгоритм хэширования паролей используется в passlib для FastAPI?",
                                    "options": ["MD5", "SHA-256", "bcrypt", "AES"],
                                    "answer": "bcrypt",
                                },
                                {
                                    "question": "OAuth2PasswordBearer(tokenUrl=...) сообщает FastAPI...",
                                    "options": [
                                        "Где создать таблицу пользователей",
                                        "По какому URL клиент получает токен (для документации Swagger)",
                                        "Как декодировать JWT",
                                        "Где хранить токены",
                                    ],
                                    "answer": "По какому URL клиент получает токен (для документации Swagger)",
                                },
                                {
                                    "question": "Что произойдёт, если передать истёкший JWT токен?",
                                    "options": [
                                        "Сервер обновит его автоматически",
                                        "jose.jwt.decode поднимет JWTError",
                                        "Декодирование пройдёт успешно",
                                        "Возникнет ошибка 500",
                                    ],
                                    "answer": "jose.jwt.decode поднимет JWTError",
                                },
                                {
                                    "question": "Поле 'sub' в JWT payload обозначает...",
                                    "options": [
                                        "Subscription (подписку)",
                                        "Subject — идентификатор субъекта (обычно email или user_id)",
                                        "Subtype токена",
                                        "Дату создания",
                                    ],
                                    "answer": "Subject — идентификатор субъекта (обычно email или user_id)",
                                },
                            ],
                        },
                    },
                ],
            },
        ],
    },
    {
        "title": "Fullstack разработчик",
        "slug": "fullstack",
        "description": "Frontend + Backend вместе: от вёрстки до API. Стеки этого направления — общие с курсами Frontend и Backend, прогресс синхронизирован.",
        "icon": "🧩",
        "order": 3,
        "stacks": [],
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for course_data in COURSES:
            course = db.query(Course).filter(Course.slug == course_data["slug"]).first()
            if not course:
                course = Course(
                    title=course_data["title"],
                    slug=course_data["slug"],
                    description=course_data["description"],
                    icon=course_data["icon"],
                    order=course_data["order"],
                )
                db.add(course)
                db.flush()
                print(f"+ курс: {course.title}")

            for stack_data in course_data["stacks"]:
                stack = db.query(Stack).filter(Stack.slug == stack_data["slug"]).first()
                if not stack:
                    stack = Stack(
                        title=stack_data["title"],
                        slug=stack_data["slug"],
                        description=stack_data["description"],
                        order=stack_data["order"],
                        course_id=course.id,
                    )
                    db.add(stack)
                    db.flush()
                    print(f"  + стек: {stack.title}")

                for lesson_data in stack_data["lessons"]:
                    lesson = db.query(Lesson).filter(Lesson.slug == lesson_data["slug"]).first()
                    if not lesson:
                        lesson = Lesson(
                            title=lesson_data["title"],
                            slug=lesson_data["slug"],
                            content=lesson_data["content"],
                            order=lesson_data["order"],
                            stack_id=stack.id,
                            youtube_url=lesson_data.get("youtube_url"),
                            duration_minutes=lesson_data.get("duration_minutes"),
                        )
                        db.add(lesson)
                        db.flush()
                        print(f"    + урок: {lesson.title}")

                        for i, ex in enumerate(lesson_data["exercises"]):
                            db.add(
                                Exercise(
                                    type=ex["type"],
                                    question=ex["question"],
                                    answer=ex["answer"],
                                    options=ex.get("options"),
                                    explanation=ex.get("explanation"),
                                    lesson_id=lesson.id,
                                    order=i + 1,
                                )
                            )

                        test_data = lesson_data["test"]
                        db.add(
                            Test(
                                lesson_id=lesson.id,
                                pass_threshold=test_data["pass_threshold"],
                                time_limit=test_data.get("time_limit"),
                                questions=test_data["questions"],
                            )
                        )
                    else:
                        changed = False
                        for field in ("youtube_url", "duration_minutes"):
                            val = lesson_data.get(field)
                            if val is not None and getattr(lesson, field) != val:
                                setattr(lesson, field, val)
                                changed = True
                        if changed:
                            print(f"    ~ обновлён: {lesson.title}")

        db.commit()
        print("Готово.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
