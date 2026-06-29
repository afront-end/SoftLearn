"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, Compass } from "lucide-react";
import { useRouter } from "next/navigation";

import { Card } from "@/components/ui/card";

export function CareerQuizBanner() {
  const router = useRouter();
  const reduce = useReducedMotion();

  return (
    <section className="mx-auto max-w-4xl px-6 pb-20">
      <motion.div
        initial={reduce ? false : { opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.4 }}
      >
        <Card className="relative overflow-hidden p-10 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-ai/10 text-ai">
            <Compass size={22} strokeWidth={1.75} />
          </div>

          <h2 className="mt-5 text-2xl font-bold tracking-tight">Не знаешь, с чего начать?</h2>
          <p className="mx-auto mt-2 max-w-md leading-relaxed text-muted">
            Ответь на несколько вопросов о своих интересах — AI подскажет, какое направление в IT тебе
            подходит больше всего, с объяснением почему.
          </p>

          <motion.button
            whileTap={{ scale: 0.98 }}
            onClick={() => router.push("/onboarding/quiz")}
            className="mt-6 inline-flex items-center gap-2 rounded-full bg-accent px-6 py-3 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
          >
            Пройти Career Path Quiz
            <ArrowRight size={16} />
          </motion.button>

          <p className="mt-3 text-xs text-muted">Это займёт около 2 минут</p>
        </Card>
      </motion.div>
    </section>
  );
}
