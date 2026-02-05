"use client";

import { useState, useRef, useEffect } from "react";

export default function Home() {
  const [command, setCommand] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  async function runAgent(e: React.FormEvent) {
    e.preventDefault();
    if (!command.trim()) return;

    setLoading(true);
    setResponse(null);

    try {
      const res = await fetch("http://localhost:8000/command", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data.message || "Command executed successfully");
    } catch (err) {
      setResponse(`Error: ${err instanceof Error ? err.message : "Connection failure. Make sure the backend is running on port 8000."}`);
    } finally {
      setLoading(false);
    }
  }

  const startListening = () => {
    // @ts-ignore
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setCommand(transcript);
      };

      recognition.start();
    } else {
      alert("Browser does not support speech recognition.");
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [response]);

  return (
    <div className="flex flex-col min-h-screen justify-center items-center bg-neutral-50 text-black p-4">
      {/* Compact Swiss Card */}
      <div className="w-full max-w-3xl border-2 border-black flex flex-col h-[85vh] shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">

        {/* Header */}
        <header className="border-b-2 border-black p-6 flex justify-between items-center bg-white">
          <h1 className="text-4xl font-bold tracking-tighter uppercase leading-none">
            Assign AI
          </h1>
          <div className="flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${loading ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`}></span>
            <span className="text-[10px] font-bold uppercase tracking-widest text-neutral-600">
              {loading ? 'Thinking...' : 'System Ready'}
            </span>
          </div>
        </header>

        {/* Console / Output */}
        <main
          className="flex-1 overflow-y-auto p-6 font-mono text-sm leading-relaxed bg-neutral-50 relative"
          ref={scrollRef}
        >
          {!response && !loading && (
            <div className="absolute inset-0 flex flex-col items-center justify-center opacity-20 pointer-events-none">
              <svg
                className="w-24 h-24 mb-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1"
              >
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
              </svg>
              <p className="text-xs uppercase tracking-wider font-bold">
                Enter a command to begin
              </p>
            </div>
          )}

          {loading && (
            <div className="space-y-2">
              <p className="text-green-600 animate-pulse">
                &gt; INITIALIZING AGENT...
              </p>
              <p className="text-green-600 animate-pulse [animation-delay:150ms]">
                &gt; OBSERVING SCREEN...
              </p>
              <p className="text-green-600 animate-pulse [animation-delay:300ms]">
                &gt; REASONING NEXT STEP...
              </p>
              <p className="text-green-600 animate-pulse [animation-delay:450ms]">
                &gt; EXECUTING ACTIONS...
              </p>
            </div>
          )}

          {response && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b-2 border-black">
                <span className="text-black font-bold">// EXECUTION_LOG</span>
                <span className="text-xs bg-black text-white px-2 py-0.5 font-bold">
                  COMPLETE
                </span>
              </div>
              <pre className="whitespace-pre-wrap font-medium text-neutral-800 leading-relaxed">
                {response}
              </pre>
            </div>
          )}
        </main>

        {/* Input Bar */}
        <div className="border-t-2 border-black bg-white p-4">
          <form onSubmit={runAgent} className="flex gap-0 border-2 border-black relative">
            {/* Voice Button */}
            <button
              type="button"
              onClick={startListening}
              className={`px-4 border-r-2 border-black hover:bg-neutral-100 transition-colors ${isListening ? 'bg-red-100 text-red-600 animate-pulse' : 'text-neutral-500'}`}
              title="Voice Command"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" y1="19" x2="12" y2="23" />
                <line x1="8" y1="23" x2="16" y2="23" />
              </svg>
            </button>

            <input
              className="flex-1 bg-transparent p-4 text-sm font-medium outline-none placeholder:text-neutral-400 font-sans"
              placeholder={isListening ? "Listening..." : "Type instruction... (e.g., 'Open ChatGPT and ask what is AI')"}
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              autoComplete="off"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !command.trim()}
              className="px-8 bg-black text-white text-xs font-bold uppercase tracking-wider hover:bg-neutral-800 disabled:bg-neutral-300 disabled:text-neutral-500 disabled:cursor-not-allowed transition-all duration-200 border-l-2 border-black"
            >
              {loading ? "Running" : "Run"}
            </button>
          </form>
        </div>

        {/* Footer */}
        <footer className="border-t-2 border-black p-3 text-center bg-white text-[10px] uppercase text-neutral-500 font-bold tracking-wider">
          v1.1.0 // Android Agent System
        </footer>

      </div>
    </div>
  );
}