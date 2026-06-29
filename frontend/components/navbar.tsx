"use client";

import { LayoutDashboard, LogOut } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { Logo } from "@/components/ui/logo";
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
    <header className="sticky top-0 z-20 border-b border-border bg-background/85 backdrop-blur-md">
      <div className="mx-auto flex h-14 max-w-5xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center">
          <Logo />
        </Link>

        <div className="flex items-center gap-2 sm:gap-3">
          {user && (
            <Link
              href="/dashboard"
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-border text-muted transition-colors hover:border-accent/50 hover:text-accent sm:h-auto sm:w-auto sm:gap-1.5 sm:px-3 sm:py-1.5"
              aria-label="Личный кабинет"
            >
              <LayoutDashboard size={15} />
              <span className="hidden font-mono text-[13px] sm:inline">кабинет</span>
            </Link>
          )}
          <ThemeToggle />
          {user ? (
            <button
              onClick={handleLogout}
              className="flex h-9 w-9 items-center justify-center rounded-lg border border-border text-muted transition-colors hover:border-danger/50 hover:text-danger sm:h-auto sm:w-auto sm:gap-1.5 sm:px-3 sm:py-1.5"
              aria-label="Выйти"
            >
              <LogOut size={15} />
              <span className="hidden font-mono text-[13px] sm:inline">выйти</span>
            </button>
          ) : (
            <Link
              href="/login"
              className="rounded-lg bg-accent px-4 py-1.5 font-mono text-[13px] font-medium text-accent-foreground transition-opacity hover:opacity-90"
            >
              войти
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
