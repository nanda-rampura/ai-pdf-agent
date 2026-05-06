import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL

export function QuestionForm({ onStatusChange }) {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')

  const handleAsk = async (event) => {
    event.preventDefault()
    if (!question) {
      onStatusChange('Enter a question')
      return
    }

    onStatusChange('Asking question...')
    setAnswer('')

    try {
      const response = await fetch(
        `${API_BASE}/ask-pdf/?question=${encodeURIComponent(question)}`
      )
      const data = await response.json()

      if (!response.ok) {
        onStatusChange(data.error || 'Query failed')
        return
      }

      setAnswer(data.answer || 'No answer returned')
      onStatusChange(`Used ${data.chunks_used || 0} chunks`)
    } catch (error) {
      console.error(error)
      onStatusChange('Query failed')
    }
  }

  return (
    <section className="card">
      <h2>2. Ask a question</h2>
      <form onSubmit={handleAsk} className="form-grid">
        <input
          type="text"
          value={question}
          placeholder="Enter your question"
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit">Ask</button>
      </form>
      {answer && (
        <div className="answer-box">
          <h3>Answer</h3>
          <pre>{answer}</pre>
        </div>
      )}
    </section>
  )
}
