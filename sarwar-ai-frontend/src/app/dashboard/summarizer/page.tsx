"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { FileText, Sparkles, Download, Copy } from "lucide-react";

export default function SummarizerPage() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSummarize = async () => {
    if (!input.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: input,
          model: "GPT-4o" // Default or could add a selector
        })
      });
      if (!response.ok) throw new Error("Summarization failed");
      const data = await response.json();
      setOutput(data.response);
    } catch (error) {
      console.error("Summarize Error:", error);
      setOutput("⚠️ An error occurred while generating the summary.");
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
              <FileText className="w-5 h-5" strokeWidth={1.5} />
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Text Summarizer</h1>
          </div>
          <p className="text-[#86868b] text-lg font-medium leading-relaxed">
            Distill long documents or articles into clear, high-fidelity insights.
          </p>
        </header>

        <section className="space-y-6">
          <div className="space-y-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b] ml-1">Input Text</label>
            <textarea
              className="w-full h-64 p-6 rounded-[24px] border border-black/[0.08] focus:ring-4 focus:ring-primary/10 focus:border-primary/30 transition-all resize-none text-[15px] leading-relaxed placeholder:text-[#86868b]"
              placeholder="Paste your text here..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </div>

          <button 
            onClick={handleSummarize}
            disabled={loading || !input.trim()}
            className="px-8 py-3.5 bg-primary text-white rounded-full font-semibold flex items-center gap-2 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:scale-100 shadow-lg shadow-primary/20"
          >
            {loading ? <Sparkles className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
            Summarize Now
          </button>
        </section>

        {output && (
          <motion.section 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-between ml-1">
              <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b]">AI Generated Summary</label>
              <div className="flex gap-2">
                <button className="p-2 rounded-lg hover:bg-black/[0.03] text-[#86868b] transition-colors"><Copy className="w-4 h-4" /></button>
                <button className="p-2 rounded-lg hover:bg-black/[0.03] text-[#86868b] transition-colors"><Download className="w-4 h-4" /></button>
              </div>
            </div>
            <div className="p-8 rounded-[28px] bg-muted border border-black/[0.04] text-[16px] leading-relaxed font-medium">
              {output}
            </div>
          </motion.section>
        )}
      </div>
    </div>
  );
}
