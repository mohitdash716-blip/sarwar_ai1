"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Layout, Type, Palette } from "lucide-react";

export default function ContentPage() {
  const [topic, setTopic] = useState("");
  const [type, setType] = useState("Blog Post");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!topic.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/content", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: topic,
          type: type,
          model: "GPT-4o"
        })
      });
      if (!response.ok) throw new Error("Content generation failed");
      const data = await response.json();
      setOutput(data.response);
    } catch (error) {
      console.error("Content Error:", error);
      setOutput("⚠️ An error occurred while creating your content.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-6 md:p-12 overflow-y-auto bg-white">
      <div className="max-w-4xl mx-auto space-y-12">
        <header>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
              <Sparkles className="w-5 h-5" strokeWidth={1.5} />
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Content Creator</h1>
          </div>
          <p className="text-[#86868b] text-lg font-medium leading-relaxed">
            Generate high-quality long-form content for blogs, social media, and more.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1 space-y-6">
            <div className="space-y-4">
              <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b]">Content Type</label>
              <div className="flex flex-col gap-2">
                {["Blog Post", "Tweet Thread", "Article", "Script"].map(t => (
                  <button 
                    key={t}
                    onClick={() => setType(t)}
                    className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                      type === t ? "bg-primary text-white shadow-md shadow-primary/10" : "bg-muted text-[#1d1d1f] hover:bg-black/[0.03]"
                    }`}
                  >
                    <Type className="w-4 h-4 opacity-70" />
                    <span className="text-sm font-medium">{t}</span>
                  </button>
                ))}
              </div>
            </div>

            <button 
              onClick={handleGenerate}
              disabled={loading || !topic.trim()}
              className="w-full py-4 bg-primary text-white rounded-full font-semibold flex items-center justify-center gap-2 hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-50"
            >
              {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
              Generate
            </button>
          </div>

          <div className="lg:col-span-2 space-y-6">
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b]">What's the topic?</label>
              <input
                type="text"
                className="w-full px-6 py-4 rounded-full border border-black/[0.08] focus:border-primary/30 transition-all font-medium"
                placeholder="Ex: The impact of minimalism on UX..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
            </div>

            <div className="min-h-[400px] p-8 rounded-[32px] bg-muted border border-black/[0.04] flex flex-col items-center justify-center text-center">
              {loading ? (
                <div className="flex flex-col items-center gap-4">
                  <Sparkles className="w-8 h-8 text-primary animate-pulse" />
                  <p className="text-[#86868b] font-medium italic">Creating something beautiful...</p>
                </div>
              ) : output ? (
                <div className="w-full text-left whitespace-pre-wrap font-medium leading-relaxed">
                  {output}
                </div>
              ) : (
                <div className="flex flex-col items-center gap-4 text-[#86868b]">
                  <Layout className="w-12 h-12 opacity-20" />
                  <p className="max-w-[200px] font-medium">Your generated content will appear here.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function RefreshCw({ className }: { className?: string }) {
  return (
    <svg 
      className={className} 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" height="24" 
      viewBox="0 0 24 24" fill="none" 
      stroke="currentColor" strokeWidth="2" 
      strokeLinecap="round" strokeLinejoin="round"
    >
      <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" /><path d="M21 3v5h-5" /><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" /><path d="M3 21v-5h5" />
    </svg>
  );
}
