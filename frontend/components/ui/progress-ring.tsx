"use client";

import { motion, useReducedMotion } from "framer-motion";

interface ProgressRingProps {
  value: number;
  total: number;
  size?: number;
  strokeWidth?: number;
  colorVar?: string;
}

export function ProgressRing({
  value,
  total,
  size = 88,
  strokeWidth = 7,
  colorVar = "var(--accent)",
}: ProgressRingProps) {
  const reduce = useReducedMotion();
  const pct = total > 0 ? Math.min(1, value / total) : 0;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="var(--border)"
          strokeWidth={strokeWidth}
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colorVar}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={reduce ? false : { strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: circumference * (1 - pct) }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
        />
      </svg>
      <span className="absolute font-mono text-sm font-semibold">{Math.round(pct * 100)}%</span>
    </div>
  );
}
