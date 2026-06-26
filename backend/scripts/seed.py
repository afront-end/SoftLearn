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
                ],
            },
        ],
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
