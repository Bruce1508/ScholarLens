import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Landing } from './pages/Landing'
import './App.css'

// Temporary placeholder components - we'll create these next
function Workspace() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 p-8">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Scholarship Workspace</h1>
      <p className="mt-4 text-slate-600 dark:text-slate-400">Coming soon...</p>
    </div>
  )
}

function Profile() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 p-8">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Student Profile</h1>
      <p className="mt-4 text-slate-600 dark:text-slate-400">Coming soon...</p>
    </div>
  )
}

function DraftStudio() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 p-8">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Draft Studio</h1>
      <p className="mt-4 text-slate-600 dark:text-slate-400">Coming soon...</p>
    </div>
  )
}

function Comparison() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 p-8">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Essay Comparison</h1>
      <p className="mt-4 text-slate-600 dark:text-slate-400">Coming soon...</p>
    </div>
  )
}

function Insights() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 p-8">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Insights Lab</h1>
      <p className="mt-4 text-slate-600 dark:text-slate-400">Coming soon...</p>
    </div>
  )
}

function Demo() {
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 p-8">
      <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Demo</h1>
      <p className="mt-4 text-slate-600 dark:text-slate-400">Sample scholarship demo coming soon...</p>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/workspace" element={<Workspace />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/draft" element={<DraftStudio />} />
        <Route path="/comparison" element={<Comparison />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/demo" element={<Demo />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App