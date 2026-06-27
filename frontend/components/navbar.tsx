"use client";

import { LayoutDashboard, LogOut, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { ThemeToggle } from "@/components/theme-toggle";
import { useAuthStore } from "@/store/auth";

export function Navbar() {
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const clearAuth = useAuthStore((s) => s.clearAuth);

  function handleLogout() {
    clearAuth();
    router.push("/login");
  }

  return (
    <header className="sticky top-0 z-20 border-b border-card-border bg-background/70 backdrop-blur-md">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3 sm:px-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-primary-2">
            <Sparkles size={16} className="text-white" />
          </div>
          <span className="hidden font-semibold sm:inline">SoftLearn</span>
        </Link>

        <div className="flex items-center gap-2 sm:gap-3">
          {user && (
            <Link
              href="/dashboard"
              className="flex h-9 w-9 items-center justify-center rounded-full border border-card-border text-muted transition-colors hover:text-foreground sm:h-auto sm:w-auto sm:gap-1.5 sm:px-3 sm:py-1.5"
              aria-label="Личный кабинет"
            >
              <LayoutDashboard size={14} />
              <span className="hidden text-sm sm:inline">Кабинет</span>
            </Link>
          )}
          <ThemeToggle />
          {user ? (
            <button
              onClick={handleLogout}
              className="flex h-9 w-9 items-center justify-center rounded-full border border-card-border text-muted transition-colors hover:text-foreground sm:h-auto sm:w-auto sm:gap-1.5 sm:px-3 sm:py-1.5"
              aria-label="Выйти"
            >
              <LogOut size={14} />
              <span className="hidden text-sm sm:inline">Выйти</span>
            </button>
          ) : (
            <Link
              href="/login"
              className="rounded-full bg-gradient-to-r from-primary to-primary-2 px-4 py-1.5 text-sm font-medium text-white"
            >
              Войти
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
