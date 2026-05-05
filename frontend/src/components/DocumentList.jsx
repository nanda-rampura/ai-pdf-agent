import { useState, useEffect } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

export function DocumentList({ triggerRefresh, onStatusChange }) {
  const [documents, setDocuments] = useState([])

  useEffect(() => {
    fetchDocuments()
  }, [triggerRefresh])

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${API_BASE}/documents`)
      const data = await response.json()
      setDocuments(data.documents || [])
    } catch (error) {
      console.error(error)
      onStatusChange('Failed to load documents')
    }
  }

  const handleDelete = async (docId) => {
    const confirmed = window.confirm(`Delete document ${docId}?`)
    if (!confirmed) {
      return
    }

    try {
      const response = await fetch(`${API_BASE}/documents/${docId}`, {
        method: 'DELETE',
      })
      const data = await response.json()
      if (!response.ok) {
        onStatusChange(data.error || 'Delete failed')
        return
      }

      onStatusChange(data.message || 'Deleted')
      await fetchDocuments()
    } catch (error) {
      console.error(error)
      onStatusChange('Delete failed')
    }
  }

  return (
    <section className="card">
      <h2>3. Stored documents</h2>
      {documents.length === 0 ? (
        <p>No stored documents yet.</p>
      ) : (
        <ul className="doc-list">
          {documents.map((docId) => (
            <li key={docId}>
              <span>{docId}</span>
              <button onClick={() => handleDelete(docId)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
      <button className="secondary" onClick={fetchDocuments}>
        Refresh
      </button>
    </section>
  )
}
