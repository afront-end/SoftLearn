import { Terminal } from "lucide-react";

interface LogoProps {
  showWordmark?: boolean;
  className?: string;
}

export function Logo({ showWordmark = true, className }: LogoProps) {
  return (
    <span className={`flex items-center gap-2 ${className ?? ""}`}>
      <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent text-accent-foreground">
        <Terminal size={16} strokeWidth={2.25} />
      </span>
      {showWordmark && (
        <span className="font-mono text-[15px] font-semibold tracking-tight">
          soft<span className="text-accent">learn</span>
        </span>
      )}
    </span>
  );
}
