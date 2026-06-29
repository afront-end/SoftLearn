"use client";

import { motion } from "framer-motion";
import { Compass, Loader2 } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { api, ApiError, QuizQuestion, QuizResultOut } from "@/lib/api";

export default function CareerQuizPage() {
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
          {error ? <p className="text-red-500">{error}</p> : <Loader2 className="animate-spin text-muted" />}
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
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card rounded-2xl p-8 text-center"
          >
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-primary-2 text-2xl">
              {result.direction_icon}
            </div>
            <p className="mt-4 text-sm text-muted">Тебе подходит направление</p>
            <h1 className="gradient-text text-2xl font-bold">{result.direction_title}</h1>
            <p className="mt-3 text-sm text-muted">{result.explanation}</p>

            <div className="mt-6 space-y-2 text-left">
              {Object.entries(result.scores)
                .sort((a, b) => b[1] - a[1])
                .map(([slug, score]) => (
                  <div key={slug} className="flex items-center gap-2 text-xs">
                    <span className="w-20 shrink-0 text-muted">{slug}</span>
                    <div className="h-2 flex-1 rounded-full bg-foreground/10">
                      <div
                        className="h-2 rounded-full bg-gradient-to-r from-primary to-primary-2"
                        style={{ width: `${(score / maxScore) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
            </div>

            {result.course_slug ? (
              <Link
                href={`/courses/${result.course_slug}`}
                className="mt-6 inline-flex rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-2 text-sm font-medium text-white"
              >
                Перейти к курсу →
              </Link>
            ) : (
              <p className="mt-6 text-sm text-muted">
                Этот курс пока в разработке — загляни на главную, чтобы выбрать из доступных направлений.
              </p>
            )}

            <div>
              <Link href="/" className="mt-4 inline-block text-sm text-muted hover:text-foreground">
                На главную
              </Link>
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
        <div className="flex items-center gap-2">
          <Compass size={20} className="text-primary" />
          <h1 className="gradient-text text-2xl font-bold">Career Path Quiz</h1>
        </div>
        <p className="mt-1 text-sm text-muted">
          Ответь на несколько вопросов о своих интересах — AI подскажет, какое направление в IT тебе подходит.
        </p>

        <div className="mt-6 space-y-5">
          {questions.map((q, qIndex) => (
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
                {q.options.map((option, optionIndex) => (
                  <button
                    key={option}
                    type="button"
                    onClick={() => selectAnswer(qIndex, optionIndex)}
                    className={`w-full rounded-xl border px-4 py-2.5 text-left text-sm transition-colors ${
                      answers[qIndex] === optionIndex
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

        {error && <p className="mt-4 text-sm text-red-500">{error}</p>}

        <button
          onClick={handleSubmit}
          disabled={!allAnswered || submitting}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-3 text-sm font-medium text-white disabled:opacity-50"
        >
          {submitting && <Loader2 size={14} className="animate-spin" />}
          Узнать направление
        </button>
      </main>
    </>
  );
}
