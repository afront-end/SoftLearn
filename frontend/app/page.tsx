"use client";

import { motion, useReducedMotion } from "framer-motion";
import { ArrowDown, ArrowRight, Loader2 } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { AssistantWidget } from "@/components/assistant-widget";
import { CareerQuizBanner } from "@/components/career-quiz-banner";
import { Footer } from "@/components/footer";
import { HowItWorks } from "@/components/how-it-works";
import { ItDirections } from "@/components/it-directions";
import { Navbar } from "@/components/navbar";
import { Card } from "@/components/ui/card";
import { GradientBlob } from "@/components/ui/gradient-blob";
import { api, ApiError, CourseOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

const DIRECTION_META: Record<string, { icon: string; level: string }> = {
  frontend: { icon: "🎨", level: "Начинающий" },
  backend: { icon: "⚙️", level: "Средний" },
  fullstack: { icon: "🔥", level: "Продвинутый" },
  ai: { icon: "🤖", level: "Скоро" },
};

interface CourseCard extends CourseOut {
  stacksTotal: number | null;
}

export default function Home() {
  const router = useRouter();
  const reduce = useReducedMotion();
  const token = useAuthStore((s) => s.token);
  const user = useAuthStore((s) => s.user);
  const [courses, setCourses] = useState<CourseCard[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listCourses()
      .then(async (list) => {
        const withStacks = await Promise.all(
          list.map(async (course) => {
            const stacksTotal = await api
              .getCourseStacks(course.slug)
              .then((c) => c.stacks.length)
              .catch(() => null);
            return { ...course, stacksTotal };
          })
        );
        setCourses(withStacks);
      })
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
        <section className="relative overflow-hidden px-6 pt-20 pb-16 text-center sm:pt-28 sm:pb-20">
          <GradientBlob />

          <motion.span
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
            className="inline-flex items-center rounded-full border border-accent/30 bg-accent/10 px-4 py-1.5 text-xs font-medium text-accent"
          >
            Для самоучек-программистов
          </motion.span>

          <motion.h1
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.05, ease: [0.16, 1, 0.3, 1] }}
            className="mx-auto mt-6 max-w-3xl text-4xl font-bold leading-[1.15] tracking-tight sm:text-5xl"
          >
            Учись программировать
            <br />
            по одному чёткому пути
          </motion.h1>

          <motion.p
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
            className="mx-auto mt-6 max-w-xl text-lg leading-[1.7] text-muted"
          >
            Никакого хаоса из источников. Один структурированный курс, AI-ассистент,
            практика и тесты после каждой темы.
          </motion.p>

          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
            className="mx-auto mt-6 flex flex-wrap justify-center gap-2 text-xs font-medium text-muted"
          >
            {["Бесплатно начать", "AI-наставник 24/7", "Тест после каждой темы"].map((badge) => (
              <span
                key={badge}
                className="rounded-full border border-border bg-surface px-3 py-1.5"
              >
                {badge}
              </span>
            ))}
          </motion.div>

          <motion.div
            initial={reduce ? false : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="mt-8 flex flex-wrap justify-center gap-3"
          >
            {!token ? (
              <>
                <Link
                  href="/register"
                  className="rounded-xl border border-foreground/80 px-6 py-3 text-base font-semibold transition-all hover:-translate-y-0.5 hover:border-accent hover:text-accent"
                >
                  Начать обучение
                </Link>
                <Link
                  href="#courses"
                  className="rounded-xl border border-border px-6 py-3 text-base font-semibold transition-all hover:-translate-y-0.5 hover:border-accent/40"
                >
                  Посмотреть курсы
                </Link>
              </>
            ) : (
              <Link
                href="/dashboard"
                className="group flex items-center gap-2 rounded-xl border border-foreground/80 px-6 py-3 text-base font-semibold transition-all hover:-translate-y-0.5 hover:border-accent hover:text-accent"
              >
                Продолжить обучение
                <ArrowRight size={18} className="transition-transform group-hover:translate-x-0.5" />
              </Link>
            )}
          </motion.div>

          <motion.a
            href="#courses"
            initial={reduce ? false : { opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.35 }}
            className="mx-auto mt-14 flex h-9 w-9 items-center justify-center rounded-full border border-border text-muted transition-colors hover:border-accent/40 hover:text-accent"
            aria-label="Прокрутить к курсам"
          >
            <ArrowDown size={16} />
          </motion.a>
        </section>

        <HowItWorks />

        <section id="courses" className="mx-auto max-w-4xl px-6 pb-24">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-xl font-semibold">Выбери направление</h2>
            <Link
              href="#directions"
              className="flex items-center gap-1 text-sm font-medium text-accent hover:underline"
            >
              Все курсы <ArrowRight size={14} />
            </Link>
          </div>

          {error && <p className="text-center text-danger">{error}</p>}

          {!courses && !error && (
            <div className="flex justify-center py-10">
              <Loader2 className="animate-spin text-muted" />
            </div>
          )}

          <div className="grid gap-4 sm:grid-cols-2">
            {courses?.map((course, i) => {
              const meta = DIRECTION_META[course.slug] ?? { icon: course.icon ?? "📘", level: "Начинающий" };
              return (
                <motion.div
                  key={course.id}
                  initial={reduce ? false : { opacity: 0, y: 16 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.3 }}
                  transition={{ delay: i * 0.08, duration: 0.5 }}
                >
                  <Link href={`/courses/${course.slug}`}>
                    <Card hover className="group flex h-full flex-col gap-3 p-5">
                      <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-accent/10 text-xl">
                        {meta.icon}
                      </div>
                      <h3 className="font-semibold">{course.title}</h3>
                      <p className="text-sm leading-relaxed text-muted">{course.description}</p>
                      <div className="mt-auto flex items-center gap-2 pt-1">
                        {course.stacksTotal !== null && (
                          <span className="rounded-full border border-border px-2.5 py-1 text-xs font-medium text-muted">
                            {course.stacksTotal} стеков
                          </span>
                        )}
                        <span className="rounded-full border border-border px-2.5 py-1 text-xs font-medium text-muted">
                          {meta.level}
                        </span>
                      </div>
                    </Card>
                  </Link>
                  {user?.experienced && (
                    <Link
                      href={`/placement/${course.slug}`}
                      className="mt-2 flex items-center justify-center gap-1.5 rounded-full border border-border px-3 py-2 text-xs font-medium text-muted transition-colors hover:border-accent/40 hover:text-accent"
                    >
                      Пройти вступительный тест по этому направлению
                    </Link>
                  )}
                </motion.div>
              );
            })}
          </div>
        </section>

        <div id="directions">
          <ItDirections />
        </div>
        {token && <CareerQuizBanner />}

      </main>
      <Footer />
      {token && <AssistantWidget />}
    </>
  );
}
