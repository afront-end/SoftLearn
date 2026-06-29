"use client";

import { motion, useReducedMotion } from "framer-motion";

interface ProgressBarProps {
  value: number;
  total: number;
  colorClassName?: string;
}

export function ProgressBar({ value, total, colorClassName = "bg-accent" }: ProgressBarProps) {
  const reduce = useReducedMotion();
  const pct = total > 0 ? Math.round((value / total) * 100) : 0;

  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface-2">
      <motion.div
        initial={reduce ? false : { width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
        className={`h-full rounded-full ${colorClassName}`}
      />
    </div>
  );
}
