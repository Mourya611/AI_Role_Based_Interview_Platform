"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Download, ChevronDown, ChevronUp, Loader2, CheckCircle, AlertCircle } from "lucide-react";
import { getInterviewReport, getReportDownloadUrl } from "@/lib/api";

export default function DetailedFeedbackPage() {
  const params = useParams();
  const sessionId = params.sessionId as string;

  const [report, setReport] = useState<any>(null);
  const [openIndex, setOpenIndex] = useState<number | null>(0);
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

  const toggleAccordion = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const handleDownloadReport = () => {
    const downloadUrl = getReportDownloadUrl(sessionId);
    window.open(downloadUrl, "_blank");
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
        <p className="text-slate-500 text-sm font-medium">Loading detailed feedback...</p>
      </div>
    );
  }

  // Fallback items matching visual reference if no Q&A in session yet
  const questionsList = report?.questions_answers?.length > 0 ? report.questions_answers : [
    {
      question_number: 1,
      question_text: "Explain the difference between a monolithic and microservices architecture.",
      rating: "Good Answer",
      feedback: "You explained the key differences well and provided relevant use cases.",
      answer_text: "Monolithic architecture packages all features into a single application. Microservices split services into independent components communicating via APIs for better scalability.",
      strengths: ["Clear explanation of core concepts", "Identified API communication mechanism"],
      weaknesses: ["Could elaborate on operational complexity"]
    },
    {
      question_number: 2,
      question_text: "What is a database index? How does it work?",
      rating: "Excellent",
      feedback: "Clear and concise explanation with practical examples.",
      answer_text: "A database index is a data structure, typically a B-Tree, that improves the speed of data retrieval operations on a table at the cost of additional writes and storage.",
      strengths: ["Mentioned B-Tree data structure", "Highlighted write latency trade-off"],
      weaknesses: []
    },
    {
      question_number: 3,
      question_text: "Explain REST vs GraphQL.",
      rating: "Good Answer",
      feedback: "Good comparison. Try to include more real-world scenarios.",
      answer_text: "REST uses standard HTTP endpoints returning fixed data structures. GraphQL allows clients to request exact fields in a single query.",
      strengths: ["Differentiated endpoint vs query approach"],
      weaknesses: ["Add discussion on caching differences"]
    },
    {
      question_number: 4,
      question_text: "Design a URL shortener system.",
      rating: "Average",
      feedback: "You covered the basics. Consider discussing scalability and high availability.",
      answer_text: "Use a hash function to map long URLs to a 6-character string stored in a relational database with key-value caching.",
      strengths: ["Basic hashing concept identified"],
      weaknesses: ["Needs detail on rate limiting, database sharding, and high availability"]
    },
    {
      question_number: 5,
      question_text: "How would you optimize a slow database query?",
      rating: "Good Answer",
      feedback: "Good understanding of indexing and query optimization.",
      answer_text: "Analyze query execution plans using EXPLAIN ANALYZE, check for missing B-Tree indexes, avoid SELECT *, and rewrite inefficient joins.",
      strengths: ["Used EXPLAIN ANALYZE", "Recommended avoiding SELECT *"],
      weaknesses: ["Could mention connection pooling"]
    }
  ];

  const getRatingBadgeClass = (rating: string) => {
    switch (rating) {
      case "Excellent":
      case "Good Answer":
      case "Good":
        return "bg-emerald-100 text-emerald-800 border-emerald-200";
      case "Average":
        return "bg-amber-100 text-amber-800 border-amber-200";
      default:
        return "bg-rose-100 text-rose-800 border-rose-200";
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-2">
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Detailed Feedback</h1>
          <p className="text-slate-500 text-xs sm:text-sm">
            Review detailed AI evaluation and recommendations for each question.
          </p>
        </div>

        <button
          onClick={handleDownloadReport}
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl border border-slate-200 text-slate-700 hover:bg-slate-50 text-xs font-semibold shadow-sm transition-colors"
        >
          <Download className="w-4 h-4 text-slate-500" />
          <span>Download Report</span>
        </button>
      </div>

      {/* Accordion Questions List */}
      <div className="space-y-3">
        {questionsList.map((q: any, idx: number) => {
          const isOpen = openIndex === idx;
          return (
            <div
              key={idx}
              className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden transition-all"
            >
              {/* Accordion Header Row */}
              <div
                onClick={() => toggleAccordion(idx)}
                className="p-5 flex items-center justify-between gap-4 cursor-pointer hover:bg-slate-50/50 transition-colors"
              >
                <div className="flex items-center gap-4 min-w-0">
                  <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 font-bold text-xs flex items-center justify-center flex-shrink-0">
                    {q.question_number || idx + 1}
                  </div>

                  <div className="min-w-0 space-y-1">
                    <div className="flex items-center gap-2.5 flex-wrap">
                      <h3 className="text-sm font-semibold text-slate-900 truncate">
                        {q.question_text}
                      </h3>
                      <span className={`px-2.5 py-0.5 rounded-full border text-[11px] font-semibold ${getRatingBadgeClass(q.rating)}`}>
                        {q.rating}
                      </span>
                    </div>

                    <p className="text-xs text-slate-500 truncate">
                      {q.feedback}
                    </p>
                  </div>
                </div>

                <div className="text-slate-400 p-1 flex-shrink-0">
                  {isOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </div>
              </div>

              {/* Accordion Collapsible Content Body */}
              {isOpen && (
                <div className="px-5 pb-5 pt-2 border-t border-slate-100 bg-slate-50/40 space-y-4">
                  {/* Question details pill bar */}
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded-full bg-indigo-50 text-indigo-700 text-xs font-semibold uppercase">
                      {q.question_type || "descriptive"}
                    </span>
                    {q.topic && (
                      <span className="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 text-xs font-medium">
                        {q.topic}
                      </span>
                    )}
                    <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold">
                      Score: {q.score !== undefined ? `${q.score}/10` : "Evaluated"}
                    </span>
                  </div>

                  {/* Candidate Answer */}
                  <div className="space-y-1.5">
                    <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wide">
                      {q.question_type === "mcq" ? "Your Selection:" : "Candidate Answer:"}
                    </h4>
                    <div className="p-3.5 rounded-xl bg-white border border-slate-200 text-xs text-slate-800 leading-relaxed font-mono">
                      {q.selected_option || q.answer_text}
                    </div>
                  </div>

                  {/* Correct Answer & Explanation for MCQs or reference */}
                  {q.correct_answer && (
                    <div className="space-y-1.5">
                      <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wide flex items-center gap-1.5">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                        {q.question_type === "mcq" ? "Correct Option:" : "Expected Core Concept:"}
                      </h4>
                      <div className="p-3.5 rounded-xl bg-emerald-50/60 border border-emerald-200 text-xs text-emerald-950 leading-relaxed">
                        <p className="font-semibold">{q.correct_answer}</p>
                        {q.explanation && (
                          <p className="text-slate-600 mt-1.5 pt-1.5 border-t border-emerald-100 font-sans">
                            {q.explanation}
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* AI Feedback */}
                  {q.feedback && (
                    <div className="space-y-1.5">
                      <h4 className="text-xs font-bold text-indigo-700 uppercase tracking-wide">
                        AI Evaluation Feedback:
                      </h4>
                      <p className="text-xs text-slate-700 leading-relaxed bg-white p-3 rounded-xl border border-slate-200">
                        {q.feedback}
                      </p>
                    </div>
                  )}

                  {q.strengths && q.strengths.length > 0 && (
                    <div className="space-y-1.5">
                      <h4 className="text-xs font-bold text-emerald-700 uppercase tracking-wide flex items-center gap-1.5">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                        Key Strengths:
                      </h4>
                      <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 pl-1">
                        {q.strengths.map((s: string, sIdx: number) => (
                          <li key={sIdx}>{s}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {q.weaknesses && q.weaknesses.length > 0 && (
                    <div className="space-y-1.5">
                      <h4 className="text-xs font-bold text-amber-700 uppercase tracking-wide flex items-center gap-1.5">
                        <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
                        Areas for Improvement:
                      </h4>
                      <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 pl-1">
                        {q.weaknesses.map((w: string, wIdx: number) => (
                          <li key={wIdx}>{w}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
