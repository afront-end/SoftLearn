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
    <div className="overflow-hidden rounded-xl border border-card-border">
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
