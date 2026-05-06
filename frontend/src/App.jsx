import { useState } from "react";
import { UploadForm } from "./components/UploadForm";
import { DocumentList } from "./components/DocumentList";
import { QuestionForm } from "./components/QuestionForm";

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0);
  const [status, setStatus] = useState("");

  const triggerRefresh = () => setRefreshKey((k) => k + 1);

  return (
    <div className="container">
      <h1>AI PDF Agent</h1>

      <p className="status">{status}</p>

      <UploadForm
        onUploadSuccess={triggerRefresh}
        onStatusChange={setStatus}
      />

      <DocumentList
        triggerRefresh={refreshKey}
        onStatusChange={setStatus}
      />

      <QuestionForm onStatusChange={setStatus} />
    </div>
  );
}