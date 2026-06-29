"use client";

import { motion, useReducedMotion } from "framer-motion";
import { Compass, Loader2 } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { api, ApiError, QuizQuestion, QuizResultOut } from "@/lib/api";

export default function CareerQuizPage() {
  const reduce = useReducedMotion();
  const [questions, setQuestions] = useState<QuizQuestion[] | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<QuizResultOut | null>(null);

  useEffect(() => {
    api
      .getCareerQuiz()
      .then((qs) => {
        setQuestions(qs);
        setAnswers(new Array(qs.length).fill(-1));
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : "Не удалось загрузить квиз"));
  }, []);

  function selectAnswer(qIndex: number, optionIndex: number) {
    setAnswers((prev) => prev.map((a, i) => (i === qIndex ? optionIndex : a)));
  }

  async function handleSubmit() {
    setSubmitting(true);
    setError(null);
    try {
      const res = await api.submitCareerQuiz(answers);
      setResult(res);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Не удалось обработать результат");
    } finally {
      setSubmitting(false);
    }
  }

  if (!questions) {
    return (
      <>
        <Navbar />
        <div className="flex flex-1 items-center justify-center">
          {error ? <p className="text-danger">{error}</p> : <Loader2 className="animate-spin text-muted" />}
        </div>
      </>
    );
  }

  if (result) {
    const maxScore = Math.max(...Object.values(result.scores), 1);

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
              <span className="ml-2 font-mono text-[11px] text-muted">result.json</span>
            </div>
            <div className="p-8">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-xl bg-ai/15 text-ai">
                <Compass size={26} strokeWidth={1.75} />
              </div>
              <p className="mt-4 font-mono text-xs text-muted">тебе подходит направление</p>
              <h1 className="text-gradient text-2xl font-bold">{result.direction_title}</h1>
              <p className="mt-3 text-sm text-muted">{result.explanation}</p>

              <div className="mt-6 space-y-2 text-left">
                {Object.entries(result.scores)
                  .sort((a, b) => b[1] - a[1])
                  .map(([slug, score]) => (
                    <div key={slug} className="flex items-center gap-2 font-mono text-xs">
                      <span className="w-20 shrink-0 truncate text-muted">{slug}</span>
                      <div className="h-1.5 flex-1 rounded-full bg-surface-2">
                        <div
                          className="h-1.5 rounded-full bg-accent"
                          style={{ width: `${(score / maxScore) * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
              </div>

              {result.course_slug ? (
                <Link
                  href={`/courses/${result.course_slug}`}
                  className="mt-6 inline-flex rounded-lg bg-accent px-4 py-2 text-sm font-medium text-accent-foreground"
                >
                  Перейти к курсу →
                </Link>
              ) : (
                <p className="mt-6 text-sm text-muted">
                  Этот курс пока в разработке, загляни на главную, чтобы выбрать из доступных направлений.
                </p>
              )}

              <div>
                <Link href="/" className="mt-4 inline-block text-sm text-muted hover:text-foreground">
                  На главную
                </Link>
              </div>
            </div>
          </motion.div>
        </main>
      </>
    );
  }

  const allAnswered = answers.every((a) => a >= 0);

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl flex-1 px-6 py-10">
        <Breadcrumb items={[{ label: "softlearn", href: "/" }, { label: "career-quiz.run" }]} />

        <div className="mt-3 flex items-center gap-2">
          <Compass size={20} className="text-ai" />
          <h1 className="text-2xl font-bold">Career Path Quiz</h1>
        </div>
        <p className="mt-1 text-sm text-muted">
          Ответь на несколько вопросов о своих интересах, AI подскажет, какое направление в IT тебе подходит.
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
                {q.options.map((option, optionIndex) => (
                  <button
                    key={option}
                    type="button"
                    onClick={() => selectAnswer(qIndex, optionIndex)}
                    className={`w-full rounded-lg border px-4 py-2.5 text-left text-sm transition-colors ${
                      answers[qIndex] === optionIndex
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

        {error && <p className="mt-4 text-sm text-danger">{error}</p>}

        <button
          onClick={handleSubmit}
          disabled={!allAnswered || submitting}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-lg bg-accent px-4 py-3 text-sm font-medium text-accent-foreground transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {submitting && <Loader2 size={14} className="animate-spin" />}
          Узнать направление
        </button>
      </main>
    </>
  );
}
