"use client";

import { useState, useEffect } from "react";
import { User, Mail, Award, CheckCircle, Shield } from "lucide-react";
import { getProfile } from "@/lib/api";

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await getProfile();
        setProfile(data);
      } catch (err) {
        console.error("Error loading profile:", err);
      }
    }
    loadProfile();
  }, []);

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-2">
      <div className="space-y-1">
        <h1 className="text-2xl font-bold text-slate-900">Candidate Profile</h1>
        <p className="text-slate-500 text-xs sm:text-sm">
          Overview of candidate credentials and platform activity.
        </p>
      </div>

      <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm space-y-8">
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 rounded-full bg-indigo-600 text-white font-bold text-2xl flex items-center justify-center shadow-lg shadow-indigo-200">
            M
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">{profile?.candidate_name || "Mourya Yarla"}</h2>
            <div className="flex items-center gap-2 text-slate-500 text-xs mt-1">
              <Mail className="w-3.5 h-3.5" />
              <span>{profile?.email || "mourya@example.com"}</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100 space-y-1">
            <div className="flex items-center gap-2 text-indigo-600 text-xs font-semibold">
              <Award className="w-4 h-4" />
              <span>Total Interviews</span>
            </div>
            <p className="text-2xl font-bold text-slate-900">{profile?.total_interviews || 1}</p>
          </div>

          <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100 space-y-1">
            <div className="flex items-center gap-2 text-emerald-600 text-xs font-semibold">
              <CheckCircle className="w-4 h-4" />
              <span>Completed</span>
            </div>
            <p className="text-2xl font-bold text-slate-900">{profile?.completed_interviews || 1}</p>
          </div>

          <div className="bg-slate-50 rounded-2xl p-5 border border-slate-100 space-y-1">
            <div className="flex items-center gap-2 text-amber-600 text-xs font-semibold">
              <Shield className="w-4 h-4" />
              <span>Average Score</span>
            </div>
            <p className="text-2xl font-bold text-slate-900">{profile?.average_score || 8.5}/10</p>
          </div>
        </div>
      </div>
    </div>
  );
}
