"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Bug, Database, Layers, Server, Smartphone, SquareCode, Workflow } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import { Card } from "@/components/ui/card";

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
];

export function ItDirections() {
  const reduce = useReducedMotion();

  return (
    <section className="mx-auto max-w-5xl px-6 pb-20">
      <div className="mb-10 text-center">
        <h2 className="text-3xl font-bold tracking-tight">Какие есть направления в IT</h2>
        <p className="mx-auto mt-3 max-w-lg leading-[1.7] text-muted">
          IT — это не одна профессия, а множество направлений с разными задачами и складом мышления.
        </p>
      </div>

      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {DIRECTIONS.map((d, i) => (
          <motion.div
            key={d.title}
            initial={reduce ? false : { opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ delay: i * 0.05, duration: 0.5 }}
          >
            <Card hover className="flex h-full flex-col gap-3 p-6">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-accent/10 text-accent">
                <d.icon size={22} strokeWidth={1.75} />
              </div>
              <h3 className="font-semibold">{d.title}</h3>
              <p className="text-sm leading-relaxed text-muted">{d.description}</p>
            </Card>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
