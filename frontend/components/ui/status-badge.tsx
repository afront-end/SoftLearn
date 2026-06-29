import { CheckCircle2, Lock, PlayCircle } from "lucide-react";

export type ProgressStatus = "locked" | "in_progress" | "completed";

const CONFIG: Record<ProgressStatus, { icon: typeof Lock; label: string; className: string }> = {
  locked: {
    icon: Lock,
    label: "Заблокировано",
    className: "text-muted border-border bg-surface-2",
  },
  in_progress: {
    icon: PlayCircle,
    label: "В процессе",
    className: "text-accent border-accent/25 bg-accent/10",
  },
  completed: {
    icon: CheckCircle2,
    label: "Завершено",
    className: "text-success border-success/25 bg-success/10",
  },
};

export function StatusBadge({ status }: { status: ProgressStatus }) {
  const { icon: Icon, label, className } = CONFIG[status];
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${className}`}>
      <Icon size={13} />
      {label}
    </span>
  );
}
