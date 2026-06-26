"use client";

import { motion } from "framer-motion";
import { CheckCircle2, ChevronRight, Lock, PlayCircle } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { api, ApiError, StackLessonsOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

const STATUS_ICON = {
  locked: Lock,
  in_progress: PlayCircle,
  completed: CheckCircle2,
} as const;

const STATUS_COLOR = {
  locked: "text-muted",
  in_progress: "text-primary",
  completed: "text-emerald-500",
} as const;

export default function StackPage() {
  const { stackSlug } = useParams<{ stackSlug: string }>();
  const token = useAuthStore((s) => s.token);
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
      .catch((err) => setError(err instanceof ApiError ? err.message : "Ошибка загрузки стека"));
  }, [stackSlug, token]);

  if (error) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-red-500">{error}</p>
      </>
    );
  }

  if (!stack) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-muted">Загрузка...</p>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-10">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="gradient-text text-3xl font-bold tracking-tight">{stack.title}</h1>
          {stack.description && <p className="mt-2 text-muted">{stack.description}</p>}
        </motion.div>

        <div className="mt-8 space-y-3">
          {stack.lessons.map((lesson, i) => {
            const Icon = STATUS_ICON[lesson.status];
            const locked = lesson.status === "locked";

            const content = (
              <motion.div
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className={`glass-card group flex items-center justify-between rounded-xl px-5 py-4 transition-all ${
                  locked ? "opacity-50" : "hover:border-primary/50 hover:shadow-lg hover:shadow-primary/10"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon size={18} className={STATUS_COLOR[lesson.status]} />
                  <span className="font-medium">{lesson.title}</span>
                </div>
                {!locked && (
                  <ChevronRight
                    size={18}
                    className="text-muted transition-transform group-hover:translate-x-1 group-hover:text-primary"
                  />
                )}
              </motion.div>
            );

            return locked ? (
              <div key={lesson.id}>{content}</div>
            ) : (
              <Link key={lesson.id} href={`/lessons/${lesson.slug}`}>
                {content}
              </Link>
            );
          })}
        </div>
      </main>
    </>
  );
}
