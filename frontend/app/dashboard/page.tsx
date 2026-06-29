"use client";

import { motion, useReducedMotion } from "framer-motion";
import {
  Award,
  BarChart3,
  LayoutGrid,
  Loader2,
  type LucideIcon,
  Settings,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { Navbar } from "@/components/navbar";
import { ProgressBar } from "@/components/ui/progress-bar";
import { api, ApiError, ProgressOverviewOut } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

interface SidebarItem {
  label: string;
  icon: LucideIcon;
  href?: string;
}

const SIDEBAR_ITEMS: SidebarItem[] = [
  { label: "Дашборд", icon: LayoutGrid, href: "/dashboard" },
  { label: "Мои курсы", icon: Sparkles, href: "/#courses" },
  { label: "Прогресс", icon: BarChart3, href: "/dashboard" },
  { label: "Сертификаты", icon: Award },
  { label: "Настройки", icon: Settings },
];

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const token = useAuthStore((s) => s.token);
  const reduce = useReducedMotion();
  const [overview, setOverview] = useState<ProgressOverviewOut | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError("Войдите, чтобы увидеть свой прогресс");
      return;
    }
    setError(null);
    api
      .getProgressOverview()
      .then(setOverview)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Не удалось загрузить прогресс"));
  }, [token]);

  if (error) {
    return (
      <>
        <Navbar />
        <p className="mt-6 text-center text-danger">{error}</p>
      </>
    );
  }

  if (!overview) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Loader2 className="animate-spin text-muted" />
      </div>
    );
  }

  const totalStacks = overview.courses.reduce((sum, c) => sum + c.stacks_total, 0);
  const totalLessons = overview.courses.reduce((sum, c) => sum + c.lessons_total, 0);
  const initial = user?.name?.[0]?.toUpperCase() ?? "?";

  return (
    <>
      <Navbar />
      <main className="mx-auto flex w-full max-w-5xl flex-1 gap-6 px-4 py-8 sm:px-6 sm:py-10">
        <aside className="hidden w-56 shrink-0 md:block">
          <nav className="panel sticky top-24 space-y-1 rounded-2xl p-2">
            {SIDEBAR_ITEMS.map((item) => {
              const clickable = Boolean(item.href);
              const className = `flex items-center gap-2.5 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors ${
                item.label === "Дашборд"
                  ? "bg-accent/10 text-accent"
                  : clickable
                    ? "text-muted hover:bg-surface-2 hover:text-foreground"
                    : "text-muted/50"
              }`;
              return clickable ? (
                <Link key={item.label} href={item.href!} className={className}>
                  <item.icon size={16} />
                  {item.label}
                </Link>
              ) : (
                <span key={item.label} className={className}>
                  <item.icon size={16} />
                  {item.label}
                </span>
              );
            })}
          </nav>
        </aside>

        <div className="min-w-0 flex-1">
          <div className="mb-6 flex items-center justify-between">
            <span className="text-sm text-muted">Личный кабинет</span>
            <div className="flex items-center gap-2.5">
              <span className="text-sm font-medium">{user?.name}</span>
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-accent text-sm font-semibold text-accent-foreground">
                {initial}
              </span>
            </div>
          </div>

          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="panel-2 rounded-2xl p-5"
          >
            <p className="font-medium">
              {user ? `Привет, ${user.name}! 👋` : "Привет!"}
            </p>
            <p className="mt-1 text-sm text-muted">Продолжай в том же духе!</p>
          </motion.div>

          <div className="mt-4 grid grid-cols-3 gap-3">
            {[
              { label: "Уроков пройдено", value: overview.lessons_completed_total },
              { label: "Стеков завершено", value: overview.stacks_completed_total },
              { label: "Направлений", value: overview.courses.length },
            ].map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={reduce ? false : { opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="panel rounded-xl p-4 text-center"
              >
                <p className="text-2xl font-bold">{stat.value}</p>
                <p className="mt-1 text-xs text-muted">{stat.label}</p>
              </motion.div>
            ))}
          </div>

          <div className="mt-8">
            <h2 className="mb-3 font-semibold">Активные курсы</h2>
            <div className="panel space-y-4 rounded-2xl p-5">
              {overview.courses.map((course) => (
                <Link key={course.course_id} href={`/courses/${course.course_slug}`} className="block">
                  <div className="mb-1.5 flex items-center justify-between text-sm">
                    <span className="font-medium">{course.course_title}</span>
                    <span className="text-muted">
                      {totalLessons > 0 ? Math.round((course.lessons_completed / Math.max(course.lessons_total, 1)) * 100) : 0}%
                    </span>
                  </div>
                  <ProgressBar value={course.lessons_completed} total={Math.max(course.lessons_total, 1)} colorClassName="bg-accent" />
                </Link>
              ))}
              {overview.courses.length === 0 && (
                <p className="text-sm text-muted">Пока нет активных курсов — выберите направление на главной.</p>
              )}
            </div>
          </div>

          <p className="mt-3 text-right text-xs text-muted">
            Всего стеков: {totalStacks} · уроков: {totalLessons}
          </p>
        </div>
      </main>
    </>
  );
}
