"use client";

import "katex/dist/katex.min.css";
import "highlight.js/styles/github-dark.css";

import { motion, useReducedMotion } from "framer-motion";
import { ArrowRight, CheckCircle2, Circle, Loader2, Lock } from "lucide-react";
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
import { Breadcrumb } from "@/components/ui/breadcrumb";
import { Card } from "@/components/ui/card";
import { api, ApiError, LessonDetail, LessonWithProgress } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

function extractYoutubeId(url: string): string | null {
  try {
    const u = new URL(url);
    if (u.hostname === "youtu.be") return u.pathname.slice(1);
    return u.searchParams.get("v");
  } catch {
    return null;
  }
}

function YoutubeEmbed({ url }: { url: string }) {
  const videoId = extractYoutubeId(url);
  if (!videoId) return null;
  return (
    <div className="not-prose mb-6 overflow-hidden rounded-xl border border-border bg-black">
      <div className="relative w-full" style={{ paddingBottom: "56.25%" }}>
        <iframe
          className="absolute inset-0 h-full w-full"
          src={`https://www.youtube.com/embed/${videoId}?rel=0`}
          title="Видео к уроку"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>
    </div>
  );
}

export default function LessonPage() {
  const { lessonSlug } = useParams<{ lessonSlug: string }>();
  const router = useRouter();
  const reduce = useReducedMotion();
  const token = useAuthStore((s) => s.token);
  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [outline, setOutline] = useState<LessonWithProgress[] | null>(null);
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

  useEffect(() => {
    if (!lesson || !token) return;
    api
      .getStackLessons(lesson.stack_slug)
      .then((data) => setOutline(data.lessons))
      .catch(() => undefined);
  }, [lesson, token]);

  const lessonIndex = outline?.findIndex((l) => l.slug === lessonSlug) ?? -1;
  const nextLesson = lessonIndex >= 0 ? outline?.[lessonIndex + 1] : undefined;

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
        <div className="flex flex-wrap items-center justify-between gap-3">
          <Breadcrumb
            items={[
              { label: "Главная", href: "/" },
              { label: lesson.stack_title, href: `/stacks/${lesson.stack_slug}` },
              { label: lesson.title },
            ]}
          />
          {outline && lessonIndex >= 0 && (
            <div className="flex items-center gap-3 text-sm">
              <span className="text-muted">
                Урок {lessonIndex + 1} из {outline.length}
              </span>
              {nextLesson && (
                <Link
                  href={`/lessons/${nextLesson.slug}`}
                  className="flex items-center gap-1 rounded-full border border-border px-3 py-1.5 font-medium transition-colors hover:border-accent/40 hover:text-accent"
                >
                  Далее <ArrowRight size={14} />
                </Link>
              )}
            </div>
          )}
        </div>

        <div className="mt-4 grid min-w-0 gap-6 lg:grid-cols-[1fr_380px]">
          <motion.div
            initial={reduce ? false : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="min-w-0"
          >
            <Card className="p-6 sm:p-8">
              <article className="lesson-content prose prose-base max-w-none dark:prose-invert">
                <h1 className="!mt-0 text-3xl font-bold tracking-tight">{lesson.title}</h1>

                {lesson.youtube_url && <YoutubeEmbed url={lesson.youtube_url} />}

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
            className="flex min-w-0 flex-col gap-4 lg:sticky lg:top-20"
          >
            <div className="h-[440px]">
              <AiChat lessonSlug={lessonSlug} />
            </div>

            {outline && outline.length > 0 && (
              <Card className="p-4">
                <h3 className="mb-3 text-sm font-semibold text-muted">Содержание урока</h3>
                <ul className="space-y-1">
                  {outline.map((l) => {
                    const isCurrent = l.slug === lessonSlug;
                    const Icon = l.status === "completed" ? CheckCircle2 : l.status === "locked" ? Lock : Circle;
                    return (
                      <li key={l.slug}>
                        {l.status === "locked" ? (
                          <span className="flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm text-muted/50">
                            <Icon size={15} />
                            {l.title}
                          </span>
                        ) : (
                          <Link
                            href={`/lessons/${l.slug}`}
                            className={`flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm transition-colors ${
                              isCurrent ? "bg-accent/10 font-medium text-accent" : "text-muted hover:text-foreground"
                            }`}
                          >
                            <Icon size={15} className={l.status === "completed" ? "text-accent" : undefined} />
                            {l.title}
                          </Link>
                        )}
                      </li>
                    );
                  })}
                </ul>
              </Card>
            )}
          </motion.div>
        </div>
      </main>
    </>
  );
}
