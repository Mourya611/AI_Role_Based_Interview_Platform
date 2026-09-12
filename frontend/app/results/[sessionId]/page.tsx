"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { CheckCircle2, Lightbulb, Check, Loader2 } from "lucide-react";
import { getInterviewReport } from "@/lib/api";

export default function ResultsPage() {
  const params = useParams();
  const sessionId = params.sessionId as string;

  const [report, setReport] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadReport() {
      try {
        setIsLoading(true);
        const data = await getInterviewReport(sessionId);
        setReport(data);
      } catch (err) {
        console.error("Error loading report:", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadReport();
  }, [sessionId]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
        <p className="text-slate-500 text-sm font-medium">Generating performance summary report...</p>
      </div>
    );
  }

  const topics = report?.topics_covered || [
    "System Design",
    "Databases",
    "APIs",
    "Backend Development",
    "Problem Solving",
  ];

  const keyInsights = report?.key_insights || [
    "Good understanding of backend concepts.",
    "Strong knowledge of databases and API design.",
    "Consider improving depth in system design and scalability topics.",
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-2">
      {/* Header Container */}
      <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-emerald-500 text-white flex items-center justify-center flex-shrink-0 shadow-md shadow-emerald-200">
            <CheckCircle2 className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Interview Completed!</h1>
            <p className="text-slate-500 text-sm">Here&apos;s a summary of your interview session.</p>
          </div>
        </div>

        <Link
          href={`/interviews/${sessionId}`}
          className="px-5 py-2.5 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-semibold shadow-sm transition-colors text-center"
        >
          View Full Report
        </Link>
      </div>

      {/* Summary Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm space-y-1">
          <p className="text-xs text-slate-400 font-medium">Total Questions</p>
          <p className="text-2xl font-bold text-slate-900">{report?.total_questions || 5}</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm space-y-1">
          <p className="text-xs text-slate-400 font-medium">Time Taken</p>
          <p className="text-2xl font-bold text-slate-900">{report?.time_taken_mins || 18} mins</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm space-y-1">
          <p className="text-xs text-slate-400 font-medium">Role</p>
          <p className="text-lg font-bold text-slate-900 truncate">{report?.target_role || "Backend Engineer"}</p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-100 shadow-sm space-y-1">
          <p className="text-xs text-slate-400 font-medium">Overall Performance</p>
          <p className="text-2xl font-bold text-emerald-600">{report?.overall_performance || "Good"}</p>
        </div>
      </div>

      {/* Topics Covered */}
      <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
          Topics Covered
        </h3>
        <div className="flex flex-wrap gap-2.5">
          {topics.map((t: string) => (
            <span
              key={t}
              className="px-3.5 py-1.5 rounded-full bg-indigo-50 text-indigo-700 text-xs font-semibold"
            >
              {t}
            </span>
          ))}
        </div>
      </div>

      {/* Key Insights */}
      <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600">
            <Lightbulb className="w-4 h-4" />
          </div>
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
            Key Insights
          </h3>
        </div>

        <div className="space-y-3 pt-1">
          {keyInsights.map((insight: string, idx: number) => (
            <div key={idx} className="flex items-start gap-3 text-sm text-slate-700">
              <div className="w-5 h-5 rounded-full bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 flex-shrink-0 mt-0.5">
                <Check className="w-3.5 h-3.5" />
              </div>
              <span className="leading-normal">{insight}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
