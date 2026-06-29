"use client";

import { useReducedMotion } from "framer-motion";
import { useEffect, useState } from "react";

interface TypingHeadingProps {
  text: string;
  className?: string;
  speedMs?: number;
}

export function TypingHeading({ text, className, speedMs = 28 }: TypingHeadingProps) {
  const reduce = useReducedMotion();
  const [shown, setShown] = useState(reduce ? text.length : 0);

  useEffect(() => {
    if (reduce) return;
    setShown(0);
    let i = 0;
    const interval = setInterval(() => {
      i += 1;
      setShown(i);
      if (i >= text.length) clearInterval(interval);
    }, speedMs);
    return () => clearInterval(interval);
  }, [text, speedMs, reduce]);

  return (
    <span className={className}>
      {text.slice(0, shown)}
      <span className="caret">&nbsp;</span>
    </span>
  );
}
