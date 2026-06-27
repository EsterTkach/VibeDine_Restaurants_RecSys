import type { ReactNode } from "react";
import "./AppShell.css";

interface AppShellProps {
  children: ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell">
      <div className="phone-frame">
        <div className="w-full h-full overflow-y-auto pb-24 scrollbar-none flex flex-col">
          <main className="flex-1 w-full">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}