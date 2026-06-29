"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Award, Loader2 } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { api, ApiError, PlacementQuestion, PlacementResultOut } from "@/lib/api";

const LEVEL_LABEL: Record<string, string> = {
  beginner: "начальный",
  intermediate: "средний",
  advanced: "продвинутый",
};

export default function PlacementPage() {
  const { courseSlug } = useParams<{ courseSlug: string }>();
  const reduce = useReducedMotion();
  const [questions, setQuestions] = useState<PlacementQuestion[] | null>(null);
  const [answers, setAnswers] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<PlacementResultOut | null>(null);

  useEffect(() => {
    api
      .getPlacementQuestions(courseSlug)
      .then((qs) => {
        setQuestions(qs);
        setAnswers(new Array(qs.length).fill(""));
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : "Не удалось загрузить тест"));
  }, [courseSlug]);

  function selectAnswer(qIndex: number, option: string) {
    setAnswers((prev) => prev.map((a, i) => (i === qIndex ? option : a)));
  }

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const res = await api.submitPlacement(courseSlug, answers);
      setResult(res);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Не удалось отправить тест");
    } finally {
      setSubmitting(false);
    }
  }

  if (error) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-danger">{error}</p>
      </>
    );
  }

  if (!questions) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Loader2 className="animate-spin text-muted" />
      </div>
    );
  }

  if (result) {
    return (
      <>
        <Navbar />
        <main className="mx-auto max-w-xl flex-1 px-6 py-10">
          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="code-window panel-shadow text-center"
          >
            <div className="code-window-titlebar justify-start">
              <span className="code-dot" style={{ background: "var(--danger)" }} />
              <span className="code-dot" style={{ background: "var(--warning)" }} />
              <span className="code-dot" style={{ background: "var(--success)" }} />
              <span className="ml-2 font-mono text-[11px] text-muted">placement.json</span>
            </div>
            <div className="p-8">
              <Award size={48} className="mx-auto text-accent" />
              <h1 className="mt-4 font-mono text-2xl font-bold">{result.score}%</h1>
              <p className="mt-1 text-muted">
                Ваш уровень:{" "}
                <span className="font-mono font-medium text-foreground">
                  {LEVEL_LABEL[result.result_level]}
                </span>
              </p>
              {result.unlocked_stacks.length > 0 && (
                <p className="mt-3 text-sm text-muted">
                  Разблокированы стеки: {result.unlocked_stacks.join(", ")}
                </p>
              )}
              <Link
                href={`/courses/${courseSlug}`}
                className="mt-6 inline-flex rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-foreground transition-opacity hover:opacity-90"
              >
                К курсу →
              </Link>
            </div>
          </motion.div>
        </main>
      </>
    );
  }

  const allAnswered = answers.every((a) => a.trim() !== "");

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl flex-1 px-6 py-10">
        <Breadcrumb items={[{ label: "softlearn", href: "/" }, { label: courseSlug, href: `/courses/${courseSlug}` }, { label: "placement.run" }]} />

        <h1 className="mt-4 text-2xl font-bold">Вступительный тест</h1>
        <p className="mt-1 text-sm text-muted">
          Вопросы идут от простого к сложному. Так мы поймём, какие темы вы уже знаете, и откроем нужные стеки.
        </p>

        <div className="mt-6 space-y-4">
          {questions.map((q, qIndex) => (
            <motion.div
              key={qIndex}
              initial={reduce ? false : { opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: qIndex * 0.05 }}
              className="panel rounded-xl p-5"
            >
              <p className="font-medium">
                <span className="font-mono text-muted">{qIndex + 1}.</span> {q.question}
              </p>
              <div className="mt-3 space-y-2">
                {q.options.map((option) => (
                  <button
                    key={option}
                    type="button"
                    onClick={() => selectAnswer(qIndex, option)}
                    className={`w-full rounded-lg border px-4 py-2.5 text-left text-sm transition-colors ${
                      answers[qIndex] === option
                        ? "border-accent bg-accent/10"
                        : "border-border hover:border-accent/40"
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        <button
          onClick={handleSubmit}
          disabled={!allAnswered || submitting}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-accent px-4 py-3 text-sm font-medium text-accent-foreground transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {submitting && <Loader2 size={14} className="animate-spin" />}
          Завершить тест
        </button>
      </main>
    </>
  );
}
