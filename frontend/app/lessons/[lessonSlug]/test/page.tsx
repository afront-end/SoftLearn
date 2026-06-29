"use client";

import { motion, useReducedMotion } from "framer-motion";
import { CheckCircle2, Loader2, RotateCcw, XCircle } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { api, ApiError, TestOut, TestResultOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function TestPage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const reduce = useReducedMotion();
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
        <p className="mt-6 text-center text-danger">{error}</p>
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
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="code-window panel-shadow text-center"
          >
            <div className="code-window-titlebar justify-start">
              <span className="code-dot" style={{ background: "var(--danger)" }} />
              <span className="code-dot" style={{ background: "var(--warning)" }} />
              <span className="code-dot" style={{ background: "var(--success)" }} />
              <span className="ml-2 font-mono text-[11px] text-muted">
                test.{result.passed ? "pass" : "fail"}
              </span>
            </div>

            <div className="p-8">
              {result.passed ? (
                <CheckCircle2 size={48} className="mx-auto text-success" />
              ) : (
                <XCircle size={48} className="mx-auto text-danger" />
              )}
              <h1 className="mt-4 font-mono text-2xl font-bold">{result.score}%</h1>
              <p className="mt-1 text-muted">
                {result.passed
                  ? "Тест пройден! Следующий урок открыт."
                  : `Нужно набрать минимум ${test.pass_threshold}%. Попробуйте снова.`}
              </p>

              {result.mistakes.length > 0 && (
                <div className="mt-6 space-y-3 text-left">
                  {result.mistakes.map((m, i) => (
                    <div key={i} className="rounded-lg bg-danger/10 p-3 text-sm">
                      <p className="font-medium">{m.question}</p>
                      <p className="mt-1 text-muted">Ваш ответ: {m.user_answer}</p>
                      <p className="text-success">Правильный: {m.correct_answer}</p>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-6 flex justify-center gap-3">
                {!result.passed && (
                  <button
                    onClick={handleRetry}
                    className="flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium transition-colors hover:border-accent/50"
                  >
                    <RotateCcw size={14} /> Попробовать снова
                  </button>
                )}
                <Link
                  href={result.passed ? "/" : `/lessons/${lessonSlug}`}
                  className="rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-foreground transition-opacity hover:opacity-90"
                >
                  {result.passed ? "К курсам" : "К уроку"}
                </Link>
              </div>
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
        <Breadcrumb
          items={[
            { label: "softlearn", href: "/" },
            { label: lessonSlug, href: `/lessons/${lessonSlug}` },
            { label: "test-barrier.lock" },
          ]}
        />

        <h1 className="mt-4 text-2xl font-bold">Тест-барьер</h1>
        <p className="mt-1 text-sm text-muted">
          Нужно набрать минимум {test.pass_threshold}%, чтобы открыть следующий урок.
        </p>

        <div className="mt-6 space-y-4">
          {test.questions.map((q, qIndex) => (
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
          Отправить тест
        </button>
      </main>
    </>
  );
}
