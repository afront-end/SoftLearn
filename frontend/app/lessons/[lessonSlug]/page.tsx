"use client";

import "katex/dist/katex.min.css";
import "highlight.js/styles/github-dark.css";

import { motion } from "framer-motion";
import { ArrowLeft, CheckCircle2, Loader2 } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

import { AiChat } from "@/components/lesson/ai-chat";
import { Navbar } from "@/components/navbar";
import { api, ApiError, LessonDetail } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function LessonPage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const router = useRouter();
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
        <p className="mt-6 text-center text-red-500">{error}</p>
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
        <Link
          href={`/stacks/${lesson.stack_slug}`}
          className="mb-4 inline-flex items-center gap-1.5 text-sm text-muted hover:text-foreground"
        >
          <ArrowLeft size={14} /> {lesson.stack_title}
        </Link>

        <div className="grid min-w-0 gap-6 lg:grid-cols-[1fr_380px]">
          <motion.article
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card lesson-content min-w-0 rounded-2xl p-6 prose prose-sm max-w-none dark:prose-invert sm:p-8"
          >
            <h1 className="!mt-0 gradient-text text-2xl font-bold">{lesson.title}</h1>
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeKatex, rehypeHighlight]}
            >
              {lesson.content ?? ""}
            </ReactMarkdown>

            <div className="mt-8 flex items-center justify-between border-t border-card-border pt-6">
              {lesson.lesson_read ? (
                <button
                  onClick={() => router.push(`/lessons/${lessonSlug}/practice`)}
                  className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-2 text-sm font-medium text-white"
                >
                  <CheckCircle2 size={14} /> К практике
                </button>
              ) : (
                <button
                  onClick={handleMarkRead}
                  disabled={marking}
                  className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary-2 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
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
          </motion.article>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
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
