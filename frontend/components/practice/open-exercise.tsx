"use client";

interface Props {
  value: string;
  disabled: boolean;
  onChange: (value: string) => void;
}

export function OpenExercise({ value, disabled, onChange }: Props) {
  return (
    <textarea
      value={value}
      disabled={disabled}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Напишите ответ своими словами..."
      rows={4}
      className="w-full rounded-xl border border-card-border bg-background/50 px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/30 disabled:opacity-70"
    />
  );
}
