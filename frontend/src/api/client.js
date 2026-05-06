const API_BASE = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE) {
  throw new Error("VITE_API_BASE_URL is missing");
}

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      ...(options.body instanceof FormData
        ? {}
        : { "Content-Type": "application/json" }),
    },
    ...options,
  });

  let data = {};
  try {
    data = await res.json();
  } catch {}

  if (!res.ok) {
    throw new Error(data.error || data.detail || "Request failed");
  }

  return data;
}

export const api = {
  uploadPDF: (file) => {
    const formData = new FormData();
    formData.append("file", file);

    return request("/upload-pdf/", {
      method: "POST",
      body: formData,
    });
  },

  getDocuments: () => request("/documents"),

  deleteDocument: (id) =>
    request(`/documents/${id}`, { method: "DELETE" }),

  askQuestion: (question) =>
  request(
    `/ask-pdf/?question=${encodeURIComponent(question)}`
  ),
};