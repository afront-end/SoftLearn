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
import { Card } from "@/components/ui/card";
import { GradientBlob } from "@/components/ui/gradient-blob";
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
      <main className="relative flex-1">
        <section className="relative overflow-hidden px-6 pt-20 pb-24 text-center sm:pt-28 sm:pb-32">
          <GradientBlob />

          <motion.h1
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            className="mx-auto max-w-3xl text-4xl font-bold leading-[1.1] tracking-tight sm:text-6xl"
          >
            Учись программировать
            <br />
            <span className="text-gradient">структурно, а не хаотично</span>
          </motion.h1>

          <motion.p
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="mx-auto mt-6 max-w-xl text-lg leading-[1.7] text-muted"
          >
            SoftLearn проводит тебя по одному чёткому курсу — объяснение, практика
            и тест-барьер на каждом шаге — вместо метаний между YouTube, статьями
            и форумами.
          </motion.p>

          <motion.div
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="mt-10 flex flex-wrap justify-center gap-3"
          >
            {!token ? (
              <>
                <Link
                  href="/register"
                  className="group flex items-center gap-2 rounded-full bg-accent px-6 py-3 text-base font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
                >
                  Начать обучение
                  <ArrowRight size={18} className="transition-transform group-hover:translate-x-0.5" />
                </Link>
                <Link
                  href="#courses"
                  className="rounded-full border border-border px-6 py-3 text-base font-semibold transition-all hover:-translate-y-0.5 hover:border-accent/40"
                >
                  Посмотреть курсы
                </Link>
              </>
            ) : (
              <Link
                href="/dashboard"
                className="group flex items-center gap-2 rounded-full bg-accent px-6 py-3 text-base font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
              >
                Продолжить обучение
                <ArrowRight size={18} className="transition-transform group-hover:translate-x-0.5" />
              </Link>
            )}
          </motion.div>
        </section>

        <div id="directions">
          <ItDirections />
        </div>

        {token && <CareerQuizBanner />}

        <section id="courses" className="mx-auto max-w-4xl px-6 pb-24">
          <div className="mb-8 text-center">
            <h2 className="text-3xl font-bold tracking-tight">Доступные курсы</h2>
            <p className="mt-2 text-muted">Выбери направление и начни с первого стека</p>
          </div>

          {error && <p className="text-center text-danger">{error}</p>}

          {!courses && !error && (
            <div className="flex justify-center py-10">
              <Loader2 className="animate-spin text-muted" />
            </div>
          )}

          <div className="grid gap-5 sm:grid-cols-2">
            {courses?.map((course, i) => (
              <motion.div
                key={course.id}
                initial={reduce ? false : { opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.3 }}
                transition={{ delay: i * 0.08, duration: 0.5 }}
              >
                <Link href={`/courses/${course.slug}`}>
                  <Card hover className="group flex h-full flex-col gap-3 p-6">
                    <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-accent/10 text-accent">
                      <GraduationCap size={22} strokeWidth={1.75} />
                    </div>
                    <h3 className="text-lg font-semibold">{course.title}</h3>
                    <p className="text-sm leading-relaxed text-muted">{course.description}</p>
                    <span className="mt-auto flex items-center gap-1 text-sm font-semibold text-accent opacity-0 transition-opacity group-hover:opacity-100">
                      Перейти <ArrowRight size={14} />
                    </span>
                  </Card>
                </Link>
                {user?.experienced && (
                  <Link
                    href={`/placement/${course.slug}`}
                    className="mt-2 flex items-center justify-center gap-1.5 rounded-full border border-border px-3 py-2 text-xs font-medium text-muted transition-colors hover:border-accent/40 hover:text-accent"
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
