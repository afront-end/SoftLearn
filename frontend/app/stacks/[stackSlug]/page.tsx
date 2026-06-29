"use client";

import { motion, useReducedMotion } from "framer-motion";
import { BookOpen, ChevronRight, Lock } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { api, ApiError, StackLessonsOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

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
      .catch((err) => setError(err instanceof ApiError ? err.message : "Ошибка загрузки стека"));
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

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-12">
        <Breadcrumb
          items={[
            { label: "Главная", href: "/" },
            { label: stack.title },
          ]}
        />

        <motion.div initial={reduce ? false : { opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-3">
          <h1 className="text-3xl font-bold tracking-tight">{stack.title}</h1>
          {stack.description && <p className="mt-2 leading-relaxed text-muted">{stack.description}</p>}
        </motion.div>

        <div className="mt-8 space-y-3">
          {stack.lessons.map((lesson, i) => {
            const locked = lesson.status === "locked";

            const row = (
              <motion.div
                initial={reduce ? false : { opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Card hover={!locked} className={`flex items-center justify-between p-5 ${locked ? "opacity-60" : ""}`}>
                  <div className="flex items-center gap-3">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${locked ? "bg-surface-2 text-muted" : "bg-accent/10 text-accent"}`}>
                      {locked ? <Lock size={17} /> : <BookOpen size={17} />}
                    </div>
                    <span className="font-semibold">
                      {lesson.order}. {lesson.title}
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <StatusBadge status={lesson.status} />
                    {!locked && (
                      <ChevronRight size={18} className="text-muted transition-transform group-hover:translate-x-1" />
                    )}
                  </div>
                </Card>
              </motion.div>
            );

            return locked ? (
              <div key={lesson.id}>{row}</div>
            ) : (
              <Link key={lesson.id} href={`/lessons/${lesson.slug}`} className="block">
                {row}
              </Link>
            );
          })}
        </div>
      </main>
    </>
  );
}
