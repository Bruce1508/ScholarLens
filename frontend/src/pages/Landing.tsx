import { Link } from 'react-router-dom'
import { cn } from '../utils/cn'

export function Landing() {
  return (
    <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden bg-slate-50 dark:bg-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-slate-200/80 bg-white/80 backdrop-blur-lg dark:border-slate-800/80 dark:bg-slate-900/80">
        <div className="mx-auto flex max-w-7xl items-center justify-between whitespace-nowrap px-8 py-4">
          <div className="flex items-center gap-4">
            <div className="size-8 text-blue-600">
              <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <g clipPath="url(#clip0_6_319)">
                  <path d="M8.57829 8.57829C5.52816 11.6284 3.451 15.5145 2.60947 19.7452C1.76794 23.9758 2.19984 28.361 3.85056 32.3462C5.50128 36.3314 8.29667 39.7376 11.8832 42.134C15.4698 44.5305 19.6865 45.8096 24 45.8096C28.3135 45.8096 32.5302 44.5305 36.1168 42.134C39.7033 39.7375 42.4987 36.3314 44.1494 32.3462C45.8002 28.361 46.2321 23.9758 45.3905 19.7452C44.549 15.5145 42.4718 11.6284 39.4217 8.57829L24 24L8.57829 8.57829Z" fill="currentColor"></path>
                </g>
                <defs>
                  <clipPath id="clip0_6_319">
                    <rect fill="white" height="48" width="48"></rect>
                  </clipPath>
                </defs>
              </svg>
            </div>
            <h2 className="font-bold text-xl tracking-tighter text-slate-900 dark:text-white">ScholarLens AI</h2>
          </div>
          <nav className="hidden items-center gap-8 md:flex">
            <a className="text-sm font-medium text-slate-600 transition-colors hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400" href="#">Product</a>
            <a className="text-sm font-medium text-slate-600 transition-colors hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400" href="#">How it works</a>
          </nav>
          <div className="flex items-center gap-3">
            <button className="flex h-10 cursor-pointer items-center justify-center overflow-hidden rounded-lg bg-transparent px-4 text-sm font-bold leading-normal tracking-[-0.015em] text-slate-600 transition-colors hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400">
              <span className="truncate">Sign in</span>
            </button>
            <Link
              to="/workspace"
              className="flex h-10 min-w-[84px] cursor-pointer items-center justify-center overflow-hidden rounded-lg bg-blue-600 px-4 text-sm font-bold leading-normal text-white shadow-sm transition-opacity hover:opacity-90"
            >
              <span className="truncate">Start free</span>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>
        {/* Hero Section */}
        <section className="relative overflow-hidden py-20 md:py-32">
          <div className="absolute inset-0 -z-10 bg-gradient-to-b from-blue-50 to-transparent dark:from-blue-950/20"></div>
          <div className="mx-auto flex max-w-7xl flex-col items-center gap-12 px-8">
            <div className="flex flex-col items-center gap-8 text-center">
              <div className="flex flex-col items-center gap-4">
                <h1 className="text-4xl font-bold leading-tight tracking-tighter text-slate-900 dark:text-white md:text-6xl">
                  Scholarship essays that speak the scholarship's language.
                </h1>
                <h2 className="max-w-2xl text-lg font-normal leading-relaxed text-slate-600 dark:text-slate-400">
                  Our AI analyzes scholarship criteria to generate highly targeted essays, helping you stand out and win.
                </h2>
              </div>
              <div className="flex flex-wrap justify-center gap-4">
                <Link
                  to="/workspace"
                  className="flex h-12 cursor-pointer items-center justify-center overflow-hidden rounded-lg bg-blue-600 px-6 text-base font-bold leading-normal text-white shadow-lg shadow-blue-600/30 transition-opacity hover:opacity-90"
                >
                  <span className="truncate">Get Started</span>
                </Link>
                <Link
                  to="/demo"
                  className="flex h-12 cursor-pointer items-center justify-center overflow-hidden rounded-lg border border-slate-300 bg-white px-6 text-base font-bold leading-normal text-slate-900 transition-colors hover:border-slate-400 hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-white dark:hover:border-slate-600 dark:hover:bg-slate-700"
                >
                  <span className="truncate">Try a Sample Scholarship</span>
                </Link>
              </div>
            </div>

            {/* Preview Card */}
            <div className="relative w-full max-w-4xl">
              <div className="absolute -inset-16 z-0 rounded-full bg-purple-600/20 blur-3xl"></div>
              <div className="absolute -inset-8 z-0 rounded-full bg-blue-600/30 blur-3xl"></div>
              <div className="relative w-full rounded-xl bg-white/50 p-2 shadow-2xl shadow-slate-900/10 backdrop-blur-md dark:bg-slate-900/50 dark:shadow-slate-900/50">
                <div className="h-full w-full rounded-lg bg-white p-4 dark:bg-slate-900">
                  <div className="flex items-center gap-1.5 pb-3">
                    <div className="size-3 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                    <div className="size-3 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                    <div className="size-3 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                  </div>
                  <div className="space-y-3">
                    <div className="flex items-start gap-3 rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-800/50">
                      <div className="flex size-10 items-center justify-center rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-900/30">
                        <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                        </svg>
                      </div>
                      <div>
                        <p className="font-bold text-slate-900 dark:text-white">Persona: Ambitious STEM Innovator</p>
                        <p className="text-sm text-slate-600 dark:text-slate-400">Creative | Leader | Resilient</p>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-3">
                      <div className="col-span-1 rounded-lg border border-slate-200 p-3 dark:border-slate-800">
                        <p className="mb-2 text-sm font-bold text-slate-900 dark:text-white">Trait Analysis</p>
                        <div className="aspect-square bg-gradient-to-br from-blue-100 to-purple-100 rounded dark:from-blue-900/20 dark:to-purple-900/20"></div>
                      </div>
                      <div className="col-span-2 space-y-2">
                        <div className="rounded-lg border border-slate-200 p-3 dark:border-slate-800">
                          <div className="h-3 w-4/5 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                          <div className="mt-2 h-2.5 w-full rounded-full bg-slate-200 dark:bg-slate-700"></div>
                          <div className="mt-1.5 h-2.5 w-3/4 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                        </div>
                        <div className="rounded-lg border border-slate-200 p-3 opacity-60 dark:border-slate-800">
                          <div className="h-3 w-3/5 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                          <div className="mt-2 h-2.5 w-full rounded-full bg-slate-200 dark:bg-slate-700"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 md:py-32">
          <div className="mx-auto flex max-w-7xl flex-col gap-12 px-8">
            <div className="flex flex-col gap-4 text-center">
              <h2 className="text-3xl font-bold leading-tight tracking-tighter text-slate-900 dark:text-white md:text-4xl">
                Unlock Your Winning Potential
              </h2>
              <p className="mx-auto max-w-2xl text-lg text-slate-600 dark:text-slate-400">
                ScholarLens AI combines deep analysis with powerful generation to give you a competitive edge.
              </p>
            </div>
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
              <FeatureCard
                icon="🧬"
                title="Scholarship Persona Genome"
                description="Our AI creates a detailed profile of your unique strengths, experiences, and goals to tailor every word."
              />
              <FeatureCard
                icon="💡"
                title="Winning Pattern Insights"
                description="We analyze thousands of successful essays and scholarship prompts to identify key themes and winning patterns."
              />
              <FeatureCard
                icon="🎯"
                title="Dynamic Essay Optimizer"
                description="Generate and refine essay content in real-time, ensuring it aligns perfectly with the scholarship's criteria."
              />
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-50 dark:bg-slate-900/50">
        <div className="mx-auto max-w-7xl px-8 py-16">
          <div className="flex flex-col items-center justify-between gap-8 md:flex-row">
            <div className="flex flex-col items-center gap-2 md:items-start">
              <div className="flex items-center gap-3">
                <div className="size-7 text-blue-600">
                  <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8.57829 8.57829C5.52816 11.6284 3.451 15.5145 2.60947 19.7452C1.76794 23.9758 2.19984 28.361 3.85056 32.3462C5.50128 36.3314 8.29667 39.7376 11.8832 42.134C15.4698 44.5305 19.6865 45.8096 24 45.8096C28.3135 45.8096 32.5302 44.5305 36.1168 42.134C39.7033 39.7375 42.4987 36.3314 44.1494 32.3462C45.8002 28.361 46.2321 23.9758 45.3905 19.7452C44.549 15.5145 42.4718 11.6284 39.4217 8.57829L24 24L8.57829 8.57829Z" fill="currentColor"></path>
                  </svg>
                </div>
                <h2 className="text-lg font-bold tracking-tighter text-slate-900 dark:text-white">ScholarLens AI</h2>
              </div>
              <p className="text-sm text-slate-600 dark:text-slate-400">© 2024 ScholarLens AI. All rights reserved.</p>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-6">
              <a className="text-sm font-medium text-slate-600 transition-colors hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400" href="#">Terms of Service</a>
              <a className="text-sm font-medium text-slate-600 transition-colors hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400" href="#">Privacy Policy</a>
              <a className="text-sm font-medium text-slate-600 transition-colors hover:text-blue-600 dark:text-slate-400 dark:hover:text-blue-400" href="#">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="flex flex-col gap-4 rounded-lg border border-slate-200 bg-white p-8 transition-shadow hover:shadow-xl hover:shadow-slate-900/5 dark:border-slate-800 dark:bg-slate-900 dark:hover:shadow-slate-900/20">
      <div className="flex size-12 items-center justify-center rounded-lg bg-blue-100 text-2xl dark:bg-blue-900/30">
        {icon}
      </div>
      <div className="flex flex-col gap-2">
        <h3 className="text-xl font-bold text-slate-900 dark:text-white">{title}</h3>
        <p className="text-base font-normal leading-relaxed text-slate-600 dark:text-slate-400">
          {description}
        </p>
      </div>
    </div>
  )
}