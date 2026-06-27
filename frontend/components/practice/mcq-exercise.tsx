"use client";

import { motion } from "framer-motion";

interface Props {
  options: string[];
  selected: string | null;
  disabled: boolean;
  onSelect: (option: string) => void;
}

export function McqExercise({ options, selected, disabled, onSelect }: Props) {
  return (
    <div className="space-y-2">
      {options.map((option) => (
        <motion.button
          key={option}
          type="button"
          disabled={disabled}
          onClick={() => onSelect(option)}
          whileTap={{ scale: 0.98 }}
          className={`w-full rounded-xl border px-4 py-3 text-left text-sm transition-colors ${
            selected === option
              ? "border-primary bg-primary/10"
              : "border-card-border hover:border-primary/40"
          } disabled:opacity-70`}
        >
          {option}
        </motion.button>
      ))}
    </div>
  );
}
