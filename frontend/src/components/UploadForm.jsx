import { useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL

export function UploadForm({ onUploadSuccess, onStatusChange }) {
  const [file, setFile] = useState(null)

  const handleUpload = async (event) => {
    event.preventDefault()
    if (!file) {
      onStatusChange('Select a PDF before uploading')
      return
    }

    onStatusChange('Uploading PDF...')
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE}/upload-pdf/`, {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()

      if (!response.ok) {
        onStatusChange(data.error || 'Upload failed')
        return
      }

      onStatusChange(`Uploaded ${data.chunks} chunks for doc ${data.doc_id}`)
      setFile(null)
      onUploadSuccess()
    } catch (error) {
      console.error(error)
      onStatusChange('Upload failed')
    }
  }

  return (
    <section className="card">
      <h2>1. Upload PDF</h2>
      <form onSubmit={handleUpload} className="form-grid">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button type="submit">Upload</button>
      </form>
    </section>
  )
}
