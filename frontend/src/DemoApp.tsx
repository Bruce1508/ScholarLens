import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

// API base URL
const API_URL = 'http://localhost:8000/api/v1/demo'

// Types
interface Scholarship {
  id: number
  name: string
  organization: string
  description: string
  amount: number
}

interface Student {
  id: number
  name: string
  gpa: number
  activities: string[]
  achievements: string[]
  goals: string
}

interface Persona {
  persona_name: string
  tone: string
  weights: {
    Academics: number
    Leadership: number
    Community: number
    Innovation: number
    FinancialNeed: number
    Research: number
  }
  rationale: string
}

interface EssayParagraph {
  paragraph: string
  focus: string
  reason: string
  alignment_score: number
}

interface Essay {
  persona_name: string
  tone_used: string
  essay: EssayParagraph[]
  overall_alignment: number
  summary: string
}

function App() {
  // State
  const [scholarships, setScholarships] = useState<Scholarship[]>([])
  const [students, setStudents] = useState<Student[]>([])
  const [selectedScholarship, setSelectedScholarship] = useState<number>(1)
  const [selectedStudent, setSelectedStudent] = useState<number>(1)
  const [persona, setPersona] = useState<Persona | null>(null)
  const [adaptiveEssay, setAdaptiveEssay] = useState<Essay | null>(null)
  const [loading, setLoading] = useState<string>('')
  const [error, setError] = useState<string>('')

  // Load initial data
  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [scholResp, studResp] = await Promise.all([
        axios.get(`${API_URL}/scholarships`),
        axios.get(`${API_URL}/students`)
      ])
      setScholarships(scholResp.data.scholarships)
      setStudents(studResp.data.students)
    } catch (err) {
      setError('Failed to load data. Make sure backend is running!')
    }
  }

  // Analyze scholarship
  const analyzeScholarship = async () => {
    setLoading('Analyzing scholarship personality...')
    setError('')
    try {
      const resp = await axios.post(`${API_URL}/analyze-scholarship?scholarship_id=${selectedScholarship}`)
      setPersona(resp.data.persona)
      setLoading('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze scholarship')
      setLoading('')
    }
  }

  // Generate essay
  const generateEssay = async () => {
    if (!persona) {
      await analyzeScholarship()
    }

    setLoading('Generating adaptive essay with AI...')
    setError('')
    try {
      const resp = await axios.post(`${API_URL}/generate-essay`, {
        scholarship_id: selectedScholarship,
        student_id: selectedStudent,
        essay_type: 'adaptive'
      })
      setAdaptiveEssay(resp.data.essay)
      setLoading('')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate essay')
      setLoading('')
    }
  }

  // Helper: Get color for trait
  const getTraitColor = (trait: string) => {
    const colors: Record<string, string> = {
      Academics: '#3b82f6',
      Leadership: '#8b5cf6',
      Community: '#10b981',
      Innovation: '#f59e0b',
      FinancialNeed: '#ef4444',
      Research: '#06b6d4'
    }
    return colors[trait] || '#6b7280'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            🎓 ScholarLens AI - Demo
          </h1>
          <a
            href="/landing.html"
            className="text-sm text-slate-600 hover:text-blue-600 transition"
          >
            ← Back to Home
          </a>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Loading Display */}
        {loading && (
          <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-700">
            <div className="flex items-center gap-3">
              <div className="animate-spin h-5 w-5 border-2 border-blue-600 border-t-transparent rounded-full"></div>
              <span>{loading}</span>
            </div>
          </div>
        )}

        {/* Selection Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold mb-6">Step 1: Select Scholarship & Student</h2>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
            {/* Scholarship Selector */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Scholarship
              </label>
              <select
                value={selectedScholarship}
                onChange={(e) => setSelectedScholarship(Number(e.target.value))}
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {scholarships.map(s => (
                  <option key={s.id} value={s.id}>
                    {s.name} (${s.amount?.toLocaleString()})
                  </option>
                ))}
              </select>
              {scholarships.find(s => s.id === selectedScholarship) && (
                <p className="mt-2 text-sm text-slate-600">
                  {scholarships.find(s => s.id === selectedScholarship)?.description.substring(0, 150)}...
                </p>
              )}
            </div>

            {/* Student Selector */}
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Student Profile
              </label>
              <select
                value={selectedStudent}
                onChange={(e) => setSelectedStudent(Number(e.target.value))}
                className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {students.map(s => (
                  <option key={s.id} value={s.id}>
                    {s.name} (GPA: {s.gpa})
                  </option>
                ))}
              </select>
              {students.find(s => s.id === selectedStudent) && (
                <p className="mt-2 text-sm text-slate-600">
                  {students.find(s => s.id === selectedStudent)?.goals}
                </p>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={analyzeScholarship}
              disabled={!!loading}
              className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              1️⃣ Analyze Scholarship
            </button>
            <button
              onClick={generateEssay}
              disabled={!!loading}
              className="flex-1 bg-purple-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              2️⃣ Generate Essay
            </button>
          </div>
        </div>

        {/* Persona Display */}
        {persona && (
          <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 animate-fadeIn">
            <h2 className="text-2xl font-bold mb-6">📊 Scholarship Persona</h2>

            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 mb-6">
              <h3 className="text-xl font-bold text-slate-800 mb-2">{persona.persona_name}</h3>
              <p className="text-slate-600 italic mb-4">💬 Tone: {persona.tone}</p>
              <p className="text-sm text-slate-700">{persona.rationale}</p>
            </div>

            {/* Trait Weights */}
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-700 mb-3">Trait Weights</h4>
              {Object.entries(persona.weights).map(([trait, weight]) => (
                weight > 0 && (
                  <div key={trait}>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="font-medium">{trait}</span>
                      <span className="text-slate-600">{(weight * 100).toFixed(0)}%</span>
                    </div>
                    <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{
                          width: `${weight * 100}%`,
                          backgroundColor: getTraitColor(trait)
                        }}
                      ></div>
                    </div>
                  </div>
                )
              ))}
            </div>
          </div>
        )}

        {/* Essay Display */}
        {adaptiveEssay && (
          <div className="bg-white rounded-2xl shadow-lg p-8 animate-fadeIn">
            <h2 className="text-2xl font-bold mb-6">✍️ Generated Essay</h2>

            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex justify-between items-center">
                <span className="font-semibold text-green-800">Overall Alignment Score</span>
                <span className="text-2xl font-bold text-green-600">
                  {(adaptiveEssay.overall_alignment * 100).toFixed(0)}%
                </span>
              </div>
            </div>

            {/* Essay Paragraphs */}
            <div className="space-y-6">
              {adaptiveEssay.essay.map((para, idx) => (
                <div key={idx} className="border-l-4 pl-6 py-4" style={{ borderColor: getTraitColor(para.focus) }}>
                  <div className="flex items-center gap-3 mb-2">
                    <span className="inline-block px-3 py-1 text-xs font-semibold rounded-full" style={{
                      backgroundColor: `${getTraitColor(para.focus)}20`,
                      color: getTraitColor(para.focus)
                    }}>
                      {para.focus}
                    </span>
                    <span className="text-sm text-slate-500">
                      Alignment: {(para.alignment_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="text-slate-700 leading-relaxed mb-2">{para.paragraph}</p>
                  <p className="text-sm text-slate-500 italic">💡 {para.reason}</p>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className="mt-6 p-4 bg-slate-50 rounded-lg">
              <h4 className="font-semibold text-slate-700 mb-2">📝 Analysis Summary</h4>
              <p className="text-sm text-slate-600">{adaptiveEssay.summary}</p>
            </div>
          </div>
        )}

        {/* CTA when no results */}
        {!persona && !adaptiveEssay && !loading && (
          <div className="text-center py-20">
            <h3 className="text-3xl font-bold text-slate-800 mb-4">
              Ready to see the magic? ✨
            </h3>
            <p className="text-slate-600 mb-8">
              Select a scholarship and student, then click "Generate Essay"
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-sm text-slate-600">
          <p>Built with ❤️ for Agentiiv Hackathon | Powered by Claude AI</p>
        </div>
      </footer>
    </div>
  )
}

export default App