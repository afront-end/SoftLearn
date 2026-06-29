"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ChevronRight, FileCode2, FolderOpen, Lock } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
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
        <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-10">
          <div className="shimmer mb-3 h-8 w-1/3 rounded-md" />
          <div className="shimmer mb-8 h-4 w-2/3 rounded-md" />
          <div className="space-y-3">
            {[0, 1, 2, 3].map((i) => (
              <div key={i} className="shimmer h-14 rounded-lg" />
            ))}
          </div>
        </main>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-10">
        <Breadcrumb items={[{ label: "softlearn", href: "/" }, { label: stack.slug }]} />

        <motion.div
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-3"
        >
          <h1 className="text-gradient text-3xl font-bold tracking-tight">{stack.title}</h1>
          {stack.description && <p className="mt-2 text-muted">{stack.description}</p>}
        </motion.div>

        <div className="mt-8 panel rounded-xl">
          <div className="flex items-center gap-2 border-b border-border px-4 py-2.5 font-mono text-[12px] text-muted">
            <FolderOpen size={14} /> {stack.slug}/
          </div>
          <div className="divide-y divide-border">
            {stack.lessons.map((lesson, i) => {
              const locked = lesson.status === "locked";

              const row = (
                <motion.div
                  initial={reduce ? false : { opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className={`group flex items-center justify-between px-4 py-3.5 transition-colors ${
                    locked ? "" : "hover:bg-surface-2"
                  }`}
                >
                  <div className={`flex items-center gap-3 ${locked ? "locked-line" : ""}`}>
                    {locked ? (
                      <Lock size={15} className="text-muted" />
                    ) : (
                      <FileCode2 size={15} className="text-accent" />
                    )}
                    <span className="font-medium">
                      {String(lesson.order).padStart(2, "0")}.{lesson.title}
                    </span>
                  </div>
                  <div className="flex items-center gap-3">
                    <StatusBadge status={lesson.status} />
                    {!locked && (
                      <ChevronRight
                        size={16}
                        className="text-muted transition-transform group-hover:translate-x-1 group-hover:text-accent"
                      />
                    )}
                  </div>
                </motion.div>
              );

              return locked ? (
                <div key={lesson.id}>{row}</div>
              ) : (
                <Link key={lesson.id} href={`/lessons/${lesson.slug}`}>
                  {row}
                </Link>
              );
            })}
          </div>
        </div>
      </main>
    </>
  );
}
