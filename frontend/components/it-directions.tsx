"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Bug, Database, Layers, Server, Smartphone, SquareCode, Workflow } from "lucide-react";
import type { LucideIcon } from "lucide-react";

interface Direction {
  icon: LucideIcon;
  title: string;
  description: string;
}

const DIRECTIONS: Direction[] = [
  {
    icon: SquareCode,
    title: "Frontend",
    description: "Создаёшь то, что видит и с чем взаимодействует пользователь: интерфейсы, анимации, вёрстка.",
  },
  {
    icon: Server,
    title: "Backend",
    description: "Пишешь серверную логику, базы данных и API — то, что работает «под капотом» приложения.",
  },
  {
    icon: Layers,
    title: "Fullstack",
    description: "Совмещаешь frontend и backend — строишь продукт от интерфейса до базы данных целиком.",
  },
  {
    icon: Database,
    title: "Data & AI",
    description: "Работаешь с данными, статистикой и моделями машинного обучения, ищешь закономерности.",
  },
  {
    icon: Smartphone,
    title: "Mobile",
    description: "Разрабатываешь приложения для смартфонов на iOS и Android.",
  },
  {
    icon: Workflow,
    title: "DevOps",
    description: "Настраиваешь серверы, облако, CI/CD — отвечаешь за то, чтобы всё стабильно работало и деплоилось.",
  },
  {
    icon: Bug,
    title: "QA",
    description: "Находишь и предотвращаешь ошибки, продумываешь тест-кейсы, следишь за качеством продукта.",
  },
];

export function ItDirections() {
  const reduce = useReducedMotion();

  return (
    <section className="mx-auto max-w-4xl px-6 pb-16">
      <div className="mb-6 text-center">
        <h2 className="text-2xl font-bold tracking-tight">Что такое IT и какие в нём направления</h2>
        <p className="mt-2 text-sm text-muted">
          IT — это не одна профессия, а множество направлений с разными задачами и складом мышления.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {DIRECTIONS.map((d, i) => (
          <motion.div
            key={d.title}
            initial={reduce ? false : { opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ delay: i * 0.05, duration: 0.5 }}
            className="panel flex flex-col gap-2 rounded-xl p-5 transition-colors hover:border-accent/40"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-surface-2 text-accent">
              <d.icon size={18} strokeWidth={1.75} />
            </div>
            <h3 className="font-mono text-sm font-semibold">{d.title}</h3>
            <p className="text-sm text-muted">{d.description}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
