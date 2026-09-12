const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function uploadResume(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/api/resumes/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to upload resume.");
  }
  return res.json();
}

export async function createInterview(resumeId: string, targetRole: string, totalQuestions: number = 5) {
  const res = await fetch(`${API_BASE_URL}/api/interviews`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resume_id: resumeId,
      target_role: targetRole,
      total_questions: totalQuestions,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to create interview session.");
  }
  return res.json();
}

export async function getInterviewSession(sessionId: string) {
  const res = await fetch(`${API_BASE_URL}/api/interviews/${sessionId}`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch interview session.");
  return res.json();
}

export async function submitAnswer(sessionId: string, questionId: string, answerText: string, selectedOption?: string) {
  const res = await fetch(`${API_BASE_URL}/api/interviews/${sessionId}/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question_id: questionId,
      answer_text: answerText,
      selected_option: selectedOption,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to submit answer.");
  }
  return res.json();
}

export async function completeInterviewSession(sessionId: string) {
  const res = await fetch(`${API_BASE_URL}/api/interviews/${sessionId}/complete`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to complete interview session.");
  return res.json();
}

export async function getInterviewReport(sessionId: string) {
  const res = await fetch(`${API_BASE_URL}/api/interviews/${sessionId}/report`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch interview report.");
  return res.json();
}

export async function listInterviews() {
  const res = await fetch(`${API_BASE_URL}/api/interviews`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to list interviews.");
  return res.json();
}

export async function getProfile() {
  const res = await fetch(`${API_BASE_URL}/api/profile`, {
    cache: "no-store",
  });
  if (!res.ok) throw new Error("Failed to fetch profile.");
  return res.json();
}

export function getReportDownloadUrl(sessionId: string) {
  return `${API_BASE_URL}/api/interviews/${sessionId}/download-report`;
}
