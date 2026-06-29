"use client";

import "katex/dist/katex.min.css";
import "highlight.js/styles/github-dark.css";

import { motion, useReducedMotion } from "framer-motion";
import { CheckCircle2, Loader2 } from "lucide-react";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

import { AiChat } from "@/components/lesson/ai-chat";
import { Navbar } from "@/components/navbar";
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
import { api, ApiError, LessonDetail } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function LessonPage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const router = useRouter();
  const reduce = useReducedMotion();
  const token = useAuthStore((s) => s.token);
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [marking, setMarking] = useState(false);

  useEffect(() => {
    if (!token) {
      setError("Войдите, чтобы открыть урок");
      return;
    }
    setError(null);
    api
      .getLesson(lessonSlug)
      .then(setLesson)
      .catch((err) =>
        setError(err instanceof ApiError ? err.message : "Не удалось загрузить урок")
      );
  }, [lessonSlug, token]);

  async function handleMarkRead() {
    setMarking(true);
    try {
      const updated = await api.markLessonRead(lessonSlug);
      setLesson(updated);
    } catch {
      // ignore
    } finally {
      setMarking(false);
    }
  }

  if (error) {
    return (
      <main className="p-6">
        <Navbar />
        <p className="mt-6 text-center text-danger">{error}</p>
      </main>
    );
  }

  if (!lesson) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <Loader2 className="animate-spin text-muted" />
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto w-full max-w-6xl min-w-0 flex-1 px-4 py-8 sm:px-6">
        <Breadcrumb
          items={[
            { label: "Главная", href: "/" },
            { label: lesson.stack_title, href: `/stacks/${lesson.stack_slug}` },
            { label: lesson.title },
          ]}
        />

        <div className="mt-4 grid min-w-0 gap-6 lg:grid-cols-[1fr_380px]">
          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="min-w-0"
          >
            <Card className="p-6 sm:p-8">
              <article className="lesson-content prose prose-base max-w-none dark:prose-invert">
                <h1 className="!mt-0 text-3xl font-bold tracking-tight">{lesson.title}</h1>
                <ReactMarkdown
                  remarkPlugins={[remarkGfm, remarkMath]}
                  rehypePlugins={[rehypeKatex, rehypeHighlight]}
                >
                  {lesson.content ?? ""}
                </ReactMarkdown>
              </article>

              <div className="mt-8 flex flex-wrap items-center justify-between gap-3 border-t border-border pt-6">
                {lesson.lesson_read ? (
                  <button
                    onClick={() => router.push(`/lessons/${lessonSlug}/practice`)}
                    className="flex items-center gap-2 rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md"
                  >
                    <CheckCircle2 size={14} /> К практике
                  </button>
                ) : (
                  <button
                    onClick={handleMarkRead}
                    disabled={marking}
                    className="flex items-center gap-2 rounded-full bg-accent px-5 py-2.5 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md disabled:opacity-50"
                  >
                    {marking ? <Loader2 size={14} className="animate-spin" /> : <CheckCircle2 size={14} />}
                    Отметить как прочитанное
                  </button>
                )}
                <button
                  onClick={() => router.push(`/stacks/${lesson.stack_slug}`)}
                  className="text-sm text-muted hover:text-foreground"
                >
                  К списку уроков →
                </button>
              </div>
            </Card>
          </motion.div>

          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="h-[70vh] min-w-0 lg:sticky lg:top-20 lg:h-[calc(100vh-6rem)]"
          >
            <AiChat lessonSlug={lessonSlug} />
          </motion.div>
        </div>
      </main>
    </>
  );
}
