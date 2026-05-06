import { useState } from "react";
import { api } from "../api/client";

export function QuestionForm({ onStatusChange }) {
  const [q, setQ] = useState("");
  const [answer, setAnswer] = useState("");

  const ask = async (e) => {
    e.preventDefault();

    try {
      onStatusChange("Thinking...");

      const data = await api.askQuestion(q);

      setAnswer(data.answer || "No answer returned");

      onStatusChange(
        data.chunks_used != null
          ? `Used ${data.chunks_used} chunks`
          : "Done"
      );
    } catch (err) {
      onStatusChange(err.message);
    }
  };

  return (
    <section className="card">
      <h2>Ask Question</h2>

      <form onSubmit={ask}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask something..."
        />
        <button>Ask</button>
      </form>

      {answer && (
        <div className="answer">
          <pre>{answer}</pre>
        </div>
      )}
    </section>
  );
}