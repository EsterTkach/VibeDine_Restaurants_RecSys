import type { ReactNode } from "react";
import PersonalizationToast from "../components/PersonalizationToast";
import "./AppShell.css";

interface AppShellProps {
  children: ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell">
      <div className="phone-frame">
        <div className="w-full h-full overflow-y-auto pb-12 scrollbar-none flex flex-col">
          <main className="flex-1 w-full">
            {children}
          </main>
        </div>
        <PersonalizationToast />
      </div>
    </div>
  );
}