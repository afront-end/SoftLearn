"use client";

import { motion } from "framer-motion";
import { GraduationCap, Loader2, Rocket } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { ThemeToggle } from "@/components/theme-toggle";
import { Card } from "@/components/ui/card";
import { GradientBlob } from "@/components/ui/gradient-blob";
import { Logo } from "@/components/ui/logo";
import { api } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function OnboardingPage() {
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const setAuth = useAuthStore((s) => s.setAuth);
  const token = useAuthStore((s) => s.token);
  const [loading, setLoading] = useState<"yes" | "no" | null>(null);

  async function handleChoice(experienced: boolean) {
    setLoading(experienced ? "yes" : "no");
    try {
      const updated = await api.completeOnboarding(experienced);
      if (token) setAuth(token, updated);
      router.push("/");
    } finally {
      setLoading(null);
    }
  }

  return (
    <main className="relative flex flex-1 items-center justify-center overflow-hidden p-6">
      <GradientBlob />
      <div className="absolute right-6 top-6">
        <ThemeToggle />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className="w-full max-w-md"
      >
        <Card className="p-8 text-center">
          <div className="mx-auto w-fit">
            <Logo />
          </div>
          <h1 className="mt-5 text-2xl font-bold">{user ? `Привет, ${user.name}!` : "Привет!"}</h1>
          <p className="mt-2 text-muted">Вы уже умеете программировать?</p>

          <div className="mt-7 space-y-3">
            <motion.button
              whileTap={{ scale: 0.98 }}
              disabled={loading !== null}
              onClick={() => handleChoice(true)}
              className="flex w-full items-center justify-center gap-2 rounded-xl bg-accent px-4 py-3 text-sm font-semibold text-accent-foreground shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md disabled:opacity-60"
            >
              {loading === "yes" ? <Loader2 size={16} className="animate-spin" /> : <GraduationCap size={16} />}
              Да, пройти вступительный тест
            </motion.button>

            <motion.button
              whileTap={{ scale: 0.98 }}
              disabled={loading !== null}
              onClick={() => handleChoice(false)}
              className="flex w-full items-center justify-center gap-2 rounded-xl border border-border px-4 py-3 text-sm font-semibold transition-all hover:-translate-y-0.5 hover:border-accent/40 disabled:opacity-60"
            >
              {loading === "no" ? <Loader2 size={16} className="animate-spin" /> : <Rocket size={16} />}
              Нет, начну с самого начала
            </motion.button>
          </div>
        </Card>
      </motion.div>
    </main>
  );
}
