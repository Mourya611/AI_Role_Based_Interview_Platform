"use client";

import { useState } from "react";
import { Settings, Save, Check } from "lucide-react";

export default function SettingsPage() {
  const [questionCount, setQuestionCount] = useState<number>(5);
  const [defaultRole, setDefaultRole] = useState<string>("Backend Engineer");
  const [saved, setSaved] = useState<boolean>(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-2">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold text-slate-900">Platform Settings</h1>
        <p className="text-slate-500 text-xs sm:text-sm">
          Customize default interview configurations and AI evaluation preferences.
        </p>
      </div>

      <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm space-y-6">
        <div className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-bold text-slate-800 uppercase tracking-wide">
              Default Questions Per Interview Session
            </label>
            <select
              value={questionCount}
              onChange={(e) => setQuestionCount(Number(e.target.value))}
              className="w-full max-w-xs p-3 rounded-xl border border-slate-200 text-sm text-slate-800 outline-none focus:border-indigo-600"
            >
              <option value={3}>3 Questions (Quick Audit)</option>
              <option value={5}>5 Questions (Standard Technical Interview)</option>
              <option value={10}>10 Questions (Deep Dive Screening)</option>
            </select>
          </div>

          <div className="space-y-1.5 pt-2">
            <label className="text-xs font-bold text-slate-800 uppercase tracking-wide">
              Preferred Target Role
            </label>
            <select
              value={defaultRole}
              onChange={(e) => setDefaultRole(e.target.value)}
              className="w-full max-w-xs p-3 rounded-xl border border-slate-200 text-sm text-slate-800 outline-none focus:border-indigo-600"
            >
              <option value="Backend Engineer">Backend Engineer</option>
              <option value="AI/ML Engineer">AI/ML Engineer</option>
              <option value="Full Stack Developer">Full Stack Developer</option>
              <option value="Data Engineer">Data Engineer</option>
              <option value="Software Engineer">Software Engineer</option>
              <option value="Cloud Engineer">Cloud Engineer</option>
            </select>
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100 flex items-center gap-4">
          <button
            onClick={handleSave}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs shadow-md shadow-indigo-200 transition-colors"
          >
            {saved ? (
              <>
                <Check className="w-4 h-4" />
                <span>Preferences Saved</span>
              </>
            ) : (
              <>
                <Save className="w-4 h-4" />
                <span>Save Preferences</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
