import { useAuthStore } from "@/store/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = useAuthStore.getState().token;
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new ApiError(res.status, body?.detail ?? "Запрос завершился с ошибкой");
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export interface UserOut {
  id: string;
  email: string;
  name: string;
  onboarded: boolean;
  experienced: boolean | null;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface CourseOut {
  id: string;
  title: string;
  slug: string;
  description: string | null;
  icon: string | null;
  order: number;
}

export interface StackWithProgress {
  id: string;
  title: string;
  slug: string;
  description: string | null;
  order: number;
  status: "locked" | "in_progress" | "completed";
}

export interface CourseWithStacks extends CourseOut {
  stacks: StackWithProgress[];
}

export interface LessonWithProgress {
  id: string;
  title: string;
  slug: string;
  order: number;
  status: "locked" | "in_progress" | "completed";
  lesson_read: boolean;
  practice_done: boolean;
}

export interface StackLessonsOut {
  id: string;
  title: string;
  slug: string;
  description: string | null;
  lessons: LessonWithProgress[];
}

export interface LessonDetail {
  id: string;
  title: string;
  slug: string;
  order: number;
  content: string | null;
  stack_slug: string;
  stack_title: string;
  lesson_read: boolean;
  practice_done: boolean;
}

export interface ChatMessageOut {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface ExerciseOut {
  id: string;
  type: "mcq" | "open" | "code";
  question: string;
  options: string[] | null;
  order: number;
}

export interface ExerciseCheckOut {
  correct: boolean;
  explanation: string | null;
  correct_answer: string | null;
}

export interface TestQuestion {
  question: string;
  options: string[];
}

export interface TestOut {
  id: string;
  pass_threshold: number;
  time_limit: number | null;
  questions: TestQuestion[];
}

export interface MistakeOut {
  question: string;
  user_answer: string;
  correct_answer: string;
}

export interface TestResultOut {
  id: string;
  score: number;
  passed: boolean;
  mistakes: MistakeOut[];
  attempt: number;
  created_at: string;
}

export interface PlacementQuestion {
  question: string;
  options: string[];
}

export interface PlacementResultOut {
  id: string;
  result_level: "beginner" | "intermediate" | "advanced";
  score: number;
  unlocked_stacks: string[];
  completed_at: string;
}

export const api = {
  register: (data: { email: string; password: string; name: string }) =>
    request<UserOut>("/api/auth/register", { method: "POST", body: JSON.stringify(data) }),

  login: (data: { email: string; password: string }) =>
    request<Token>("/api/auth/login", { method: "POST", body: JSON.stringify(data) }),

  me: () => request<UserOut>("/api/auth/me"),

  listCourses: () => request<CourseOut[]>("/api/courses"),

  getCourse: (slug: string) => request<CourseOut>(`/api/courses/${slug}`),

  getCourseStacks: (slug: string) => request<CourseWithStacks>(`/api/courses/${slug}/stacks`),

  getStackLessons: (slug: string) => request<StackLessonsOut>(`/api/stacks/${slug}/lessons`),

  getLesson: (slug: string) => request<LessonDetail>(`/api/lessons/${slug}`),

  markLessonRead: (slug: string) =>
    request<LessonDetail>(`/api/lessons/${slug}/read`, { method: "PATCH" }),

  completeOnboarding: (experienced: boolean) =>
    request<UserOut>("/api/onboarding", { method: "POST", body: JSON.stringify({ experienced }) }),

  getPlacementQuestions: (courseSlug: string) =>
    request<PlacementQuestion[]>(`/api/placement/${courseSlug}`),

  submitPlacement: (courseSlug: string, answers: string[]) =>
    request<PlacementResultOut>(`/api/placement/${courseSlug}/submit`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),

  getExercises: (lessonSlug: string) => request<ExerciseOut[]>(`/api/lessons/${lessonSlug}/exercises`),

  checkExercise: (exerciseId: string, answer: string) =>
    request<ExerciseCheckOut>(`/api/exercises/${exerciseId}/check`, {
      method: "POST",
      body: JSON.stringify({ answer }),
    }),

  getTest: (lessonSlug: string) => request<TestOut>(`/api/lessons/${lessonSlug}/test`),

  submitTest: (lessonSlug: string, answers: string[]) =>
    request<TestResultOut>(`/api/lessons/${lessonSlug}/test/submit`, {
      method: "POST",
      body: JSON.stringify({ answers }),
    }),

  getTestResults: (lessonSlug: string) =>
    request<TestResultOut[]>(`/api/lessons/${lessonSlug}/test/results`),

  getChatHistory: (lessonSlug: string) =>
    request<ChatMessageOut[]>(`/api/chat/${lessonSlug}/history`),

  clearChatHistory: (lessonSlug: string) =>
    request<{ detail: string }>(`/api/chat/${lessonSlug}/history`, { method: "DELETE" }),

  streamChat: async (
    lessonSlug: string,
    message: string,
    onToken: (token: string) => void,
  ): Promise<void> => {
    const token = useAuthStore.getState().token;
    const headers = new Headers({ "Content-Type": "application/json" });
    if (token) headers.set("Authorization", `Bearer ${token}`);

    const res = await fetch(`${API_URL}/api/chat/${lessonSlug}`, {
      method: "POST",
      headers,
      body: JSON.stringify({ message }),
    });

    if (!res.ok || !res.body) {
      const body = await res.json().catch(() => null);
      throw new ApiError(res.status, body?.detail ?? "Не удалось получить ответ от AI");
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      const lines = buffer.split("\n\n");
      buffer = lines.pop() ?? "";

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed.startsWith("data:")) continue;
        const data = trimmed.slice(5).trim();
        if (data === "[DONE]") return;
        try {
          const parsed = JSON.parse(data) as { content?: string };
          if (parsed.content) onToken(parsed.content);
        } catch {
          // ignore malformed chunk
        }
      }
    }
  },
};
