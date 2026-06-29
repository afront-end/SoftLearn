import Link from "next/link";

import { Logo } from "@/components/ui/logo";

const LINKS = [
  { href: "/#courses", label: "Курсы" },
  { href: "/#directions", label: "Направления в IT" },
  { href: "/#community", label: "Сообщество" },
];

export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-6 px-6 py-10 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex flex-col items-center gap-2 sm:items-start">
          <Logo />
          <p className="max-w-xs text-center text-sm leading-relaxed text-muted sm:text-left">
            Один чёткий путь для самоучек-программистов: курсы, практика и AI-наставник.
          </p>
        </div>

        <nav className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm font-medium text-muted">
          {LINKS.map((link) => (
            <Link key={link.href} href={link.href} className="transition-colors hover:text-foreground">
              {link.label}
            </Link>
          ))}
        </nav>
      </div>

      <div className="border-t border-border py-5 text-center text-xs text-muted">
        © {new Date().getFullYear()} SoftLearn. Начать учиться — бесплатно.
      </div>
    </footer>
  );
}
