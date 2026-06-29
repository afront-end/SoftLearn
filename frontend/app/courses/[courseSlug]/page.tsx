"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ChevronRight, Folder, FolderOpen, Lock } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { StatusBadge } from "@/components/ui/status-badge";
import { api, ApiError, CourseWithStacks } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

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
        <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-10">
          <div className="shimmer mb-3 h-8 w-1/3 rounded-md" />
          <div className="shimmer mb-8 h-4 w-2/3 rounded-md" />
          <div className="space-y-3">
            {[0, 1, 2].map((i) => (
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
        <Breadcrumb items={[{ label: "softlearn", href: "/" }, { label: course.slug }]} />

        <motion.div
          initial={reduce ? false : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-3"
        >
          <h1 className="text-gradient text-3xl font-bold tracking-tight">{course.title}</h1>
          <p className="mt-2 text-muted">{course.description}</p>
        </motion.div>

        <div className="mt-8 panel rounded-xl">
          <div className="flex items-center gap-2 border-b border-border px-4 py-2.5 font-mono text-[12px] text-muted">
            <FolderOpen size={14} /> {course.slug}/
          </div>
          <div className="divide-y divide-border">
            {course.stacks.map((stack, i) => {
              const locked = stack.status === "locked";

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
                      <Folder size={15} className="text-accent" />
                    )}
                    <span className="font-medium">{stack.title}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <StatusBadge status={stack.status} />
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
                <div key={stack.id}>{row}</div>
              ) : (
                <Link key={stack.id} href={`/stacks/${stack.slug}`}>
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
