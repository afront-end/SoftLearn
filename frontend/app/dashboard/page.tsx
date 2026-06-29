"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, BookOpen, CheckCircle2, Layers, Loader2 } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { ProgressBar } from "@/components/ui/progress-bar";
import { ProgressRing } from "@/components/ui/progress-ring";
import { api, ApiError, ProgressOverviewOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const token = useAuthStore((s) => s.token);
  const reduce = useReducedMotion();
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
        <p className="mt-6 text-center text-danger">{error}</p>
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

  const totalStacks = overview.courses.reduce((sum, c) => sum + c.stacks_total, 0);
  const totalLessons = overview.courses.reduce((sum, c) => sum + c.lessons_total, 0);

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-8 sm:px-6 sm:py-10">
        <Breadcrumb items={[{ label: "softlearn", href: "/" }, { label: "dashboard.tsx" }]} />

        <motion.div initial={reduce ? false : { opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-3">
          <h1 className="text-gradient text-2xl font-bold sm:text-3xl">
            {user ? `Привет, ${user.name}!` : "Личный кабинет"}
          </h1>
          <p className="mt-1 text-muted">Ваш прогресс по всем направлениям</p>
        </motion.div>

        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-[auto_auto_1fr] sm:gap-4">
          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="panel flex items-center gap-4 rounded-xl p-4 sm:p-5"
          >
            <ProgressRing value={overview.stacks_completed_total} total={Math.max(totalStacks, 1)} colorVar="var(--accent)" />
            <div>
              <div className="flex items-center gap-1.5 text-muted">
                <Layers size={14} />
                <span className="text-xs">стеков</span>
              </div>
              <p className="font-mono text-xl font-bold">
                {overview.stacks_completed_total}/{totalStacks}
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
            className="panel flex items-center gap-4 rounded-xl p-4 sm:p-5"
          >
            <ProgressRing value={overview.lessons_completed_total} total={Math.max(totalLessons, 1)} colorVar="var(--success)" />
            <div>
              <div className="flex items-center gap-1.5 text-muted">
                <CheckCircle2 size={14} />
                <span className="text-xs">уроков</span>
              </div>
              <p className="font-mono text-xl font-bold">
                {overview.lessons_completed_total}/{totalLessons}
              </p>
            </div>
          </motion.div>
        </div>

        <div className="mt-8 space-y-4">
          {overview.courses.map((course, i) => (
            <motion.div
              key={course.course_id}
              initial={reduce ? false : { opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="code-window"
            >
              <div className="code-window-titlebar justify-between">
                <div className="flex items-center gap-2">
                  <span className="code-dot" style={{ background: "var(--danger)" }} />
                  <span className="code-dot" style={{ background: "var(--warning)" }} />
                  <span className="code-dot" style={{ background: "var(--success)" }} />
                  <span className="ml-2 font-mono text-[11px] text-muted">{course.course_slug}.progress</span>
                </div>
                <Link
                  href={`/courses/${course.course_slug}`}
                  className="flex items-center gap-1 text-xs font-medium text-accent hover:underline"
                >
                  продолжить <ArrowRight size={12} />
                </Link>
              </div>

              <div className="p-5">
                <h3 className="font-semibold">{course.course_title}</h3>

                <div className="mt-4 space-y-3">
                  <div>
                    <div className="mb-1 flex items-center justify-between font-mono text-xs text-muted">
                      <span className="flex items-center gap-1">
                        <Layers size={12} /> stacks
                      </span>
                      <span>
                        {course.stacks_completed} / {course.stacks_total}
                      </span>
                    </div>
                    <ProgressBar value={course.stacks_completed} total={course.stacks_total} colorClassName="bg-accent" />
                  </div>
                  <div>
                    <div className="mb-1 flex items-center justify-between font-mono text-xs text-muted">
                      <span className="flex items-center gap-1">
                        <BookOpen size={12} /> lessons
                      </span>
                      <span>
                        {course.lessons_completed} / {course.lessons_total}
                      </span>
                    </div>
                    <ProgressBar value={course.lessons_completed} total={course.lessons_total} colorClassName="bg-success" />
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </main>
    </>
  );
}
