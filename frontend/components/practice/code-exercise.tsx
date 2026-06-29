"use client";

import { javascript } from "@codemirror/lang-javascript";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import CodeMirror from "@uiw/react-codemirror";
import { useTheme } from "next-themes";

interface Props {
  value: string;
  disabled: boolean;
  onChange: (value: string) => void;
  language?: "javascript" | "python";
}

export function CodeExercise({ value, disabled, onChange, language = "javascript" }: Props) {
  const { resolvedTheme } = useTheme();
  const extensions = [language === "python" ? python() : javascript({ jsx: true })];

  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <div className="flex items-center gap-2 border-b border-border bg-surface-2 px-3 py-1.5">
        <span className="code-dot h-2 w-2" style={{ background: "var(--danger)" }} />
        <span className="code-dot h-2 w-2" style={{ background: "var(--warning)" }} />
        <span className="code-dot h-2 w-2" style={{ background: "var(--success)" }} />
        <span className="ml-1 font-mono text-[10px] text-muted">
          solution.{language === "python" ? "py" : "js"}
        </span>
      </div>
      <CodeMirror
        value={value}
        height="180px"
        theme={resolvedTheme === "dark" ? oneDark : "light"}
        extensions={extensions}
        editable={!disabled}
        onChange={onChange}
        basicSetup={{ lineNumbers: true, foldGutter: false }}
      />
    </div>
  );
}
