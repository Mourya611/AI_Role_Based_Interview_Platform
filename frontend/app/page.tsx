import Link from "next/link";
import { 
  FileText, 
  ShieldCheck, 
  Sparkles, 
  Cpu, 
  ArrowRight, 
  Code, 
  MessageSquare, 
  CheckCircle2, 
  Zap 
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="max-w-6xl mx-auto space-y-10 py-2">
      {/* Top Header Tagline */}
      <div className="flex justify-end">
        <span className="text-xs font-medium text-slate-400 tracking-wide">
          Build Skills. Ace Interviews. Grow Your Career.
        </span>
      </div>

      {/* Hero Section Container */}
      <div className="bg-white rounded-3xl p-8 md:p-10 border border-slate-100 shadow-sm relative overflow-hidden flex flex-col lg:flex-row items-center justify-between gap-10">
        
        {/* Left Column: Hero Content */}
        <div className="flex-1 space-y-6">
          <div className="space-y-3">
            <h1 className="text-4xl lg:text-5xl font-extrabold tracking-tight text-slate-900 leading-tight">
              AI-Powered <span className="text-indigo-600">Interview</span> Platform
            </h1>
            <p className="text-slate-500 text-base lg:text-lg max-w-lg leading-relaxed font-normal">
              Get role-specific, personalized interview questions generated from your resume using AI.
            </p>
          </div>

          {/* 4 Feature Tag Pills */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-100 text-xs font-medium text-slate-700">
              <FileText className="w-4 h-4 text-indigo-600 flex-shrink-0" />
              <span>Resume Based Questions</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-100 text-xs font-medium text-slate-700">
              <ShieldCheck className="w-4 h-4 text-indigo-600 flex-shrink-0" />
              <span>Role Specific Evaluation</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-100 text-xs font-medium text-slate-700">
              <Sparkles className="w-4 h-4 text-indigo-600 flex-shrink-0" />
              <span>AI-Powered Insights</span>
            </div>
            <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-50 border border-slate-100 text-xs font-medium text-slate-700">
              <Cpu className="w-4 h-4 text-indigo-600 flex-shrink-0" />
              <span>Real Interview Experience</span>
            </div>
          </div>

          {/* Primary CTA Button */}
          <div className="pt-2">
            <Link
              href="/new-interview"
              className="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-lg shadow-indigo-200 transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              <span>Start an Interview</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {/* Quote Sub-banner */}
          <div className="pt-4 flex flex-col items-center sm:items-start space-y-1">
            <p className="text-xs italic text-slate-400 font-medium">
              &quot;A smarter way to prepare for your dream role.&quot;
            </p>
            <div className="w-12 h-0.5 bg-indigo-400 rounded-full" />
          </div>
        </div>

        {/* Right Column: Hero Visual Illustration & Floating Feature Badges */}
        <div className="w-full lg:w-80 flex-shrink-0 flex justify-center relative">
          <div className="w-full bg-indigo-50/70 rounded-3xl p-6 border border-indigo-100/60 flex flex-col items-center justify-center relative space-y-3 min-h-[300px]">
            
            {/* Person Illustration Avatar Card */}
            <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-indigo-500 to-indigo-600 flex items-center justify-center text-white shadow-xl shadow-indigo-200 my-2">
              <Code className="w-12 h-12 stroke-[1.75]" />
            </div>

            {/* Floating Cards */}
            <div className="w-full space-y-2.5 pt-2">
              <div className="bg-white/90 backdrop-blur px-3.5 py-2 rounded-xl border border-indigo-100/80 shadow-sm flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-2">
                  <Zap className="w-3.5 h-3.5 text-indigo-600" />
                  Technical Deep Dive
                </span>
              </div>
              <div className="bg-white/90 backdrop-blur px-3.5 py-2 rounded-xl border border-indigo-100/80 shadow-sm flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-2">
                  <MessageSquare className="w-3.5 h-3.5 text-indigo-600" />
                  Real-world Scenarios
                </span>
              </div>
              <div className="bg-white/90 backdrop-blur px-3.5 py-2 rounded-xl border border-indigo-100/80 shadow-sm flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-indigo-600" />
                  Personalized Questions
                </span>
              </div>
              <div className="bg-white/90 backdrop-blur px-3.5 py-2 rounded-xl border border-indigo-100/80 shadow-sm flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-2">
                  <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                  Instant Feedback
                </span>
              </div>
            </div>

          </div>
        </div>

      </div>

      {/* Bottom Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm text-center space-y-1">
          <p className="text-2xl font-bold text-indigo-600">100+</p>
          <p className="text-xs font-medium text-slate-500">Technical Topics</p>
        </div>
        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm text-center space-y-1">
          <p className="text-2xl font-bold text-indigo-600">Multiple</p>
          <p className="text-xs font-medium text-slate-500">Job Roles</p>
        </div>
        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm text-center space-y-1">
          <p className="text-2xl font-bold text-indigo-600">Personalized</p>
          <p className="text-xs font-medium text-slate-500">Questions</p>
        </div>
        <div className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm text-center space-y-1">
          <p className="text-2xl font-bold text-indigo-600">Detailed</p>
          <p className="text-xs font-medium text-slate-500">Performance Analysis</p>
        </div>
      </div>
    </div>
  );
}
