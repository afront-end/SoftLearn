"use client";

import { motion } from "framer-motion";
import { ArrowRight, Compass } from "lucide-react";
import { useRouter } from "next/navigation";

export function CareerQuizBanner() {
  const router = useRouter();

  return (
    <section className="mx-auto max-w-4xl px-6 pb-16">
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card relative overflow-hidden rounded-2xl border border-primary/30 p-8 text-center"
      >
        <div className="aurora-bg" />
        <div className="relative mx-auto flex w-fit items-center gap-2 rounded-full border border-card-border bg-foreground/5 px-4 py-1.5 text-sm text-muted">
          <Compass size={14} className="text-primary" /> Не знаешь, с чего начать?
        </div>

        <h2 className="relative mt-4 text-2xl font-bold tracking-tight">Career Path Quiz</h2>
        <p className="relative mx-auto mt-2 max-w-md text-sm text-muted">
          Ответь на несколько вопросов о своих интересах — и AI подскажет, какое направление в IT тебе
          подходит больше всего, с объяснением почему.
        </p>

        <motion.button
          whileTap={{ scale: 0.98 }}
          onClick={() => router.push("/onboarding/quiz")}
          className="relative mt-6 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-5 py-2.5 text-sm font-medium text-white shadow-lg shadow-primary/30 transition-all hover:shadow-primary/50"
        >
          Пройти Career Path Quiz
          <ArrowRight size={16} />
        </motion.button>

        <p className="relative mt-2 text-xs text-muted">Это займёт 2 минуты</p>
      </motion.div>
    </section>
  );
}
