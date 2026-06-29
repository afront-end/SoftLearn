interface LogoProps {
  className?: string;
}

export function Logo({ className }: LogoProps) {
  return (
    <span className={`text-[19px] font-bold tracking-tight ${className ?? ""}`}>
      <span className="text-foreground">Soft</span>
      <span className="text-accent">Learn</span>
    </span>
  );
}
