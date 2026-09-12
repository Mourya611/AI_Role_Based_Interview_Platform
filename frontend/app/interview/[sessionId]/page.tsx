"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { Clock, Loader2, AlertCircle, CheckCircle2, HelpCircle, FileQuestion, Sparkles } from "lucide-react";
import { getInterviewSession, submitAnswer, completeInterviewSession } from "@/lib/api";

export default function InterviewScreenPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.sessionId as string;

  const [session, setSession] = useState<any>(null);
  const [currentQuestion, setCurrentQuestion] = useState<any>(null);
  const [answerText, setAnswerText] = useState<string>("");
  const [selectedOption, setSelectedOption] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Live Countdown Timer (default 25 mins = 1500s)
  const [secondsLeft, setSecondsLeft] = useState<number>(1500);

  useEffect(() => {
    async function loadData() {
      try {
        setIsLoading(true);
        const data = await getInterviewSession(sessionId);
        setSession(data);
        setCurrentQuestion(data.current_question);
        
        // Dynamic timer based on total questions (approx 3 mins per question)
        const total = data.total_questions || 5;
        setSecondsLeft(total * 180);
      } catch (err: any) {
        setErrorMsg(err.message || "Failed to load interview session.");
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, [sessionId]);

  // Countdown timer interval
  useEffect(() => {
    const timer = setInterval(() => {
      setSecondsLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTimer = (totalSeconds: number) => {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    return `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  };

  const handleSubmitAnswer = async () => {
    const isMcq = currentQuestion?.question_type === "mcq";
    if (isMcq && !selectedOption) {
      setErrorMsg("Please select an option before submitting.");
      return;
    }
    if (!isMcq && !answerText.trim()) {
      setErrorMsg("Please type your answer before submitting.");
      return;
    }

    setIsSubmitting(true);
    setErrorMsg(null);
    try {
      const submissionText = isMcq ? selectedOption : answerText;
      const res = await submitAnswer(sessionId, currentQuestion.id, submissionText, isMcq ? selectedOption : undefined);
      
      setAnswerText("");
      setSelectedOption("");

      if (res.is_completed || !res.next_question) {
        router.push(`/results/${sessionId}`);
      } else {
        setCurrentQuestion(res.next_question);
        setSession((prev: any) => ({
          ...prev,
          current_question_number: res.next_question.question_number,
          current_difficulty: res.next_question.difficulty
        }));
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to submit answer.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEndInterview = async () => {
    if (confirm("Are you sure you want to end this interview early? Your answers so far will be evaluated.")) {
      try {
        await completeInterviewSession(sessionId);
        router.push(`/results/${sessionId}`);
      } catch (err) {
        router.push(`/results/${sessionId}`);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
        <p className="text-slate-500 text-sm font-medium">Loading interview environment...</p>
      </div>
    );
  }

  const qNumber = currentQuestion?.question_number || session?.current_question_number || 1;
  const qTotal = session?.total_questions || 5;
  const qType = currentQuestion?.question_type || "descriptive";
  const progressPercent = Math.round(((qNumber - 1) / qTotal) * 100);

  const getQuestionTypeBadge = (type: string) => {
    switch (type) {
      case "mcq":
        return { label: "Multiple Choice", bg: "bg-blue-50 text-blue-700 border-blue-100" };
      case "short_answer":
        return { label: "Short Answer", bg: "bg-purple-50 text-purple-700 border-purple-100" };
      case "scenario":
        return { label: "Scenario Problem", bg: "bg-emerald-50 text-emerald-700 border-emerald-100" };
      default:
        return { label: "Descriptive", bg: "bg-indigo-50 text-indigo-700 border-indigo-100" };
    }
  };

  const typeBadge = getQuestionTypeBadge(qType);

  return (
    <div className="max-w-6xl mx-auto space-y-6 py-2">
      {/* Top Bar Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-slate-900">Technical Interview</h1>
            <span className="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 text-xs font-semibold">
              Live Session
            </span>
          </div>
          <p className="text-slate-500 text-xs sm:text-sm">
            Questions adapt to your responses and test core competency in <span className="font-semibold text-slate-700">{session?.target_role}</span>.
          </p>
        </div>

        {/* Timer & End Interview Button */}
        <div className="flex items-center gap-4 flex-shrink-0">
          <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white border border-slate-200 text-slate-700 text-xs font-semibold shadow-sm">
            <Clock className="w-4 h-4 text-indigo-600" />
            <span>{formatTimer(secondsLeft)}</span>
          </div>

          <button
            onClick={handleEndInterview}
            className="px-4 py-2 rounded-xl bg-white border border-rose-200 text-rose-600 hover:bg-rose-50 text-xs font-semibold transition-colors shadow-sm"
          >
            End Interview
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white p-3 rounded-2xl border border-slate-100 shadow-sm flex items-center gap-4">
        <div className="flex-1 bg-slate-100 h-2 rounded-full overflow-hidden">
          <div 
            className="bg-indigo-600 h-full rounded-full transition-all duration-500"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        <span className="text-xs font-bold text-slate-600 min-w-[70px] text-right">
          {progressPercent}% Done
        </span>
      </div>

      {errorMsg && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-xl flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
        
        {/* Left Column: Question Card */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-sm space-y-6 relative border-l-4 border-l-indigo-600">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs font-bold text-indigo-600 tracking-wide uppercase">
                Question {qNumber} of {qTotal}
              </p>
              <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${typeBadge.bg}`}>
                {typeBadge.label}
              </span>
            </div>

            <div className="flex flex-wrap items-center gap-2 pt-0.5">
              <span className="px-3 py-1 rounded-full bg-indigo-50 text-indigo-700 text-xs font-semibold">
                {session?.target_role || "AI/ML Engineer"}
              </span>
              <span className="px-3 py-1 rounded-full bg-amber-50 text-amber-700 text-xs font-semibold">
                {currentQuestion?.difficulty || "Medium"} Difficulty
              </span>
              {currentQuestion?.topic && (
                <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-medium">
                  {currentQuestion.topic}
                </span>
              )}
            </div>
          </div>

          <div className="pt-2">
            <p className="text-slate-900 font-medium text-base sm:text-lg leading-relaxed whitespace-pre-line">
              {currentQuestion?.question_text || "Loading question..."}
            </p>
          </div>

          {currentQuestion?.concept && (
            <div className="pt-2 border-t border-slate-100 flex items-center gap-1.5 text-xs text-slate-400">
              <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
              <span>Core Concept: {currentQuestion.concept}</span>
            </div>
          )}
        </div>

        {/* Right Column: Dynamic Input Section based on Question Type */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-100 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <label className="block text-xs font-bold text-slate-800 uppercase tracking-wide">
              {qType === "mcq" ? "Select One Option" : "Your Answer"}
            </label>
            <span className="text-xs text-slate-400">
              {qType === "mcq" 
                ? "Choose the single most accurate option" 
                : qType === "short_answer" 
                ? "Concise 1-3 sentences" 
                : "Comprehensive architectural answer"}
            </span>
          </div>

          {/* MCQ Options Rendering */}
          {qType === "mcq" ? (
            <div className="space-y-3 pt-1">
              {(currentQuestion?.options || [
                "A) Standard baseline approach",
                "B) Optimized vectorized approach",
                "C) Distributed partitioning approach",
                "D) In-memory cached approach"
              ]).map((option: string, idx: number) => {
                const isSelected = selectedOption === option;
                const letter = option.slice(0, 2);
                return (
                  <div
                    key={idx}
                    onClick={() => setSelectedOption(option)}
                    className={`p-4 rounded-2xl border-2 cursor-pointer transition-all flex items-start gap-3.5 ${
                      isSelected
                        ? "border-indigo-600 bg-indigo-50/50 shadow-sm"
                        : "border-slate-200 hover:border-slate-300 bg-white"
                    }`}
                  >
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5 transition-colors ${
                      isSelected ? "bg-indigo-600 text-white" : "bg-slate-100 text-slate-600"
                    }`}>
                      {["A", "B", "C", "D"][idx]}
                    </div>
                    <span className={`text-sm leading-relaxed ${isSelected ? "text-indigo-950 font-medium" : "text-slate-700"}`}>
                      {option.replace(/^[A-D]\)\s*/, "")}
                    </span>
                  </div>
                );
              })}
            </div>
          ) : qType === "short_answer" ? (
            /* Short Answer Compact Input */
            <div className="space-y-2">
              <textarea
                rows={4}
                value={answerText}
                onChange={(e) => setAnswerText(e.target.value)}
                placeholder="State your answer clearly and concisely (formula, mechanism, or definition)..."
                maxLength={600}
                className="w-full p-4 rounded-2xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none text-sm text-slate-800 leading-relaxed resize-none transition-all placeholder:text-slate-300"
              />
              <div className="flex items-center justify-between text-xs text-slate-400 px-1">
                <span>Recommended: 1-3 sentences</span>
                <span>{answerText.length}/600</span>
              </div>
            </div>
          ) : (
            /* Descriptive / Scenario Multiline Textarea */
            <div className="space-y-2">
              <textarea
                rows={8}
                value={answerText}
                onChange={(e) => setAnswerText(e.target.value)}
                placeholder={
                  qType === "scenario"
                    ? "Explain your diagnostic steps, design choices, components, and trade-offs..."
                    : "Type your detailed technical explanation here..."
                }
                maxLength={2500}
                className="w-full p-4 rounded-2xl border border-slate-200 focus:border-indigo-600 focus:ring-2 focus:ring-indigo-100 outline-none text-sm text-slate-800 leading-relaxed resize-none transition-all placeholder:text-slate-300"
              />
              <div className="flex items-center justify-between text-xs text-slate-400 px-1">
                <span>Be specific about algorithms, libraries, and edge cases</span>
                <span>{answerText.length}/2500</span>
              </div>
            </div>
          )}

          <div className="flex justify-end pt-3">
            <button
              onClick={handleSubmitAnswer}
              disabled={isSubmitting || (qType === "mcq" ? !selectedOption : !answerText.trim())}
              className="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-md shadow-indigo-200 transition-all disabled:opacity-50 flex items-center gap-2 cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Evaluating Answer...</span>
                </>
              ) : (
                <span>Submit Answer</span>
              )}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
