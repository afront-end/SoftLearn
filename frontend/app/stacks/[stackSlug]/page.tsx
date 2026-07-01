"use client";

import { motion, useReducedMotion } from "framer-motion";
import {
  BookOpen,
  CheckCircle2,
  ChevronRight,
  Clock,
  Code2,
  ClipboardList,
  Lock,
  PlayCircle,
} from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { api, ApiError, LessonWithProgress, StackLessonsOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

function ProgressBar({ value, total }: { value: number; total: number }) {
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;
  return (
    <div className="flex items-center gap-3">
      <div className="h-2 flex-1 overflow-hidden rounded-full bg-surface-2">
        <motion.div
          className="h-full rounded-full bg-accent"
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        />
      </div>
      <span className="shrink-0 text-sm font-medium tabular-nums text-muted">
        {pct}%
      </span>
    </div>
  );
}

function LessonRow({
  lesson,
  index,
  reduce,
}: {
  lesson: LessonWithProgress;
  index: number;
  reduce: boolean | null;
}) {
  const locked = lesson.status === "locked";
  const active = lesson.status === "in_progress";
  const done = lesson.status === "completed";

  const icon = locked ? (
    <Lock size={16} />
  ) : done ? (
    <CheckCircle2 size={16} />
  ) : (
    <BookOpen size={16} />
  );

  const iconBg = locked
    ? "bg-surface-2 text-muted"
    : done
    ? "bg-success/10 text-success"
    : "bg-accent/10 text-accent";

  const row = (
    <motion.div
      initial={reduce ? false : { opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.04 }}
    >
      <Card
        hover={!locked}
        className={`p-4 transition-all ${locked ? "opacity-55" : ""} ${
          active ? "ring-1 ring-accent/30" : ""
        }`}
      >
        <div className="flex items-center justify-between gap-3">
          <div className="flex min-w-0 items-center gap-3">
            <div
              className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${iconBg}`}
            >
              {icon}
            </div>

            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted">{lesson.order}.</span>
                <span
                  className={`truncate font-medium ${
                    active ? "text-accent" : ""
                  }`}
                >
                  {lesson.title}
                </span>
              </div>
              <div className="mt-1 flex flex-wrap items-center gap-2">
                {lesson.duration_minutes && (
                  <span className="flex items-center gap-1 text-xs text-muted">
                    <Clock size={11} />
                    {lesson.duration_minutes} мин
                  </span>
                )}
                {lesson.has_exercises && (
                  <span className="flex items-center gap-1 rounded-md bg-surface-2 px-1.5 py-0.5 text-xs text-muted">
                    <Code2 size={11} />
                    Практика
                  </span>
                )}
                {lesson.has_test && (
                  <span className="flex items-center gap-1 rounded-md bg-surface-2 px-1.5 py-0.5 text-xs text-muted">
                    <ClipboardList size={11} />
                    Тест
                  </span>
                )}
              </div>
            </div>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            {active && (
              <span className="flex items-center gap-1 rounded-lg bg-accent/10 px-2 py-1 text-xs font-medium text-accent">
                <PlayCircle size={12} />
                Активный
              </span>
            )}
            <StatusBadge status={lesson.status} />
            {!locked && (
              <ChevronRight
                size={16}
                className="text-muted transition-transform group-hover:translate-x-1"
              />
            )}
          </div>
        </div>
      </Card>
    </motion.div>
  );

  if (locked) {
    return (
      <div
        key={lesson.id}
        title="Завершите предыдущий урок, чтобы разблокировать"
      >
        {row}
      </div>
    );
  }

  return (
    <Link key={lesson.id} href={`/lessons/${lesson.slug}`} className="block">
      {row}
    </Link>
  );
}

export default function StackPage() {
  const { stackSlug } = useParams<{ stackSlug: string }>();
  const token = useAuthStore((s) => s.token);
  const reduce = useReducedMotion();
  const [stack, setStack] = useState<StackLessonsOut | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError("Войдите, чтобы увидеть уроки стека");
      return;
    }
    setError(null);
    api
      .getStackLessons(stackSlug)
      .then(setStack)
      .catch((err) =>
        setError(err instanceof ApiError ? err.message : "Ошибка загрузки стека")
      );
  }, [stackSlug, token]);

  if (error) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-danger">{error}</p>
      </>
    );
  }

  if (!stack) {
    return (
      <>
        <Navbar />
        <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-12">
          <div className="shimmer mb-3 h-8 w-1/3 rounded-lg" />
          <div className="shimmer mb-8 h-4 w-2/3 rounded-lg" />
          <div className="space-y-3">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="shimmer h-16 rounded-2xl" />
            ))}
          </div>
        </main>
      </>
    );
  }

  const total = stack.lessons.length;
  const done = stack.completed_count;

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-12">
        <Breadcrumb
          items={[{ label: "Главная", href: "/" }, { label: stack.title }]}
        />

        <motion.div
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-3"
        >
          <h1 className="text-3xl font-bold tracking-tight">{stack.title}</h1>
          {stack.description && (
            <p className="mt-2 leading-relaxed text-muted">{stack.description}</p>
          )}

          {total > 0 && (
            <div className="mt-4 rounded-xl border border-border bg-surface-2/50 px-4 py-3">
              <div className="mb-2 flex items-center justify-between text-sm">
                <span className="font-medium">Прогресс стека</span>
                <span className="text-muted">
                  {done} из {total} уроков завершено
                </span>
              </div>
              <ProgressBar value={done} total={total} />
            </div>
          )}
        </motion.div>

        <div className="mt-6 space-y-2">
          {stack.lessons.map((lesson, i) => (
            <LessonRow key={lesson.id} lesson={lesson} index={i} reduce={reduce} />
          ))}
        </div>
      </main>
    </>
  );
}
