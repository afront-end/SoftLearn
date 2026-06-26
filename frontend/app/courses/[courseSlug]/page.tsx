"use client";

import { motion } from "framer-motion";
import { CheckCircle2, ChevronRight, Lock, PlayCircle } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { api, ApiError, CourseWithStacks } from "@/lib/api";
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

export default function CoursePage() {
  const { courseSlug } = useParams<{ courseSlug: string }>();
  const token = useAuthStore((s) => s.token);
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
        <p className="mt-6 text-center text-red-500">{error}</p>
      </>
    );
  }

  if (!course) {
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
          <h1 className="gradient-text text-3xl font-bold tracking-tight">{course.title}</h1>
          <p className="mt-2 text-muted">{course.description}</p>
        </motion.div>

        <div className="mt-8 space-y-3">
          {course.stacks.map((stack, i) => {
            const Icon = STATUS_ICON[stack.status];
            const locked = stack.status === "locked";

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
                  <Icon size={18} className={STATUS_COLOR[stack.status]} />
                  <span className="font-medium">{stack.title}</span>
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
              <div key={stack.id}>{content}</div>
            ) : (
              <Link key={stack.id} href={`/stacks/${stack.slug}`}>
                {content}
              </Link>
            );
          })}
        </div>
      </main>
    </>
  );
}
