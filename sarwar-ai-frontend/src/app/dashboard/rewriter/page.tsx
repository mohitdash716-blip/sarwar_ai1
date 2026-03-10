"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { PenTool, Sparkles, RefreshCcw } from "lucide-react";

export default function RewriterPage() {
  const [text, setText] = useState("");
  const [style, setStyle] = useState("Academic");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRewrite = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/rewrite", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: text,
          style: style,
          model: "GPT-4o"
        })
      });
      if (!response.ok) throw new Error("Rewrite failed");
      const data = await response.json();
      setOutput(data.response);
    } catch (error) {
      console.error("Rewrite Error:", error);
      setOutput("⚠️ An error occurred while rewriting your content.");
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
              <RefreshCcw className="w-5 h-5" strokeWidth={1.5} />
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Content Rewriter</h1>
          </div>
          <p className="text-[#86868b] text-lg font-medium leading-relaxed">
            Transform your writing into any style while preserving the original meaning.
          </p>
        </header>

        <section className="space-y-8">
          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b] ml-1">Original Content</label>
            <textarea
              className="w-full h-48 p-6 rounded-[24px] border border-black/[0.08] focus:border-primary/30 transition-all resize-none text-[15px] leading-relaxed"
              placeholder="Enter text to rewrite..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
          </div>

          <div className="flex flex-col md:flex-row gap-6 items-end">
            <div className="flex-1 space-y-2 w-full">
              <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b] ml-1">Target Style</label>
              <div className="flex flex-wrap gap-2">
                {["Academic", "Witty", "Direct", "Poetic", "Corporate"].map(s => (
                  <button 
                    key={s}
                    onClick={() => setStyle(s)}
                    className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                      style === s ? "bg-primary text-white" : "bg-muted text-[#1d1d1f] hover:bg-black/[0.03]"
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
            <button 
              onClick={handleRewrite}
              disabled={loading || !text.trim()}
              className="px-10 py-4 bg-primary text-white rounded-full font-semibold flex items-center justify-center gap-2 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 shadow-lg shadow-primary/20"
            >
              {loading ? <Sparkles className="w-5 h-5 animate-spin" /> : <RefreshCcw className="w-5 h-5" />}
              Rewrite Content
            </button>
          </div>
        </section>

        {output && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-8 rounded-[28px] bg-muted border border-black/[0.04] text-[16px] leading-relaxed font-medium"
          >
            {output}
          </motion.div>
        )}
      </div>
    </div>
  );
}
