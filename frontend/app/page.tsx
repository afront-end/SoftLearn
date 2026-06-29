"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, GraduationCap, Loader2 } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { AssistantWidget } from "@/components/assistant-widget";
import { CareerQuizBanner } from "@/components/career-quiz-banner";
import { ItDirections } from "@/components/it-directions";
import { Navbar } from "@/components/navbar";
import { HeroCodeBackdrop } from "@/components/ui/hero-code-backdrop";
import { TypingHeading } from "@/components/ui/typing-heading";
import { api, ApiError, CourseOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function Home() {
  const router = useRouter();
  const reduce = useReducedMotion();
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
        <section className="relative mx-auto max-w-3xl px-6 pt-16 pb-12 text-center">
          <HeroCodeBackdrop />

          <motion.div
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mx-auto mb-5 flex w-fit items-center gap-2 rounded-md border border-border bg-surface px-3 py-1 font-mono text-[12px] text-muted"
          >
            <span className="text-success">$</span> npm run learn -- --no-chaos
          </motion.div>

          <motion.h1
            initial={reduce ? false : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl font-bold tracking-tight sm:text-5xl"
          >
            Учись программировать
            <br />
            <TypingHeading text="структурно, а не хаотично" className="text-gradient" />
          </motion.h1>

          <motion.p
            initial={reduce ? false : { opacity: 0, y: 20 }}
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
              initial={reduce ? false : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="mt-8 flex justify-center gap-3"
            >
              <Link
                href="/register"
                className="group flex items-center gap-2 rounded-lg bg-accent px-5 py-2.5 text-sm font-medium text-accent-foreground transition-opacity hover:opacity-90"
              >
                Начать бесплатно
                <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              </Link>
              <Link
                href="/login"
                className="rounded-lg border border-border px-5 py-2.5 text-sm font-medium transition-colors hover:border-accent/50"
              >
                Войти
              </Link>
            </motion.div>
          )}
        </section>

        {token && (
          <>
            <ItDirections />
            <CareerQuizBanner />
          </>
        )}

        <section className="mx-auto max-w-4xl px-6 pb-20">
          {token && <h2 className="mb-6 text-center text-2xl font-bold tracking-tight">Доступные курсы</h2>}

          {error && <p className="text-center text-danger">{error}</p>}

          {!courses && !error && (
            <div className="flex justify-center py-10">
              <Loader2 className="animate-spin text-muted" />
            </div>
          )}

          <div className="grid gap-4 sm:grid-cols-2">
            {courses?.map((course, i) => (
              <motion.div
                key={course.id}
                initial={reduce ? false : { opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.3 }}
                transition={{ delay: i * 0.08, duration: 0.5 }}
              >
                <Link
                  href={`/courses/${course.slug}`}
                  className="code-window group flex h-full flex-col transition-all hover:-translate-y-1 hover:border-accent/50 hover:shadow-lg"
                >
                  <div className="code-window-titlebar justify-start">
                    <span className="code-dot" style={{ background: "var(--danger)" }} />
                    <span className="code-dot" style={{ background: "var(--warning)" }} />
                    <span className="code-dot" style={{ background: "var(--success)" }} />
                    <span className="ml-2 truncate font-mono text-[11px] text-muted">{course.slug}.dir</span>
                  </div>
                  <div className="flex flex-1 flex-col gap-2 p-5">
                    <h3 className="font-mono text-lg font-semibold">{course.title}</h3>
                    <p className="text-sm text-muted">{course.description}</p>
                    <span className="mt-auto flex items-center gap-1 text-sm font-medium text-accent opacity-0 transition-opacity group-hover:opacity-100">
                      Перейти <ArrowRight size={14} />
                    </span>
                  </div>
                </Link>
                {user?.experienced && (
                  <Link
                    href={`/placement/${course.slug}`}
                    className="mt-2 flex items-center justify-center gap-1.5 rounded-lg border border-border px-3 py-2 text-xs font-medium text-muted transition-colors hover:border-accent/40 hover:text-accent"
                  >
                    <GraduationCap size={14} /> Пройти вступительный тест по этому направлению
                  </Link>
                )}
              </motion.div>
            ))}
          </div>
        </section>
      </main>
      {token && <AssistantWidget />}
    </>
  );
}
