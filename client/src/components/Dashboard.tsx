import { useState } from "react"

export default function Dashboard() {
    const [prompt, setPrompt] = useState("")

    async function generatingImages(e: { preventDefault: () => void }) {
        e.preventDefault()

        try {
            const res = await fetch("http://127.0.0.1:8000/api/auth/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ prompt })
            })

            const data = await res.json()
            console.log(data)
        } catch (error) {
            console.error(error)
        }
    }

    return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* Top bar */}
      <header className="border-b border-zinc-800 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold tracking-tight">
          DreamFrame
        </h1>

        <div className="flex items-center gap-4">
          <button className="text-sm text-zinc-400 hover:text-zinc-200 transition">
            Gallery
          </button>
          <button className="text-sm text-zinc-400 hover:text-zinc-200 transition">
            Settings
          </button>
          <div className="w-9 h-9 rounded-full bg-zinc-800 flex items-center justify-center text-sm">
            U
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-6xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Prompt section */}
        <section className="lg:col-span-2 space-y-6">
          <div>
            <h2 className="text-lg font-medium mb-2">
              Prompt
            </h2>
            <textarea
              placeholder="Describe the image you want to generate..."
              className="w-full h-40 resize-none rounded-xl bg-zinc-900 border border-zinc-800 p-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value = {prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="flex gap-3">
              <button className="px-4 py-2 rounded-lg bg-zinc-800 text-sm hover:bg-zinc-700 transition">
                Style
              </button>
              <button className="px-4 py-2 rounded-lg bg-zinc-800 text-sm hover:bg-zinc-700 transition">
                Model
              </button>
              <button className="px-4 py-2 rounded-lg bg-zinc-800 text-sm hover:bg-zinc-700 transition">
                Settings
              </button>
            </div>

            <button onClick={generatingImages} className="px-6 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 transition font-medium">
              Generate
            </button>
          </div>
        </section>

        {/* Sidebar */}
        <aside className="space-y-6">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
            <h3 className="text-sm font-medium mb-3">
              Credits
            </h3>
            <p className="text-2xl font-semibold">
              42
            </p>
            <p className="text-xs text-zinc-400">
              Remaining generations
            </p>
          </div>

          <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-4">
            <h3 className="text-sm font-medium mb-3">
              Recent Generations
            </h3>

            <div className="grid grid-cols-3 gap-2">
              <div className="aspect-square rounded-lg bg-zinc-800" />
              <div className="aspect-square rounded-lg bg-zinc-800" />
              <div className="aspect-square rounded-lg bg-zinc-800" />
              <div className="aspect-square rounded-lg bg-zinc-800" />
              <div className="aspect-square rounded-lg bg-zinc-800" />
              <div className="aspect-square rounded-lg bg-zinc-800" />
            </div>
          </div>
        </aside>
      </main>
    </div>
    )
}