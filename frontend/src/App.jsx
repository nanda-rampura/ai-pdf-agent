import { useState } from 'react'
import { UploadForm } from './components/UploadForm'
import { QuestionForm } from './components/QuestionForm'
import { DocumentList } from './components/DocumentList'

function App() {
  const [status, setStatus] = useState('')
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleUploadSuccess = () => {
    setRefreshTrigger((prev) => prev + 1)
  }

  return (
    <div className="app-shell">
      <header>
        <h1>AI PDF Agent</h1>
        <p>Upload a PDF, ask questions, and browse stored documents.</p>
      </header>

      <UploadForm 
        onUploadSuccess={handleUploadSuccess}
        onStatusChange={setStatus}
      />

      <QuestionForm onStatusChange={setStatus} />

      <DocumentList 
        triggerRefresh={refreshTrigger}
        onStatusChange={setStatus}
      />

      <footer>
        <p>{status}</p>
      </footer>
    </div>
  )
}

export default App
