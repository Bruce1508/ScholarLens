import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import { cn } from '../../utils/cn'

interface ExtractedData {
  name: string
  email: string
  phone?: string
  gpa?: number
  skills: string[]
  education: any[]
  work_experience: any[]
  activities: string[]
  achievements: string[]
  languages: string[]
  certifications: string[]
  awards: string[]
  extraction_confidence: number
}

interface ResumeUploadProps {
  onExtracted?: (data: ExtractedData) => void
  studentId?: number
}

export function ResumeUpload({ onExtracted, studentId }: ResumeUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [extracting, setExtracting] = useState(false)
  const [extractedData, setExtractedData] = useState<ExtractedData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
        return
      }
      setFile(file)
      setError(null)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    maxFiles: 1,
    multiple: false
  })

  const handleUpload = async () => {
    if (!file || !studentId) return

    setUploading(true)
    setError(null)
    setUploadProgress(0)

    const formData = new FormData()
    formData.append('file', file)

    try {
      // Upload resume
      const uploadResponse = await axios.post(
        `http://localhost:8000/api/v1/profiles/upload-resume?student_id=${studentId}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
              setUploadProgress(progress)
            }
          }
        }
      )

      if (uploadResponse.data.success) {
        setUploading(false)
        setExtracting(true)

        // Extract profile data
        const extractResponse = await axios.post(
          `http://localhost:8000/api/v1/profiles/extract-from-resume/${studentId}`
        )

        if (extractResponse.data.success) {
          const data = extractResponse.data.data
          setExtractedData(data)
          if (onExtracted) {
            onExtracted(data)
          }
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
      setExtracting(false)
    }
  }

  const resetUpload = () => {
    setFile(null)
    setExtractedData(null)
    setError(null)
    setUploadProgress(0)
  }

  // If data is already extracted, show review UI
  if (extractedData) {
    return (
      <div className="rounded-lg border border-green-200 bg-green-50 p-6 dark:border-green-900 dark:bg-green-900/20">
        <div className="flex items-start gap-4">
          <div className="flex size-10 items-center justify-center rounded-lg bg-green-100 text-green-600 dark:bg-green-900/50">
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-green-900 dark:text-green-100">
              Resume Extracted Successfully!
            </h3>
            <p className="mt-1 text-sm text-green-700 dark:text-green-300">
              Confidence: {Math.round(extractedData.extraction_confidence * 100)}%
            </p>
            <div className="mt-4 space-y-2">
              <div className="text-sm">
                <span className="font-medium">Name:</span> {extractedData.name}
              </div>
              <div className="text-sm">
                <span className="font-medium">Email:</span> {extractedData.email}
              </div>
              {extractedData.gpa && (
                <div className="text-sm">
                  <span className="font-medium">GPA:</span> {extractedData.gpa}
                </div>
              )}
              {extractedData.skills.length > 0 && (
                <div className="text-sm">
                  <span className="font-medium">Skills:</span> {extractedData.skills.slice(0, 5).join(', ')}
                  {extractedData.skills.length > 5 && ` +${extractedData.skills.length - 5} more`}
                </div>
              )}
            </div>
            <button
              onClick={resetUpload}
              className="mt-4 text-sm font-medium text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300"
            >
              Upload a different resume
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={cn(
          "relative rounded-lg border-2 border-dashed p-8 text-center transition-colors cursor-pointer",
          isDragActive
            ? "border-blue-400 bg-blue-50 dark:border-blue-600 dark:bg-blue-900/20"
            : "border-slate-300 hover:border-slate-400 dark:border-slate-700 dark:hover:border-slate-600",
          file && "border-green-400 bg-green-50 dark:border-green-600 dark:bg-green-900/20"
        )}
      >
        <input {...getInputProps()} />

        {file ? (
          <div className="space-y-2">
            <div className="flex justify-center">
              <div className="flex size-12 items-center justify-center rounded-lg bg-green-100 text-green-600 dark:bg-green-900/50">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                </svg>
              </div>
            </div>
            <p className="font-medium text-slate-900 dark:text-white">{file.name}</p>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              {(file.size / (1024 * 1024)).toFixed(2)} MB
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="flex justify-center">
              <div className="flex size-12 items-center justify-center rounded-lg bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M13.5,16V19H10.5V16H8L12,12L16,16H13.5M13,9V3.5L18.5,9H13Z"/>
                </svg>
              </div>
            </div>
            <p className="font-medium text-slate-900 dark:text-white">
              {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
            </p>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              or click to browse (PDF only, max 10MB)
            </p>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-900 dark:bg-red-900/20">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      {/* Upload Progress */}
      {uploading && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-600 dark:text-slate-400">Uploading...</span>
            <span className="font-medium">{uploadProgress}%</span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
            <div
              className="h-full bg-blue-600 transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Extracting Indicator */}
      {extracting && (
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 dark:border-blue-900 dark:bg-blue-900/20">
          <div className="flex items-center gap-3">
            <div className="size-5 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
            <p className="text-sm text-blue-600 dark:text-blue-400">
              AI is extracting your profile data...
            </p>
          </div>
        </div>
      )}

      {/* Upload Button */}
      {file && !uploading && !extracting && studentId && (
        <button
          onClick={handleUpload}
          className="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition-opacity hover:opacity-90"
        >
          Upload and Extract Profile
        </button>
      )}

      {/* Manual Option */}
      {!file && (
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-slate-300 dark:border-slate-700" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="bg-white px-4 text-slate-600 dark:bg-slate-900 dark:text-slate-400">
              or enter manually
            </span>
          </div>
        </div>
      )}
    </div>
  )
}