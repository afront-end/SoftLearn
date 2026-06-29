"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Award, Loader2 } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
import { api, ApiError, PlacementQuestion, PlacementResultOut } from "@/lib/api";

const LEVEL_LABEL: Record<string, string> = {
  beginner: "Начальный",
  intermediate: "Средний",
  advanced: "Продвинутый",
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
        <main className="mx-auto max-w-xl flex-1 px-6 py-12">
          <motion.div initial={reduce ? false : { opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
            <Card className="p-8 text-center">
              <Award size={48} className="mx-auto text-accent" />
              <h1 className="mt-4 text-3xl font-bold">{result.score}%</h1>
              <p className="mt-1 text-muted">
                Ваш уровень:{" "}
                <span className="font-semibold text-foreground">{LEVEL_LABEL[result.result_level]}</span>
              </p>
              {result.unlocked_stacks.length > 0 && (
                <p className="mt-3 text-sm text-muted">
                  Разблокированы стеки: {result.unlocked_stacks.join(", ")}
                </p>
              )}
              <Link
                href={`/courses/${courseSlug}`}
                className="mt-6 inline-flex rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
              >
                К курсу →
              </Link>
            </Card>
          </motion.div>
        </main>
      </>
    );
  }

  const allAnswered = answers.every((a) => a.trim() !== "");

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl flex-1 px-6 py-12">
        <Breadcrumb
          items={[
            { label: "Главная", href: "/" },
            { label: "Вступительный тест" },
          ]}
        />

        <h1 className="mt-4 text-2xl font-bold">Вступительный тест</h1>
        <p className="mt-1 leading-relaxed text-muted">
          Вопросы идут от простого к сложному. Так мы поймём, какие темы вы уже знаете, и откроем нужные стеки.
        </p>

        <div className="mt-6 space-y-4">
          {questions.map((q, qIndex) => (
            <motion.div
              key={qIndex}
              initial={reduce ? false : { opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: qIndex * 0.05 }}
            >
              <Card className="p-5">
                <p className="font-medium">
                  {qIndex + 1}. {q.question}
                </p>
                <div className="mt-3 space-y-2">
                  {q.options.map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => selectAnswer(qIndex, option)}
                      className={`w-full rounded-xl border px-4 py-2.5 text-left text-sm transition-colors ${
                        answers[qIndex] === option
                          ? "border-accent bg-accent/10"
                          : "border-border hover:border-accent/40"
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        <button
          onClick={handleSubmit}
          disabled={!allAnswered || submitting}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-full bg-accent px-4 py-3 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md disabled:opacity-50"
        >
          {submitting && <Loader2 size={14} className="animate-spin" />}
          Завершить тест
        </button>
      </main>
    </>
  );
}
