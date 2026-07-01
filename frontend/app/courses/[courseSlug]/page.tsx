"use client";

import { motion, useReducedMotion } from "framer-motion";
import { BookOpen, ChevronRight, Layers, Lock, PlayCircle } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { api, ApiError, CourseWithStacks, StackWithProgress } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

function ProgressBar({ value, total }: { value: number; total: number }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;
  return (
    <div className="mt-2 flex items-center gap-2">
      <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-surface-2">
        <div
          className="h-full rounded-full bg-accent transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="min-w-[3rem] text-right text-xs text-muted">
        {value}/{total}
      </span>
    </div>
  );
}

function StackCard({ stack, index, reduce }: { stack: StackWithProgress; index: number; reduce: boolean | null }) {
  const locked = stack.status === "locked";
  const inProgress = stack.status === "in_progress";

  const card = (
    <motion.div
      initial={reduce ? false : { opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
    >
      <Card
        hover={!locked}
        className={`p-5 transition-shadow ${locked ? "opacity-55" : ""} ${inProgress ? "ring-1 ring-accent/30" : ""}`}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3">
            <div
              className={`mt-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${
                locked ? "bg-surface-2 text-muted" : "bg-accent/10 text-accent"
              }`}
            >
              {locked ? <Lock size={17} /> : <Layers size={17} />}
            </div>
            <div>
              <p className="font-semibold leading-snug">{stack.title}</p>
              {stack.description && (
                <p className="mt-0.5 text-sm text-muted line-clamp-1">{stack.description}</p>
              )}
              {stack.lesson_count > 0 && (
                <div className="mt-1 flex items-center gap-1 text-xs text-muted">
                  <BookOpen size={12} />
                  <span>{stack.lesson_count} уроков</span>
                </div>
              )}
            </div>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <StatusBadge status={stack.status} />
            {inProgress && (
              <div className="flex items-center gap-1 rounded-lg bg-accent/10 px-2 py-1 text-xs font-medium text-accent">
                <PlayCircle size={13} />
                <span>Продолжить</span>
              </div>
            )}
            {!locked && (
              <ChevronRight size={18} className="text-muted transition-transform group-hover:translate-x-1" />
            )}
          </div>
        </div>

        {!locked && stack.lesson_count > 0 && (
          <ProgressBar value={stack.completed_count} total={stack.lesson_count} />
        )}
      </Card>
    </motion.div>
  );

  return locked ? (
    <div key={stack.id}>{card}</div>
  ) : (
    <Link key={stack.id} href={`/stacks/${stack.slug}`} className="block">
      {card}
    </Link>
  );
}

export default function CoursePage() {
  const { courseSlug } = useParams<{ courseSlug: string }>();
  const token = useAuthStore((s) => s.token);
  const reduce = useReducedMotion();
  const [course, setCourse] = useState<CourseWithStacks | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError("Войдите, чтобы увидеть стеки курса");
      return;
    }
    setError(null);
    api
      .getCourseStacks(courseSlug)
      .then(setCourse)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Ошибка загрузки курса"));
  }, [courseSlug, token]);

  if (error) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-danger">{error}</p>
      </>
    );
  }

  if (!course) {
    return (
      <>
        <Navbar />
        <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-12">
          <div className="shimmer mb-3 h-8 w-1/3 rounded-lg" />
          <div className="shimmer mb-8 h-4 w-2/3 rounded-lg" />
          <div className="space-y-3">
            {[0, 1, 2].map((i) => (
              <div key={i} className="shimmer h-20 rounded-2xl" />
            ))}
          </div>
        </main>
      </>
    );
  }

  const totalLessons = course.stacks.reduce((s, st) => s + st.lesson_count, 0);
  const doneLessons = course.stacks.reduce((s, st) => s + st.completed_count, 0);

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-12">
        <Breadcrumb items={[{ label: "Главная", href: "/" }, { label: course.title }]} />

        <motion.div initial={reduce ? false : { opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-3">
          <h1 className="text-3xl font-bold tracking-tight">{course.title}</h1>
          <p className="mt-2 leading-relaxed text-muted">{course.description}</p>

          {totalLessons > 0 && (
            <div className="mt-4 rounded-xl border border-border bg-surface-2/50 px-4 py-3">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium">Общий прогресс</span>
                <span className="text-muted">
                  {doneLessons} из {totalLessons} уроков
                </span>
              </div>
              <ProgressBar value={doneLessons} total={totalLessons} />
            </div>
          )}
        </motion.div>

        <div className="mt-6 space-y-3">
          {course.stacks.map((stack, i) => (
            <StackCard key={stack.id} stack={stack} index={i} reduce={reduce} />
          ))}
        </div>
      </main>
    </>
  );
}
