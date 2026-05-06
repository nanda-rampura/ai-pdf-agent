import { useState } from "react";
import { UploadForm } from "./components/UploadForm";
import { DocumentList } from "./components/DocumentList";
import { QuestionForm } from "./components/QuestionForm";
import "./App.css";

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [status, setStatus] = useState("");

  const triggerRefresh = () => setRefreshKey((k) => k + 1);

  return (
    <div className="container">
      <h1>AI PDF Agent</h1>

      <p className="status">{status}</p>

      <div className="grid">
        <UploadForm
          onUploadSuccess={triggerRefresh}
          onStatusChange={setStatus}
        />

        <QuestionForm onStatusChange={setStatus} />
      </div>

      <div style={{ marginTop: "18px" }}>
        <DocumentList
          triggerRefresh={refreshKey}
          onStatusChange={setStatus}
        />
      </div>
    </div>
  );
}