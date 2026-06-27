"use client";

import { motion } from "framer-motion";
import { CheckCircle2, ChevronRight, Loader2, XCircle } from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { CodeExercise } from "@/components/practice/code-exercise";
import { McqExercise } from "@/components/practice/mcq-exercise";
import { OpenExercise } from "@/components/practice/open-exercise";
import { Navbar } from "@/components/navbar";
import { api, ApiError, ExerciseCheckOut, ExerciseOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function PracticePage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const router = useRouter();
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
        <p className="mt-6 text-center text-red-500">{error}</p>
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
        <main className="mx-auto max-w-2xl flex-1 px-6 py-10 text-center">
          <p className="text-muted">В этом уроке нет задач для практики.</p>
          <button
            onClick={() => router.push(`/lessons/${lessonSlug}/test`)}
            className="mt-4 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-2 text-sm font-medium text-white"
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
      <main className="mx-auto max-w-2xl flex-1 px-6 py-10">
        <div className="mb-4 flex items-center justify-between text-sm text-muted">
          <span>
            Задача {index + 1} / {exercises.length}
          </span>
          <span className="rounded-full bg-foreground/5 px-2 py-0.5">{current.type}</span>
        </div>

        <motion.div
          key={current.id}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card rounded-2xl p-6"
        >
          <p className="font-medium">{current.question}</p>

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
                result.correct
                  ? "bg-emerald-500/10 text-emerald-500"
                  : "bg-red-500/10 text-red-500"
              }`}
            >
              {result.correct ? <CheckCircle2 size={16} className="mt-0.5 shrink-0" /> : <XCircle size={16} className="mt-0.5 shrink-0" />}
              <div>
                <p className="font-medium">{result.correct ? "Верно!" : "Неверно"}</p>
                {result.correct_answer && <p className="mt-1 text-muted">Правильный ответ: {result.correct_answer}</p>}
                {result.explanation && <p className="mt-1 text-muted">{result.explanation}</p>}
              </div>
            </motion.div>
          )}

          <div className="mt-6 flex justify-end gap-2">
            {!result ? (
              <button
                onClick={handleCheck}
                disabled={checking || !answer.trim()}
                className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
              >
                {checking && <Loader2 size={14} className="animate-spin" />}
                Проверить
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-2 text-sm font-medium text-white"
              >
                {index + 1 < exercises.length ? "Следующая задача" : "К тесту"}
                <ChevronRight size={14} />
              </button>
            )}
          </div>
        </motion.div>
      </main>
    </>
  );
}
