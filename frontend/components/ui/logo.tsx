import { GraduationCap } from "lucide-react";

interface LogoProps {
  showWordmark?: boolean;
  className?: string;
}

export function Logo({ showWordmark = true, className }: LogoProps) {
  return (
    <span className={`flex items-center gap-2 ${className ?? ""}`}>
      <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-accent text-accent-foreground">
        <GraduationCap size={19} strokeWidth={2.1} />
      </span>
      {showWordmark && <span className="text-[17px] font-bold tracking-tight">SoftLearn</span>}
    </span>
  );
}
