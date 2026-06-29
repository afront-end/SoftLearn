"use client";

import { AnimatePresence, motion } from "framer-motion";
import { Bot, Loader2, Send, Trash2, User } from "lucide-react";
import { useEffect, useRef, useState } from "react";

import { Card } from "@/components/ui/card";
import { api, ApiError, ChatMessageOut } from "@/lib/api";

interface Props {
  lessonSlug: string;
}

interface LocalMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export function AiChat({ lessonSlug }: Props) {
  const [messages, setMessages] = useState<LocalMessage[]>([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    api
      .getChatHistory(lessonSlug)
      .then((history: ChatMessageOut[]) =>
        setMessages(history.map((m) => ({ id: m.id, role: m.role, content: m.content })))
      )
      .catch(() => undefined);
  }, [lessonSlug]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || streaming) return;

    setError(null);
    setInput("");
    const userMsg: LocalMessage = { id: `u-${Date.now()}`, role: "user", content: text };
    const assistantId = `a-${Date.now()}`;
    setMessages((prev) => [...prev, userMsg, { id: assistantId, role: "assistant", content: "" }]);
    setStreaming(true);

    try {
      await api.streamChat(lessonSlug, text, (token) => {
        setMessages((prev) =>
          prev.map((m) => (m.id === assistantId ? { ...m, content: m.content + token } : m))
        );
      });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "AI-ассистент недоступен. Запущена ли Ollama?");
      setMessages((prev) => prev.filter((m) => m.id !== assistantId));
    } finally {
      setStreaming(false);
    }
  }

  async function handleClear() {
    await api.clearChatHistory(lessonSlug).catch(() => undefined);
    setMessages([]);
  }

  return (
    <Card className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-border px-4 py-3.5">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-accent/10 text-accent">
            <Bot size={15} />
          </div>
          <span className="text-sm font-semibold">AI-ассистент</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full border border-accent/30 bg-accent/10 px-2.5 py-1 text-xs font-medium text-accent">
            по теме урока
          </span>
          <button
            onClick={handleClear}
            className="text-muted transition-colors hover:text-danger"
            aria-label="Очистить историю"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto px-4 py-4">
        {messages.length === 0 && (
          <p className="text-sm leading-relaxed text-muted">
            Спросите что-нибудь про этот урок, отвечу только по теме.
          </p>
        )}
        <AnimatePresence initial={false}>
          {messages.map((m) => (
            <motion.div
              key={m.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-2 ${m.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {m.role === "assistant" && (
                <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-ai/10 text-ai">
                  <Bot size={13} />
                </div>
              )}
              <div
                className={`max-w-[80%] whitespace-pre-wrap rounded-2xl px-3.5 py-2 text-sm leading-relaxed ${
                  m.role === "user" ? "bg-accent text-accent-foreground" : "panel-2 text-foreground"
                }`}
              >
                {m.content || <Loader2 size={14} className="animate-spin text-muted" />}
              </div>
              {m.role === "user" && (
                <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-surface-2">
                  <User size={13} />
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {error && <p className="px-4 pb-2 text-xs text-danger">{error}</p>}

      <form onSubmit={handleSend} className="flex gap-2 border-t border-border p-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Спросите про урок..."
          disabled={streaming}
          className="flex-1 rounded-full border border-border bg-background px-4 py-2 text-sm outline-none focus:border-accent focus:ring-2 focus:ring-accent/20"
        />
        <button
          type="submit"
          disabled={streaming || !input.trim()}
          className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-accent text-accent-foreground disabled:opacity-50"
        >
          {streaming ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
        </button>
      </form>
    </Card>
  );
}
