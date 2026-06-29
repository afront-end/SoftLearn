"use client";

import { motion, useReducedMotion } from "framer-motion";

interface Token {
  text: string;
  cls: string;
}

interface CodeLine {
  tokens: Token[];
}

const SNIPPET: CodeLine[] = [
  { tokens: [{ text: "const", cls: "text-ai" }, { text: " path = ", cls: "text-foreground" }, { text: "buildPath", cls: "text-accent" }, { text: "(student);", cls: "text-foreground" }] },
  { tokens: [{ text: "function", cls: "text-ai" }, { text: " ", cls: "" }, { text: "nextLesson", cls: "text-accent" }, { text: "(stack) {", cls: "text-foreground" }] },
  { tokens: [{ text: "  if", cls: "text-ai" }, { text: " (stack.", cls: "text-foreground" }, { text: "isLocked", cls: "text-accent" }, { text: ") return null;", cls: "text-foreground" }] },
  { tokens: [{ text: "  return", cls: "text-ai" }, { text: " stack.", cls: "text-foreground" }, { text: "lessons", cls: "text-accent" }, { text: "[0];", cls: "text-foreground" }] },
  { tokens: [{ text: "}", cls: "text-foreground" }] },
  { tokens: [{ text: "// один путь, без хаоса", cls: "text-muted" }] },
  { tokens: [{ text: "test", cls: "text-ai" }, { text: "(", cls: "text-foreground" }, { text: "\"barrier passed\"", cls: "text-success" }, { text: ", () => {", cls: "text-foreground" }] },
  { tokens: [{ text: "  expect", cls: "text-accent" }, { text: "(score).", cls: "text-foreground" }, { text: "toBeGreaterThan", cls: "text-accent" }, { text: "(70);", cls: "text-foreground" }] },
  { tokens: [{ text: "});", cls: "text-foreground" }] },
];

export function HeroCodeBackdrop() {
  const reduce = useReducedMotion();

  return (
    <div className="dot-grid pointer-events-none absolute inset-0 -z-10" aria-hidden="true">
      <motion.div
        initial={reduce ? false : { opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="code-window absolute -right-16 top-12 hidden w-[420px] -rotate-2 opacity-[0.18] lg:block"
      >
        <div className="code-window-titlebar">
          <span className="code-dot" style={{ background: "var(--danger)" }} />
          <span className="code-dot" style={{ background: "var(--warning)" }} />
          <span className="code-dot" style={{ background: "var(--success)" }} />
          <span className="ml-2 font-mono text-[11px] text-muted">path.ts</span>
        </div>
        <pre className="px-4 py-4 font-mono text-[12px] leading-relaxed">
          {SNIPPET.map((line, i) => (
            <div key={i}>
              {line.tokens.map((t, j) => (
                <span key={j} className={t.cls}>
                  {t.text}
                </span>
              ))}
            </div>
          ))}
        </pre>
      </motion.div>
    </div>
  );
}
