"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, Compass } from "lucide-react";
import { useRouter } from "next/navigation";

export function CareerQuizBanner() {
  const router = useRouter();
  const reduce = useReducedMotion();

  return (
    <section className="mx-auto max-w-4xl px-6 pb-16">
      <motion.div
        initial={reduce ? false : { opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.4 }}
        className="code-window panel-shadow relative overflow-hidden text-center"
      >
        <div className="code-window-titlebar justify-start">
          <span className="code-dot" style={{ background: "var(--danger)" }} />
          <span className="code-dot" style={{ background: "var(--warning)" }} />
          <span className="code-dot" style={{ background: "var(--success)" }} />
          <span className="ml-2 font-mono text-[11px] text-muted">career-quiz.run</span>
        </div>

        <div className="p-8">
          <div className="mx-auto flex w-fit items-center gap-2 rounded-md border border-border bg-surface-2 px-3 py-1 font-mono text-[12px] text-muted">
            <Compass size={13} className="text-ai" /> не знаешь, с чего начать?
          </div>

          <h2 className="mt-4 text-2xl font-bold tracking-tight">Career Path Quiz</h2>
          <p className="mx-auto mt-2 max-w-md text-sm text-muted">
            Ответь на несколько вопросов о своих интересах — AI подскажет, какое направление в IT тебе
            подходит больше всего, с объяснением почему.
          </p>

          <motion.button
            whileTap={{ scale: 0.98 }}
            onClick={() => router.push("/onboarding/quiz")}
            className="mt-6 inline-flex items-center gap-2 rounded-lg bg-accent px-5 py-2.5 text-sm font-medium text-accent-foreground transition-opacity hover:opacity-90"
          >
            Пройти Career Path Quiz
            <ArrowRight size={16} />
          </motion.button>

          <p className="mt-2 font-mono text-xs text-muted">~2 минуты</p>
        </div>
      </motion.div>
    </section>
  );
}
