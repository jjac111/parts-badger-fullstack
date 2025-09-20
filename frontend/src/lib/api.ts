export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  uploadCsv: async (file: File): Promise<{ task_id: string }> => {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${API_BASE_URL}/upload-csv/`, { method: "POST", body: form });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  taskStatus: (taskId: string) => request<{ task_id: string; state: string; info: any }>(`/tasks/${taskId}/`),
  listResults: (params: { search?: string; page?: number }) => {
    const u = new URL(`${API_BASE_URL}/csv-results/`);
    if (params.search) u.searchParams.set("search", params.search);
    if (params.page) u.searchParams.set("page", String(params.page));
    return request<{ count: number; next: string | null; previous: string | null; results: any[] }>(u.pathname + u.search);
  },
};
