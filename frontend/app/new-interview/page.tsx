"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { 
  UploadCloud, 
  FileText, 
  X, 
  ArrowRight, 
  ArrowLeft, 
  Check, 
  Server, 
  Brain, 
  Code, 
  Database, 
  Monitor, 
  Cloud,
  Loader2
} from "lucide-react";
import { uploadResume, createInterview } from "@/lib/api";

export default function NewInterviewPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [file, setFile] = useState<File | null>(null);
  const [uploadedResumeId, setUploadedResumeId] = useState<string | null>(null);
  const [selectedRole, setSelectedRole] = useState<string>("AI/ML Engineer");
  const [questionCount, setQuestionCount] = useState<number>(5);
  
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [isCreatingSession, setIsCreatingSession] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const roles = [
    {
      title: "Backend Engineer",
      description: "APIs, Databases, System Design",
      icon: Server,
    },
    {
      title: "AI/ML Engineer",
      description: "Machine Learning, Deep Learning",
      icon: Brain,
    },
    {
      title: "Full Stack Developer",
      description: "Frontend + Backend",
      icon: Code,
    },
    {
      title: "Data Engineer",
      description: "Data Pipelines, Big Data",
      icon: Database,
    },
    {
      title: "Software Engineer",
      description: "DSA, OOP, System Design",
      icon: Monitor,
    },
    {
      title: "Cloud Engineer",
      description: "Cloud Platforms, DevOps",
      icon: Cloud,
    },
  ];

  const handleFileSelect = (selectedFile: File) => {
    setErrorMsg(null);
    if (!selectedFile.name.endsWith(".pdf") && !selectedFile.name.endsWith(".txt")) {
      setErrorMsg("Only PDF or TXT files are supported.");
      return;
    }
    if (selectedFile.size > 5 * 1024 * 1024) {
      setErrorMsg("File size exceeds maximum 5MB limit.");
      return;
    }
    setFile(selectedFile);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleNextStep1 = async () => {
    if (!file) {
      setErrorMsg("Please upload a resume before proceeding.");
      return;
    }
    setIsUploading(true);
    setErrorMsg(null);
    try {
      const res = await uploadResume(file);
      setUploadedResumeId(res.id);
      setStep(2);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to upload resume.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleStartInterview = async () => {
    if (!uploadedResumeId) {
      setErrorMsg("Resume upload session missing. Please re-upload resume.");
      setStep(1);
      return;
    }
    setIsCreatingSession(true);
    setErrorMsg(null);
    try {
      const sessionData = await createInterview(uploadedResumeId, selectedRole, questionCount);
      router.push(`/interview/${sessionData.session_id}`);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to start interview session.");
      setIsCreatingSession(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 py-2">
      {/* 3-Step Stepper Progress Bar */}
      <div className="flex items-center justify-center gap-4 sm:gap-8 max-w-xl mx-auto py-2">
        {/* Step 1 Indicator */}
        <div className="flex items-center gap-2">
          <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold ${
            step > 1 
              ? "bg-indigo-600 text-white" 
              : step === 1 
              ? "bg-indigo-600 text-white shadow-md shadow-indigo-200" 
              : "bg-slate-200 text-slate-500"
          }`}>
            {step > 1 ? <Check className="w-4 h-4" /> : "1"}
          </div>
          <span className={`text-xs font-medium ${step >= 1 ? "text-indigo-600" : "text-slate-400"}`}>
            {step > 1 ? "Upload Resume ✓" : "Upload Resume"}
          </span>
        </div>

        <div className={`flex-1 h-0.5 max-w-[60px] ${step > 1 ? "bg-indigo-600" : "bg-slate-200"}`} />

        {/* Step 2 Indicator */}
        <div className="flex items-center gap-2">
          <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold ${
            step > 2 
              ? "bg-indigo-600 text-white" 
              : step === 2 
              ? "bg-indigo-600 text-white shadow-md shadow-indigo-200" 
              : "bg-slate-200 text-slate-500"
          }`}>
            {step > 2 ? <Check className="w-4 h-4" /> : "2"}
          </div>
          <span className={`text-xs font-medium ${step >= 2 ? "text-indigo-600" : "text-slate-400"}`}>
            Select Role
          </span>
        </div>

        <div className={`flex-1 h-0.5 max-w-[60px] ${step > 2 ? "bg-indigo-600" : "bg-slate-200"}`} />

        {/* Step 3 Indicator */}
        <div className="flex items-center gap-2">
          <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold ${
            step === 3 ? "bg-indigo-600 text-white" : "bg-slate-200 text-slate-500"
          }`}>
            3
          </div>
          <span className={`text-xs font-medium ${step === 3 ? "text-indigo-600" : "text-slate-400"}`}>
            Start Interview
          </span>
        </div>
      </div>

      {/* Validation / API Error Banner */}
      {errorMsg && (
        <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-xl flex items-center justify-between">
          <span>{errorMsg}</span>
          <button onClick={() => setErrorMsg(null)} className="text-red-500 hover:text-red-700">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* STEP 1: RESUME UPLOAD */}
      {step === 1 && (
        <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm space-y-6">
          <div className="space-y-1">
            <h2 className="text-2xl font-bold text-slate-900">Upload Your Resume</h2>
            <p className="text-slate-500 text-sm">
              Upload your resume (PDF or text) to get personalized interview questions.
            </p>
          </div>

          {/* Drag & Drop Upload Zone */}
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleDrop}
            className="border-2 border-dashed border-slate-200 rounded-2xl p-10 flex flex-col items-center justify-center space-y-3 bg-slate-50/50 hover:bg-slate-50 hover:border-indigo-300 transition-all cursor-pointer"
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
              accept=".pdf,.txt"
              className="hidden"
            />
            <div className="w-12 h-12 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 mb-1">
              <UploadCloud className="w-6 h-6" />
            </div>
            <div className="text-center space-y-1">
              <p className="text-sm font-semibold text-slate-800">
                Drag and drop your resume here
              </p>
              <p className="text-xs text-slate-400">or</p>
            </div>
            <button
              type="button"
              className="px-5 py-2.5 rounded-xl bg-indigo-600 text-white font-medium text-xs shadow-sm hover:bg-indigo-700 transition-colors"
            >
              Choose File
            </button>
            <p className="text-xs text-slate-400 pt-2">
              Supported formats: PDF, TXT (Max size: 5MB)
            </p>
          </div>

          {/* File Selected Card Preview */}
          {file && (
            <div className="bg-slate-50 border border-slate-200/80 rounded-2xl p-4 flex items-center justify-between">
              <div className="flex items-center gap-3.5">
                <div className="w-10 h-10 rounded-xl bg-rose-50 border border-rose-100 flex items-center justify-center text-rose-500 font-bold text-xs">
                  <FileText className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-800">{file.name}</p>
                  <p className="text-xs text-slate-400">
                    {(file.size / (1024 * 1024)).toFixed(1)} MB
                  </p>
                </div>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setFile(null);
                }}
                className="text-slate-400 hover:text-slate-600 p-1.5 rounded-lg hover:bg-slate-200/60 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Bottom Next Button */}
          <div className="flex justify-end pt-4">
            <button
              onClick={handleNextStep1}
              disabled={!file || isUploading}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-md shadow-indigo-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isUploading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Processing Resume...</span>
                </>
              ) : (
                <>
                  <span>Next</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: SELECT TARGET ROLE */}
      {step === 2 && (
        <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm space-y-6">
          <div className="space-y-1">
            <h2 className="text-2xl font-bold text-slate-900">Select Target Role</h2>
            <p className="text-slate-500 text-sm">
              Choose the role you want to be interviewed for. Questions will be tailored based on the role and your resume.
            </p>
          </div>

          {/* Role Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
            {roles.map((role) => {
              const RoleIcon = role.icon;
              const isSelected = selectedRole === role.title;
              return (
                <div
                  key={role.title}
                  onClick={() => setSelectedRole(role.title)}
                  className={`p-6 rounded-2xl border-2 transition-all cursor-pointer flex flex-col items-center text-center space-y-3 relative ${
                    isSelected
                      ? "border-indigo-600 bg-indigo-50/40 shadow-sm"
                      : "border-slate-100 hover:border-slate-200 bg-white"
                  }`}
                >
                  <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-colors ${
                    isSelected ? "bg-indigo-600 text-white shadow-md shadow-indigo-200" : "bg-indigo-50 text-indigo-600"
                  }`}>
                    <RoleIcon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">{role.title}</h3>
                    <p className="text-xs text-slate-400 mt-1">{role.description}</p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Question Count Selection */}
          <div className="space-y-3 pt-4 border-t border-slate-100">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-slate-900">Number of Questions</h3>
                <p className="text-xs text-slate-500">Select session length and question distribution</p>
              </div>
              <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700">
                {questionCount} Questions Selected
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { count: 5, label: "5 Questions", tag: "Quick Screening", time: "~15 mins" },
                { count: 7, label: "7 Questions", tag: "Standard Assessment", time: "~25 mins" },
                { count: 12, label: "12 Questions", tag: "In-Depth Technical", time: "~45 mins" },
                { count: 15, label: "15 Questions", tag: "Full Panel Simulation", time: "~60 mins" }
              ].map((item) => {
                const isCountSelected = questionCount === item.count;
                return (
                  <div
                    key={item.count}
                    onClick={() => setQuestionCount(item.count)}
                    className={`p-3.5 rounded-xl border-2 cursor-pointer transition-all flex flex-col justify-between text-left ${
                      isCountSelected
                        ? "border-indigo-600 bg-indigo-50/50 shadow-sm"
                        : "border-slate-200 hover:border-slate-300 bg-white"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className={`font-bold text-sm ${isCountSelected ? "text-indigo-900" : "text-slate-800"}`}>
                        {item.count} Questions
                      </span>
                      {isCountSelected && (
                        <div className="w-2.5 h-2.5 rounded-full bg-indigo-600" />
                      )}
                    </div>
                    <div className="mt-1">
                      <p className="text-[11px] font-semibold text-indigo-600">{item.tag}</p>
                      <p className="text-[10px] text-slate-400 mt-0.5">{item.time}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-between pt-4">
            <button
              onClick={() => setStep(1)}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 font-medium text-sm transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back</span>
            </button>
            <button
              onClick={() => {
                setStep(3);
                handleStartInterview();
              }}
              disabled={isCreatingSession}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-md shadow-indigo-200 transition-all disabled:opacity-50"
            >
              <span>Next</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: STARTING INTERVIEW LOADING STATE */}
      {step === 3 && (
        <div className="bg-white rounded-3xl p-12 border border-slate-100 shadow-sm flex flex-col items-center justify-center text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600 mb-2">
            <Loader2 className="w-8 h-8 animate-spin" />
          </div>
          <div className="space-y-1">
            <h3 className="text-xl font-bold text-slate-900">Constructing RAG Interview Context</h3>
            <p className="text-slate-500 text-sm max-w-md">
              Analyzing candidate resume, retrieving Pinecone technical knowledge chunks, and generating your dynamic first question...
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
