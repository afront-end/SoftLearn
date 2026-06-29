"use client";

import { motion, useReducedMotion } from "framer-motion";

export function GradientBlob({ className = "" }: { className?: string }) {
  const reduce = useReducedMotion();

  return (
    <div className={`pointer-events-none absolute inset-0 -z-10 overflow-hidden ${className}`} aria-hidden="true">
      <motion.div
        initial={reduce ? false : { opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1.1, ease: [0.16, 1, 0.3, 1] }}
        className="absolute -top-32 left-1/2 h-[460px] w-[680px] -translate-x-1/2 rounded-full blur-3xl"
        style={{
          background: "radial-gradient(circle, color-mix(in srgb, var(--accent) 22%, transparent), transparent 70%)",
        }}
      />
      <motion.div
        initial={reduce ? false : { opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1.1, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
        className="absolute -top-10 right-[8%] h-[320px] w-[420px] rounded-full blur-3xl"
        style={{
          background: "radial-gradient(circle, color-mix(in srgb, var(--ai) 18%, transparent), transparent 70%)",
        }}
      />
    </div>
  );
}
