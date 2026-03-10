"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Mail, Sparkles, Send } from "lucide-react";

export default function EmailPage() {
  const [context, setContext] = useState("");
  const [tone, setTone] = useState("Professional");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!context.trim()) return;
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          context: context,
          tone: tone,
          model: "GPT-4o"
        })
      });
      if (!response.ok) throw new Error("Email generation failed");
      const data = await response.json();
      setOutput(data.response);
    } catch (error) {
      console.error("Email Error:", error);
      setOutput("⚠️ An error occurred while generating the email draft.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-6 md:p-12 overflow-y-auto bg-[#fbfbfd] mesh-gradient">
      <div className="max-w-4xl mx-auto space-y-12">
        <header>
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
              <Mail className="w-5 h-5" strokeWidth={1.5} />
            </div>
            <h1 className="text-3xl font-bold tracking-tight">Email Generator</h1>
          </div>
          <p className="text-[#86868b] text-lg font-medium leading-relaxed">
            Draft perfectly toned professional emails with the help of advanced AI.
          </p>
        </header>

        <section className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b] ml-1">Email Context</label>
              <textarea
                className="w-full h-40 p-5 rounded-[20px] border border-black/[0.08] focus:border-primary/30 transition-all resize-none text-[15px] leading-relaxed"
                placeholder="What is this email about?"
                value={context}
                onChange={(e) => setContext(e.target.value)}
              />
            </div>
            <div className="space-y-6">
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase tracking-wider text-[#86868b] ml-1">Tone & Voice</label>
                <div className="grid grid-cols-2 gap-2">
                  {["Professional", "Friendly", "Formal", "Casual"].map(t => (
                    <button 
                      key={t}
                      onClick={() => setTone(t)}
                      className={`px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                        tone === t ? "bg-primary text-white shadow-md" : "bg-muted text-[#1d1d1f] hover:bg-black/[0.03]"
                      }`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>
              <button 
                onClick={handleGenerate}
                disabled={loading || !context.trim()}
                className="w-full py-4 bg-primary text-white rounded-full font-semibold flex items-center justify-center gap-2 hover:scale-[1.01] active:scale-[0.99] transition-all disabled:opacity-50"
              >
                {loading ? <Sparkles className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
                Draft Email
              </button>
            </div>
          </div>
        </section>

        {output && (
          <motion.section 
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            className="p-8 rounded-[28px] bg-muted border border-black/[0.04] relative group"
          >
            <div className="whitespace-pre-wrap text-[16px] leading-relaxed font-medium">
              {output}
            </div>
            <button className="absolute top-6 right-6 p-2 rounded-xl bg-white border border-black/[0.05] opacity-0 group-hover:opacity-100 transition-opacity">
              <Send className="w-4 h-4 text-primary" />
            </button>
          </motion.section>
        )}
      </div>
    </div>
  );
}
