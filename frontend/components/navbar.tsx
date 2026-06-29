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
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center">
          <Logo />
        </Link>

        <nav className="hidden items-center gap-8 text-sm font-medium text-muted md:flex">
          <Link href="/#courses" className="transition-colors hover:text-foreground">
            Курсы
          </Link>
          <Link href="/#directions" className="transition-colors hover:text-foreground">
            О нас
          </Link>
          <Link href="/#community" className="transition-colors hover:text-foreground">
            Сообщество
          </Link>
          {user && (
            <Link href="/dashboard" className="transition-colors hover:text-foreground">
              Кабинет
            </Link>
          )}
        </nav>

        <div className="flex items-center gap-2 sm:gap-3">
          <ThemeToggle />
          {user ? (
            <>
              <Link
                href="/dashboard"
                className="flex h-9 w-9 items-center justify-center rounded-full border border-border text-muted transition-colors hover:border-accent/40 hover:text-accent md:hidden"
                aria-label="Личный кабинет"
              >
                <LayoutDashboard size={16} />
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1.5 rounded-full border border-border px-3.5 py-2 text-sm font-medium text-muted transition-colors hover:border-danger/40 hover:text-danger"
              >
                <LogOut size={15} />
                <span className="hidden sm:inline">Выйти</span>
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="hidden text-sm font-medium text-muted transition-colors hover:text-foreground sm:inline"
              >
                Войти
              </Link>
              <Link
                href="/register"
                className="rounded-full border border-border px-4 py-2 text-sm font-semibold transition-colors hover:border-accent/50 hover:text-accent"
              >
                Начать бесплатно
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
