"use client";

import { motion, useReducedMotion } from "framer-motion";
import { CheckCircle2, ChevronRight, Loader2, XCircle } from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { CodeExercise } from "@/components/practice/code-exercise";
import { McqExercise } from "@/components/practice/mcq-exercise";
import { OpenExercise } from "@/components/practice/open-exercise";
import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
import { api, ApiError, ExerciseCheckOut, ExerciseOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

const TYPE_LABEL: Record<string, string> = {
  mcq: "Выбор ответа",
  open: "Открытый вопрос",
  code: "Код",
};

export default function PracticePage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const router = useRouter();
  const reduce = useReducedMotion();
  const token = useAuthStore((s) => s.token);

  const [exercises, setExercises] = useState<ExerciseOut[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [checking, setChecking] = useState(false);
  const [result, setResult] = useState<ExerciseCheckOut | null>(null);

  useEffect(() => {
    if (!token) {
      setError("Войдите, чтобы открыть практику");
      return;
    }
    setError(null);
    api
      .getExercises(lessonSlug)
      .then(setExercises)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Не удалось загрузить практику"));
  }, [lessonSlug, token]);

  const current = exercises?.[index];

  async function handleCheck() {
    if (!current || !answer.trim()) return;
    setChecking(true);
    try {
      const res = await api.checkExercise(current.id, answer);
      setResult(res);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Не удалось проверить ответ");
    } finally {
      setChecking(false);
    }
  }

  function handleNext() {
    setResult(null);
    setAnswer("");
    if (exercises && index + 1 < exercises.length) {
      setIndex(index + 1);
    } else {
      router.push(`/lessons/${lessonSlug}/test`);
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

  if (!exercises) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Loader2 className="animate-spin text-muted" />
      </div>
    );
  }

  if (exercises.length === 0 || !current) {
    return (
      <>
        <Navbar />
        <main className="mx-auto max-w-2xl flex-1 px-6 py-12 text-center">
          <p className="text-muted">В этом уроке нет задач для практики.</p>
          <button
            onClick={() => router.push(`/lessons/${lessonSlug}/test`)}
            className="mt-4 rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
          >
            Перейти к тесту →
          </button>
        </main>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-2xl flex-1 px-6 py-12">
        <Breadcrumb
          items={[
            { label: "Главная", href: "/" },
            { label: "Практика" },
          ]}
        />

        <div className="mb-4 mt-4 flex items-center justify-between text-sm text-muted">
          <span>
            Задача {index + 1} из {exercises.length}
          </span>
          <span className="rounded-full border border-border bg-surface-2 px-3 py-1 text-xs font-medium text-ai">
            {TYPE_LABEL[current.type]}
          </span>
        </div>

        <motion.div key={current.id} initial={reduce ? false : { opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <Card className="p-6">
            <p className="font-medium leading-relaxed">{current.question}</p>

            <div className="mt-4">
              {current.type === "mcq" && current.options && (
                <McqExercise
                  options={current.options}
                  selected={answer || null}
                  disabled={!!result}
                  onSelect={setAnswer}
                />
              )}
              {current.type === "open" && (
                <OpenExercise value={answer} disabled={!!result} onChange={setAnswer} />
              )}
              {current.type === "code" && (
                <CodeExercise value={answer} disabled={!!result} onChange={setAnswer} />
              )}
            </div>

            {result && (
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                className={`mt-4 flex gap-2 rounded-xl p-3 text-sm ${
                  result.correct ? "bg-success/10 text-success" : "bg-danger/10 text-danger"
                }`}
              >
                {result.correct ? (
                  <CheckCircle2 size={16} className="mt-0.5 shrink-0" />
                ) : (
                  <XCircle size={16} className="mt-0.5 shrink-0" />
                )}
                <div>
                  <p className="font-medium">{result.correct ? "Верно!" : "Неверно"}</p>
                  {result.correct_answer && (
                    <p className="mt-1 text-muted">Правильный ответ: {result.correct_answer}</p>
                  )}
                  {result.explanation && <p className="mt-1 text-muted">{result.explanation}</p>}
                </div>
              </motion.div>
            )}

            <div className="mt-6 flex justify-end gap-2">
              {!result ? (
                <button
                  onClick={handleCheck}
                  disabled={checking || !answer.trim()}
                  className="flex items-center gap-2 rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md disabled:opacity-50"
                >
                  {checking && <Loader2 size={14} className="animate-spin" />}
                  Проверить
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  className="flex items-center gap-2 rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
                >
                  {index + 1 < exercises.length ? "Следующая задача" : "К тесту"}
                  <ChevronRight size={14} />
                </button>
              )}
            </div>
          </Card>
        </motion.div>
      </main>
    </>
  );
}
