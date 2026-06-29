"use client";

import { motion } from "framer-motion";
import { AlertCircle, ArrowRight, Eye, EyeOff, Lock, Mail } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useState } from "react";

import { GoogleButton } from "@/components/auth/google-button";
import { ThemeToggle } from "@/components/theme-toggle";
import { Logo } from "@/components/ui/logo";
import { api, ApiError } from "@/lib/api";
import { useAuthStore } from "@/store/auth";

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function finishAuth(access_token: string) {
    useAuthStore.setState({ token: access_token });
    const user = await api.me();
    setAuth(access_token, user);
    router.push("/");
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { access_token } = await api.login({ email, password });
      await finishAuth(access_token);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Не удалось войти");
    } finally {
      setLoading(false);
    }
  }

  const handleGoogleCredential = useCallback(async (idToken: string) => {
    setError(null);
    try {
      const { access_token } = await api.googleLogin(idToken);
      await finishAuth(access_token);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Не удалось войти через Google");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="dot-grid relative flex flex-1 items-center justify-center overflow-hidden p-6">
      <div className="absolute right-6 top-6">
        <ThemeToggle />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 24, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="code-window panel-shadow w-full max-w-sm"
      >
        <div className="code-window-titlebar justify-start">
          <span className="code-dot" style={{ background: "var(--danger)" }} />
          <span className="code-dot" style={{ background: "var(--warning)" }} />
          <span className="code-dot" style={{ background: "var(--success)" }} />
          <span className="ml-2 font-mono text-[11px] text-muted">login.ts</span>
        </div>

        <div className="p-8">
          <Logo />

          <h1 className="mt-6 text-2xl font-bold tracking-tight">С возвращением</h1>
          <p className="mt-1 text-sm text-muted">Войдите, чтобы продолжить обучение</p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">
            <div className="relative">
              <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
              <input
                type="email"
                placeholder="Email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full rounded-lg border border-border bg-background px-10 py-2.5 text-sm outline-none transition-colors focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
            </div>

            <div className="relative">
              <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Пароль"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full rounded-lg border border-border bg-background px-10 py-2.5 text-sm outline-none transition-colors focus:border-accent focus:ring-2 focus:ring-accent/25"
              />
              <button
                type="button"
                onClick={() => setShowPassword((v) => !v)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted hover:text-foreground"
                aria-label="Показать пароль"
              >
                {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>

            {error && (
              <motion.p
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                className="flex items-center gap-1.5 text-sm text-danger"
              >
                <AlertCircle size={14} /> {error}
              </motion.p>
            )}

            <motion.button
              type="submit"
              disabled={loading}
              whileTap={{ scale: 0.98 }}
              className="group flex w-full items-center justify-center gap-2 rounded-lg bg-accent px-3 py-2.5 text-sm font-medium text-accent-foreground transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {loading ? "Входим..." : "Войти"}
              {!loading && (
                <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              )}
            </motion.button>

            <p className="text-center text-sm text-muted">
              Нет аккаунта?{" "}
              <Link href="/register" className="font-medium text-accent hover:underline">
                Зарегистрироваться
              </Link>
            </p>
          </form>

          <div className="my-5 flex items-center gap-3">
            <div className="h-px flex-1 bg-border" />
            <span className="font-mono text-xs text-muted">или</span>
            <div className="h-px flex-1 bg-border" />
          </div>

          <GoogleButton onCredential={handleGoogleCredential} text="signin_with" />
        </div>
      </motion.div>
    </main>
  );
}
