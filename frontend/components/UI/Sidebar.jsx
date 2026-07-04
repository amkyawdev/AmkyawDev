"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MessageSquare, Database, FolderOpen, Settings, Brain, Code2 } from "lucide-react";
import clsx from "clsx";

const navItems = [
  { href: "/", label: "Chat", icon: MessageSquare },
  { href: "/knowledge", label: "Knowledge", icon: Database },
  { href: "/files", label: "Files", icon: FolderOpen },
  { href: "/settings", label: "Settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
      <div className="p-5 border-b border-slate-200">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-primary-600 rounded-lg flex items-center justify-center">
            <Brain className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-slate-900 text-sm">AmkyawDev</h1>
            <p className="text-xs text-slate-500">Tools v1.0</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href} className={clsx("sidebar-link", isActive && "active")}>
              <Icon className="w-5 h-5" /><span>{item.label}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-slate-200">
        <a href="https://amkyaw.dev" className="flex items-center gap-2 text-xs text-slate-500 hover:text-primary-600">
          <Code2 className="w-4 h-4" /><span>amkyaw.dev</span>
        </a>
      </div>
    </aside>
  );
}
