import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}

export function Card({ children, className = "", hover = false }: CardProps) {
  return (
    <div
      className={`panel panel-shadow rounded-2xl ${hover ? "panel-shadow-hover" : ""} ${className}`}
    >
      {children}
    </div>
  );
}
