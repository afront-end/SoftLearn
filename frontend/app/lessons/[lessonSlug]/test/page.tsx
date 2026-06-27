"use client";

import { motion } from "framer-motion";
import { CheckCircle2, Loader2, RotateCcw, XCircle } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { api, ApiError, TestOut, TestResultOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function TestPage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const token = useAuthStore((s) => s.token);

  const [test, setTest] = useState<TestOut | null>(null);
  const [answers, setAnswers] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<TestResultOut | null>(null);

  useEffect(() => {
    if (!token) {
      setError("Войдите, чтобы пройти тест");
      return;
    }
    setError(null);
    api
      .getTest(lessonSlug)
      .then((t) => {
        setTest(t);
        setAnswers(new Array(t.questions.length).fill(""));
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : "Не удалось загрузить тест"));
  }, [lessonSlug, token]);

  function selectAnswer(qIndex: number, option: string) {
    setAnswers((prev) => prev.map((a, i) => (i === qIndex ? option : a)));
  }

  async function handleSubmit() {
    setSubmitting(true);
    try {
      const res = await api.submitTest(lessonSlug, answers);
      setResult(res);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Не удалось отправить тест");
    } finally {
      setSubmitting(false);
    }
  }

  function handleRetry() {
    setResult(null);
    setAnswers(test ? new Array(test.questions.length).fill("") : []);
  }

  if (error) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-red-500">{error}</p>
      </>
    );
  }

  if (!test) {
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
        <main className="mx-auto max-w-2xl flex-1 px-6 py-10">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card rounded-2xl p-8 text-center"
          >
            {result.passed ? (
              <CheckCircle2 size={48} className="mx-auto text-emerald-500" />
            ) : (
              <XCircle size={48} className="mx-auto text-red-500" />
            )}
            <h1 className="mt-4 text-2xl font-bold">{result.score}%</h1>
            <p className="mt-1 text-muted">
              {result.passed ? "Тест пройден! Следующий урок открыт." : `Нужно набрать минимум ${test.pass_threshold}%. Попробуйте снова.`}
            </p>

            {result.mistakes.length > 0 && (
              <div className="mt-6 space-y-3 text-left">
                {result.mistakes.map((m, i) => (
                  <div key={i} className="rounded-xl bg-red-500/10 p-3 text-sm">
                    <p className="font-medium">{m.question}</p>
                    <p className="mt-1 text-muted">Ваш ответ: {m.user_answer}</p>
                    <p className="text-emerald-500">Правильный: {m.correct_answer}</p>
                  </div>
                ))}
              </div>
            )}

            <div className="mt-6 flex justify-center gap-3">
              {!result.passed && (
                <button
                  onClick={handleRetry}
                  className="flex items-center gap-2 rounded-xl border border-card-border px-4 py-2 text-sm font-medium hover:bg-foreground/5"
                >
                  <RotateCcw size={14} /> Попробовать снова
                </button>
              )}
              <Link
                href={result.passed ? "/" : `/lessons/${lessonSlug}`}
                className="rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-2 text-sm font-medium text-white"
              >
                {result.passed ? "К курсам" : "К уроку"}
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
        <h1 className="gradient-text text-2xl font-bold">Тест-барьер</h1>
        <p className="mt-1 text-sm text-muted">
          Нужно набрать минимум {test.pass_threshold}%, чтобы открыть следующий урок.
        </p>

        <div className="mt-6 space-y-5">
          {test.questions.map((q, qIndex) => (
            <motion.div
              key={qIndex}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: qIndex * 0.05 }}
              className="glass-card rounded-2xl p-5"
            >
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
                        ? "border-primary bg-primary/10"
                        : "border-card-border hover:border-primary/40"
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
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {submitting && <Loader2 size={14} className="animate-spin" />}
          Отправить тест
        </button>
      </main>
    </>
  );
}
