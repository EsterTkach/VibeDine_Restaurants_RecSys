import type { ReactNode } from "react";
import "./AppShell.css";

interface AppShellProps {
  children: ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell">
      <div className="phone-frame">
        {children}
      </div>
    </div>
  );
}