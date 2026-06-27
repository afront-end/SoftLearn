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

        db.commit()
        print("Готово.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
