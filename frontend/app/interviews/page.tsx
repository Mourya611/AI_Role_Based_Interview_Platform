"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { FileText, ArrowRight, Loader2, Award, Calendar } from "lucide-react";
import { listInterviews } from "@/lib/api";

export default function MyInterviewsPage() {
  const [interviews, setInterviews] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadInterviews() {
      try {
        setIsLoading(true);
        const data = await listInterviews();
        setInterviews(data);
      } catch (err) {
        console.error("Failed to load interviews:", err);
      } finally {
        setIsLoading(false);
      }
    }
    loadInterviews();
  }, []);

  return (
    <div className="max-w-5xl mx-auto space-y-6 py-2">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">My Interviews</h1>
          <p className="text-slate-500 text-xs sm:text-sm">
            View your completed technical interview history and performance reports.
          </p>
        </div>

        <Link
          href="/new-interview"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-md shadow-indigo-200 transition-all text-center"
        >
          <span>Start New Interview</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {isLoading ? (
        <div className="flex flex-col items-center justify-center min-h-[300px] space-y-3">
          <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
          <p className="text-slate-500 text-xs font-medium">Fetching interview records...</p>
        </div>
      ) : interviews.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 border border-slate-100 shadow-sm text-center space-y-4">
          <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mx-auto">
            <FileText className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-bold text-slate-900">No interviews completed yet</h3>
            <p className="text-slate-500 text-xs max-w-sm mx-auto">
              Start your first role-based technical interview to get personalized AI feedback and scoring.
            </p>
          </div>
          <Link
            href="/new-interview"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 text-white font-semibold text-xs shadow-md shadow-indigo-200"
          >
            Start Interview
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden divide-y divide-slate-100">
          {interviews.map((session) => (
            <div key={session.id} className="p-5 flex items-center justify-between gap-4 hover:bg-slate-50/60 transition-colors">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold text-xs flex-shrink-0">
                  <Award className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">{session.target_role}</h3>
                  <div className="flex items-center gap-3 text-xs text-slate-400 mt-0.5">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      {new Date(session.started_at).toLocaleDateString()}
                    </span>
                    <span>•</span>
                    <span>{session.total_questions} Questions</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className="text-xs text-slate-400">Score</p>
                  <p className="text-sm font-bold text-emerald-600">
                    {session.score ? `${session.score}/10` : "N/A"}
                  </p>
                </div>

                <Link
                  href={`/interviews/${session.id}`}
                  className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition-colors"
                >
                  View Report
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
