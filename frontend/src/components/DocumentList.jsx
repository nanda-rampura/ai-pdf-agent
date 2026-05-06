import { useEffect, useState } from "react";
import { api } from "../api/client";

export function DocumentList({ triggerRefresh, onStatusChange }) {
  const [docs, setDocs] = useState([]);

  const load = async () => {
    try {
      const data = await api.getDocuments();
      setDocs(data.documents || data || []);
    } catch (err) {
      onStatusChange(err.message);
    }
  };

  useEffect(() => {
    load();
  }, [triggerRefresh]);

  const handleDelete = async (id) => {
    if (!confirm("Delete document?")) return;

    try {
      await api.deleteDocument(id);
      onStatusChange("Deleted");
      load();
    } catch (err) {
      onStatusChange(err.message);
    }
  };

  return (
    <section className="card">
      <h2>Documents</h2>

      {docs.length === 0 ? (
        <p>No documents</p>
      ) : (
        docs.map((id) => (
          <div key={id} className="doc-item">
            {id}
            <button onClick={() => handleDelete(id)}>Delete</button>
          </div>
        ))
      )}

      <button onClick={load}>Refresh</button>
    </section>
  );
}