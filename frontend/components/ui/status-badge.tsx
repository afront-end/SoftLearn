import { CheckCircle2, Lock, PlayCircle } from "lucide-react";

export type ProgressStatus = "locked" | "in_progress" | "completed";

const CONFIG: Record<ProgressStatus, { icon: typeof Lock; label: string; className: string }> = {
  locked: {
    icon: Lock,
    label: "locked",
    className: "text-muted border-border bg-surface-2",
  },
  in_progress: {
    icon: PlayCircle,
    label: "in_progress",
    className: "text-accent border-accent/30 bg-accent/10",
  },
  completed: {
    icon: CheckCircle2,
    label: "done",
    className: "text-success border-success/30 bg-success/10",
  },
};

export function StatusBadge({ status }: { status: ProgressStatus }) {
  const { icon: Icon, label, className } = CONFIG[status];
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-md border px-2 py-0.5 font-mono text-[11px] ${className}`}
    >
      <Icon size={12} />
      {label}
    </span>
  );
}
