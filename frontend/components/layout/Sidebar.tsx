"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Home, 
  PlusCircle, 
  FileText, 
  User, 
  Settings, 
  Flame 
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Home", href: "/", icon: Home },
    { name: "New Interview", href: "/new-interview", icon: PlusCircle },
    { name: "My Interviews", href: "/interviews", icon: FileText },
    { name: "Profile", href: "/profile", icon: User },
    { name: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between h-screen sticky top-0 px-4 py-6 select-none z-20">
      <div>
        {/* Brand Logo Header */}
        <Link href="/" className="flex items-center gap-3 px-3 mb-8 group">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-200 group-hover:scale-105 transition-transform">
            <Flame className="w-6 h-6 fill-current" />
          </div>
          <span className="text-xl font-bold tracking-tight text-slate-900">
            Interview<span className="text-indigo-600">AI</span>
          </span>
        </Link>

        {/* Navigation Links */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? "bg-indigo-50 text-indigo-600 shadow-sm"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? "text-indigo-600" : "text-slate-400"}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Candidate Profile Pill */}
      <div className="pt-4 border-t border-slate-100 flex items-center gap-3 px-2">
        <div className="w-10 h-10 rounded-full bg-indigo-600 text-white font-semibold flex items-center justify-center text-base shadow-sm">
          M
        </div>
        <div className="flex flex-col min-w-0">
          <span className="text-sm font-semibold text-slate-800 truncate">Mourya Yarla</span>
          <span className="text-xs text-slate-400 truncate">mourya@example.com</span>
        </div>
      </div>
    </aside>
  );
}
