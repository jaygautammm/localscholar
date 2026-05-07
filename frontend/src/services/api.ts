const API_BASE = "http://127.0.0.1:8000";

// Type definitions
export interface HealthResponse {
  status: string;
  message: string;
}

export interface DocumentInfo {
  file_name: string;
  size_bytes: number;
}

export interface DocumentsResponse {
  documents: DocumentInfo[];
  count: number;
}

export interface IngestRequest {
  file_name: string;
  reset_collection?: boolean;
  max_chars?: number;
  overlap_chars?: number;
}

export interface UploadResponse {
  message: string;
  file_name: string;
  size_bytes: number;
  saved_to: string;
}

export interface IngestResponse {
  message: string;
  result: {
    source: string;
    chunks_indexed: number;
  };
}

export interface SourceInfo {
  source_number: number;
  file: string;
  chapter: string;
  page_start: number;
  page_end: number;
  distance: number;
  preview: string;
}

export interface ChatRequest {
  question: string;
  n_results?: number;
  file_name?: string | null;
}

export interface ChatResponse {
  question: string;
  answer: string;
  sources: SourceInfo[];
}

export async function uploadPDF(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload-pdf`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to upload PDF");
  }

  return res.json();
}

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Failed to fetch health");
  return res.json();
}

export async function fetchDocuments(): Promise<DocumentsResponse> {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) throw new Error("Failed to fetch documents");
  return res.json();
}

export async function ingestDocument(payload: IngestRequest): Promise<IngestResponse> {
  const res = await fetch(`${API_BASE}/ingest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to ingest document");
  }

  return res.json();
}

export async function chatWithDocument(payload: ChatRequest): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Failed to chat");
  }

  return res.json();
}