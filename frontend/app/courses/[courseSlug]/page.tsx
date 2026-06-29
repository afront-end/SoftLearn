"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ChevronRight, Layers, Lock } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
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
        <main className="mx-auto w-full max-w-3xl flex-1 px-6 py-12">
          <div className="shimmer mb-3 h-8 w-1/3 rounded-lg" />
          <div className="shimmer mb-8 h-4 w-2/3 rounded-lg" />
          <div className="space-y-3">
            {[0, 1, 2].map((i) => (
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
        <Breadcrumb items={[{ label: "Главная", href: "/" }, { label: course.title }]} />

        <motion.div initial={reduce ? false : { opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-3">
          <h1 className="text-3xl font-bold tracking-tight">{course.title}</h1>
          <p className="mt-2 leading-relaxed text-muted">{course.description}</p>
        </motion.div>

        <div className="mt-8 space-y-3">
          {course.stacks.map((stack, i) => {
            const locked = stack.status === "locked";

            const row = (
              <motion.div
                initial={reduce ? false : { opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Card hover={!locked} className={`flex items-center justify-between p-5 ${locked ? "opacity-60" : ""}`}>
                  <div className="flex items-center gap-3">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${locked ? "bg-surface-2 text-muted" : "bg-accent/10 text-accent"}`}>
                      {locked ? <Lock size={17} /> : <Layers size={17} />}
                    </div>
                    <span className="font-semibold">{stack.title}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <StatusBadge status={stack.status} />
                    {!locked && (
                      <ChevronRight size={18} className="text-muted transition-transform group-hover:translate-x-1" />
                    )}
                  </div>
                </Card>
              </motion.div>
            );

            return locked ? (
              <div key={stack.id}>{row}</div>
            ) : (
              <Link key={stack.id} href={`/stacks/${stack.slug}`} className="block">
                {row}
              </Link>
            );
          })}
        </div>
      </main>
    </>
  );
}
