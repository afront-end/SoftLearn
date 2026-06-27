"use client";

import { motion } from "framer-motion";
import { ArrowRight, BookOpen, CheckCircle2, Layers, Loader2 } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { api, ApiError, ProgressOverviewOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

function ProgressBar({ value, total }: { value: number; total: number }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-foreground/10">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="h-full rounded-full bg-gradient-to-r from-primary to-primary-2"
      />
    </div>
  );
}

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const token = useAuthStore((s) => s.token);
  const [overview, setOverview] = useState<ProgressOverviewOut | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError("Войдите, чтобы увидеть свой прогресс");
      return;
    }
    setError(null);
    api
      .getProgressOverview()
      .then(setOverview)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Не удалось загрузить прогресс"));
  }, [token]);

  if (error) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-red-500">{error}</p>
      </>
    );
  }

  if (!overview) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Loader2 className="animate-spin text-muted" />
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-8 sm:px-6 sm:py-10">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="gradient-text text-2xl font-bold sm:text-3xl">
            {user ? `Привет, ${user.name}!` : "Личный кабинет"}
          </h1>
          <p className="mt-1 text-muted">Ваш прогресс по всем направлениям</p>
        </motion.div>

        <div className="mt-6 grid grid-cols-2 gap-3 sm:gap-4">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card rounded-2xl p-4 sm:p-5"
          >
            <div className="flex items-center gap-2 text-muted">
              <Layers size={16} />
              <span className="text-xs sm:text-sm">Стеков пройдено</span>
            </div>
            <p className="mt-2 text-2xl font-bold sm:text-3xl">{overview.stacks_completed_total}</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
            className="glass-card rounded-2xl p-4 sm:p-5"
          >
            <div className="flex items-center gap-2 text-muted">
              <CheckCircle2 size={16} />
              <span className="text-xs sm:text-sm">Уроков пройдено</span>
            </div>
            <p className="mt-2 text-2xl font-bold sm:text-3xl">{overview.lessons_completed_total}</p>
          </motion.div>
        </div>

        <div className="mt-8 space-y-4">
          {overview.courses.map((course, i) => (
            <motion.div
              key={course.course_id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="glass-card rounded-2xl p-5"
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="text-xl">{course.course_icon}</span>
                  <h3 className="font-semibold">{course.course_title}</h3>
                </div>
                <Link
                  href={`/courses/${course.course_slug}`}
                  className="flex items-center gap-1 text-sm font-medium text-primary hover:underline"
                >
                  Продолжить <ArrowRight size={14} />
                </Link>
              </div>

              <div className="mt-4 space-y-3">
                <div>
                  <div className="mb-1 flex items-center justify-between text-xs text-muted">
                    <span className="flex items-center gap-1">
                      <Layers size={12} /> Стеки
                    </span>
                    <span>
                      {course.stacks_completed} / {course.stacks_total}
                    </span>
                  </div>
                  <ProgressBar value={course.stacks_completed} total={course.stacks_total} />
                </div>
                <div>
                  <div className="mb-1 flex items-center justify-between text-xs text-muted">
                    <span className="flex items-center gap-1">
                      <BookOpen size={12} /> Уроки
                    </span>
                    <span>
                      {course.lessons_completed} / {course.lessons_total}
                    </span>
                  </div>
                  <ProgressBar value={course.lessons_completed} total={course.lessons_total} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </main>
    </>
  );
}
