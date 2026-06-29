"use client";

import { motion } from "framer-motion";

interface Direction {
  icon: string;
  title: string;
  description: string;
}

const DIRECTIONS: Direction[] = [
  {
    icon: "🎨",
    title: "Frontend",
    description: "Создаёшь то, что видит и с чем взаимодействует пользователь: интерфейсы, анимации, вёрстка.",
  },
  {
    icon: "⚙️",
    title: "Backend",
    description: "Пишешь серверную логику, базы данных и API — то, что работает «под капотом» приложения.",
  },
  {
    icon: "🧩",
    title: "Fullstack",
    description: "Совмещаешь frontend и backend — строишь продукт от интерфейса до базы данных целиком.",
  },
  {
    icon: "📊",
    title: "Data & AI",
    description: "Работаешь с данными, статистикой и моделями машинного обучения, ищешь закономерности.",
  },
  {
    icon: "📱",
    title: "Mobile",
    description: "Разрабатываешь приложения для смартфонов на iOS и Android.",
  },
  {
    icon: "🛠️",
    title: "DevOps",
    description: "Настраиваешь серверы, облако, CI/CD — отвечаешь за то, чтобы всё стабильно работало и деплоилось.",
  },
  {
    icon: "🔍",
    title: "QA",
    description: "Находишь и предотвращаешь ошибки, продумываешь тест-кейсы, следишь за качеством продукта.",
  },
];

export function ItDirections() {
  return (
    <section className="mx-auto max-w-4xl px-6 pb-16">
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold tracking-tight">Что такое IT и какие в нём направления</h2>
        <p className="mt-2 text-sm text-muted">
          IT — это не одна профессия, а множество направлений с разными задачами и складом мышления.
          Вот основные из них.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {DIRECTIONS.map((d, i) => (
          <motion.div
            key={d.title}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06 }}
            className="glass-card flex flex-col gap-2 rounded-2xl p-5"
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary-2 text-lg">
              {d.icon}
            </div>
            <h3 className="font-semibold">{d.title}</h3>
            <p className="text-sm text-muted">{d.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
