import "@/styles/globals.css";
import { Toaster } from "sonner";
import Sidebar from "@/components/UI/Sidebar";

export const metadata = {
  title: "AI Brain Coder Agent",
  description: "AI-powered coding assistant with dynamic skill loading",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <main className="flex-1 overflow-y-auto bg-slate-50">
            {children}
          </main>
        </div>
        <Toaster position="bottom-right" />
      </body>
    </html>
  );
}
