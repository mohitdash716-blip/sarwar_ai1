"use client";

import { motion } from "framer-motion";
import { 
  MessageSquare, 
  FileText, 
  Mail, 
  PenTool, 
  Sparkles, 
  LayoutDashboard,
  Settings,
  ChevronLeft,
  PlusCircle
} from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { cn } from "@/lib/utils";

const sidebarItems = [
  { icon: MessageSquare, label: "Chat", href: "/dashboard/chat" },
  { icon: FileText, label: "Summarizer", href: "/dashboard/summarizer" },
  { icon: Mail, label: "Email Generator", href: "/dashboard/email" },
  { icon: PenTool, label: "Rewriter", href: "/dashboard/rewriter" },
  { icon: Sparkles, label: "Content Gen", href: "/dashboard/content" },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className="flex h-screen bg-[#fbfbfd]">
      {/* Sidebar */}
      <motion.aside 
        initial={false}
        animate={{ width: isCollapsed ? 80 : 260 }}
        className="h-full glass border-r border-black/[0.05] flex flex-col relative z-20"
      >
        <div className="p-6 flex items-center justify-between">
          {!isCollapsed && (
            <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <Sparkles className="text-primary w-5 h-5" />
              <span className="font-semibold text-lg tracking-tight">Sarwar AI</span>
            </Link>
          )}
          <button 
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="p-1.5 rounded-lg hover:bg-black/[0.03] text-[#86868b] transition-colors"
          >
            <ChevronLeft className={cn("w-5 h-5 transition-transform", isCollapsed && "rotate-180")} />
          </button>
        </div>

        <div className="px-4 py-2">
          <button className={cn(
            "w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white border border-black/[0.05] shadow-sm hover:shadow-md transition-all group",
            isCollapsed && "justify-center"
          )}>
            <PlusCircle className="w-5 h-5 text-primary group-hover:scale-110 transition-transform" />
            {!isCollapsed && <span className="font-medium text-sm">New Chat</span>}
          </button>
        </div>

        <nav className="flex-1 px-4 py-6 flex flex-col gap-1">
          {sidebarItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link key={item.href} href={item.href}>
                <span className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 group",
                  isActive 
                    ? "bg-primary/5 text-primary font-semibold" 
                    : "text-[#86868b] hover:bg-black/[0.03] hover:text-[#1d1d1f]",
                  isCollapsed && "justify-center"
                )}>
                  <item.icon className={cn("w-5 h-5", isActive ? "text-primary" : "text-[#86868b] group-hover:text-[#1d1d1f]")} strokeWidth={isActive ? 2 : 1.5} />
                  {!isCollapsed && <span className="text-sm">{item.label}</span>}
                </span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-black/[0.05]">
          <Link href="/dashboard/settings">
            <span className={cn(
              "flex items-center gap-3 px-3 py-2.5 rounded-xl text-[#86868b] hover:bg-black/[0.03] transition-all",
              isCollapsed && "justify-center"
            )}>
              <Settings className="w-5 h-5" strokeWidth={1.5} />
              {!isCollapsed && <span className="text-sm font-medium">Settings</span>}
            </span>
          </Link>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 h-full overflow-hidden flex flex-col">
        {children}
      </main>
    </div>
  );
}
