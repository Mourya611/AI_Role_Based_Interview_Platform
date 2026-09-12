import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";

export const metadata: Metadata = {
  title: "InterviewAI - Role-Based AI Technical Interview Platform",
  description: "AI-Powered Technical Candidate Screening & Technical Interview Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen bg-[#F8FAFC]">
        <Sidebar />
        <main className="flex-1 min-w-0 p-8 overflow-y-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
