"use client";

import { motion } from "framer-motion";
import { ArrowRight, Code2, GraduationCap, Loader2, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { api, ApiError, CourseOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function Home() {
  const router = useRouter();
  const token = useAuthStore((s) => s.token);
  const user = useAuthStore((s) => s.user);
  const [courses, setCourses] = useState<CourseOut[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listCourses()
      .then(setCourses)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Не удалось загрузить курсы"));
  }, []);

  useEffect(() => {
    if (token && user && !user.onboarded) {
      router.push("/onboarding");
    }
  }, [token, user, router]);

  return (
    <>
      <Navbar />
      <main className="relative flex-1 overflow-hidden">
        <div className="aurora-bg" />

        <section className="mx-auto max-w-3xl px-6 pt-20 pb-12 text-center">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mx-auto mb-5 flex w-fit items-center gap-2 rounded-full border border-card-border bg-foreground/5 px-4 py-1.5 text-sm text-muted"
          >
            <Sparkles size={14} className="text-primary" /> Один путь. Без хаоса источников.
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl font-bold tracking-tight sm:text-5xl"
          >
            Учись программировать
            <br />
            <span className="gradient-text">структурно, а не хаотично</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mx-auto mt-5 max-w-xl text-muted"
          >
            SoftLearn проводит тебя по одному чёткому курсу — объяснение, практика
            и тест-барьер на каждом шаге — вместо метаний между YouTube, статьями
            и форумами.
          </motion.p>

          {!token && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="mt-8 flex justify-center gap-3"
            >
              <Link
                href="/register"
                className="group flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-5 py-2.5 text-sm font-medium text-white shadow-lg shadow-primary/30 transition-all hover:shadow-primary/50"
              >
                Начать бесплатно
                <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              </Link>
              <Link
                href="/login"
                className="rounded-xl border border-card-border px-5 py-2.5 text-sm font-medium transition-colors hover:bg-foreground/5"
              >
                Войти
              </Link>
            </motion.div>
          )}
        </section>

        <section className="mx-auto max-w-4xl px-6 pb-20">
          {error && <p className="text-center text-red-500">{error}</p>}

          {!courses && !error && (
            <div className="flex justify-center py-10">
              <Loader2 className="animate-spin text-muted" />
            </div>
          )}

          <div className="grid gap-4 sm:grid-cols-2">
            {courses?.map((course, i) => (
              <motion.div
                key={course.id}
                initial={{ opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
              >
                <Link
                  href={`/courses/${course.slug}`}
                  className="glass-card group flex h-full flex-col gap-3 rounded-2xl p-6 transition-all hover:-translate-y-1 hover:border-primary/50 hover:shadow-xl hover:shadow-primary/10"
                >
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary-2 text-xl">
                    {course.icon ?? <Code2 size={20} className="text-white" />}
                  </div>
                  <h3 className="text-lg font-semibold">{course.title}</h3>
                  <p className="text-sm text-muted">{course.description}</p>
                  <span className="mt-auto flex items-center gap-1 text-sm font-medium text-primary opacity-0 transition-opacity group-hover:opacity-100">
                    Перейти <ArrowRight size={14} />
                  </span>
                </Link>
                {user?.experienced && (
                  <Link
                    href={`/placement/${course.slug}`}
                    className="mt-2 flex items-center justify-center gap-1.5 rounded-xl border border-card-border px-3 py-2 text-xs font-medium text-muted transition-colors hover:border-primary/40 hover:text-primary"
                  >
                    <GraduationCap size={14} /> Пройти вступительный тест по этому направлению
                  </Link>
                )}
              </motion.div>
            ))}
          </div>
        </section>
      </main>
    </>
  );
}
