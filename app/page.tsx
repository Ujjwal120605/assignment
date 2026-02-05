"use client";

import { useState, useRef, useEffect } from "react";
import Head from "next/head";

export default function Home() {
  const [command, setCommand] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  async function runAgent(e: React.FormEvent) {
    e.preventDefault();
    if (!command.trim()) return;

    setLoading(true);
    setResponse(""); // Clear previous
    try {
      const res = await fetch("http://localhost:8000/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command }),
      });
      const data = await res.json();
      setResponse(data.message);
    } catch (err) {
      setResponse("Error: Could not connect to agent backend.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [response]);

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 md:p-8">
      {/* Header */}
      <header className="flex items-center justify-between mb-8 animate-fade-in">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500 flex items-center justify-center shadow-lg shadow-indigo-500/30">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" className="w-6 h-6">
              <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2M7.5 13A2.5 2.5 0 1 0 5 15.5 2.5 2.5 0 0 0 7.5 13m9 0a2.5 2.5 0 1 0 2.5 2.5A2.5 2.5 0 0 0 16.5 13" />
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight text-white glow-text">ASSIGN AI</h1>
            <p className="text-xs text-indigo-200 font-medium tracking-wide opacity-80">ANDROID AUTOMATION AGENT</p>
          </div>
        </div>
        <div className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          SYSTEM ONLINE
        </div>
      </header>

      {/* Main Display - Terminal Style */}
      <main className="flex-1 overflow-hidden flex flex-col gap-6 animate-fade-in" style={{ animationDelay: "0.1s" }}>

        {/* Output Console */}
        <div className="flex-1 glass-panel rounded-2xl p-6 overflow-y-auto font-mono text-sm relative" ref={scrollRef}>
          <div className="absolute top-0 left-0 w-full h-8 bg-gradient-to-b from-slate-900/50 to-transparent pointer-events-none sticky z-10" />

          {!response && !loading && (
            <div className="h-full flex flex-col items-center justify-center text-slate-500 gap-4">
              <div className="w-16 h-16 rounded-full bg-slate-800/50 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 opacity-50">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
                </svg>
              </div>
              <p>Awaiting Command...</p>
            </div>
          )}

          {loading && (
            <div className="text-indigo-400 animate-pulse">
              &gt; Processing command...
              <br />
              &gt; analyzing_intent...
              <br />
              &gt; planning_steps...
            </div>
          )}

          {response && (
            <div className="space-y-4">
              <div className="text-slate-400 border-b border-slate-700/50 pb-2 mb-4">
                &gt; Command Executed
              </div>
              <pre className="whitespace-pre-wrap text-emerald-300 leading-relaxed">
                {response}
              </pre>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="mb-4">
          <form onSubmit={runAgent} className="relative group">
            <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
            <div className="relative flex items-center glass-panel rounded-xl p-2 gap-2">
              <input
                id="cmd"
                className="flex-1 bg-transparent border-none outline-none text-white px-4 py-3 placeholder-slate-500 text-lg"
                placeholder="What should I do? (e.g. Open ChatGPT and ask 'Hello')"
                value={command}
                onChange={(e) => setCommand(e.target.value)}
                autoComplete="off"
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-lg font-semibold transition-all shadow-lg shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {loading ? (
                  <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <>Run</>
                )}
              </button>
            </div>
          </form>
        </div>

      </main>

      {/* Footer */}
      <footer className="text-center text-slate-600 text-xs py-2">
        Assign AI v1.0 • Connected to LocalHost:8000
      </footer>
    </div>
  );
}
