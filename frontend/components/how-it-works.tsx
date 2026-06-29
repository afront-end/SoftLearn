"use client";

import { motion, useReducedMotion } from "framer-motion";
import { BookOpen, ShieldCheck, SquareCode } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import { Card } from "@/components/ui/card";

interface Step {
  icon: LucideIcon;
  title: string;
  description: string;
}

const STEPS: Step[] = [
  {
    icon: BookOpen,
    title: "Объяснение",
    description: "Читаешь тему урока и сразу можешь спросить у AI-ассистента, если что-то непонятно.",
  },
  {
    icon: SquareCode,
    title: "Практика",
    description: "Закрепляешь тему на задачах: тесты, открытые вопросы и код в редакторе.",
  },
  {
    icon: ShieldCheck,
    title: "Тест-барьер",
    description: "Сдаёшь короткий тест по теме — без этого следующий урок не откроется.",
  },
];

export function HowItWorks() {
  const reduce = useReducedMotion();

  return (
    <section className="mx-auto max-w-4xl px-6 pb-20">
      <div className="mb-10 text-center">
        <h2 className="text-3xl font-bold tracking-tight">Как устроен урок</h2>
        <p className="mx-auto mt-3 max-w-lg leading-[1.7] text-muted">
          Один и тот же понятный цикл для каждой темы — никаких пропущенных шагов.
        </p>
      </div>

      <div className="grid gap-5 sm:grid-cols-3">
        {STEPS.map((step, i) => (
          <motion.div
            key={step.title}
            initial={reduce ? false : { opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ delay: i * 0.08, duration: 0.5 }}
            className="relative"
          >
            <Card className="flex h-full flex-col gap-3 p-6">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-accent/10 text-accent">
                <step.icon size={22} strokeWidth={1.75} />
              </div>
              <h3 className="font-semibold">
                {i + 1}. {step.title}
              </h3>
              <p className="text-sm leading-relaxed text-muted">{step.description}</p>
            </Card>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
