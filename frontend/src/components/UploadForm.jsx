import { useState } from "react";
import { api } from "../api/client";

export function UploadForm({ onUploadSuccess, onStatusChange }) {
  const [file, setFile] = useState(null);

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      onStatusChange("Select a PDF");
      return;
    }

    try {
      onStatusChange("Uploading...");

      const data = await api.uploadPDF(file);

      onStatusChange(
        `Uploaded ${data.chunks || 0} chunks (ID: ${data.doc_id})`
      );

      setFile(null);
      onUploadSuccess(); // refresh list
    } catch (err) {
      onStatusChange(err.message);
    }
  };

  return (
    <section className="card">
      <h2>Upload PDF</h2>

      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0])}
        />
        <button>Upload</button>
      </form>
    </section>
  );
}