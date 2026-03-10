"use client";

import { motion } from "framer-motion";
import { ArrowRight, Sparkles, MessageSquare, FileText, Mail, PenTool } from "lucide-react";
import Link from "next/link";

export default function Home() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.2 } 
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { 
      y: 0, 
      opacity: 1,
      transition: { duration: 0.6, ease: "circOut" }
    }
  };

  const features = [
    { icon: <MessageSquare className="w-6 h-6" strokeWidth={1.5} />, title: "Intelligent Chat", desc: "Interact with GPT-4, Claude, and Gemini in a single, refined conversation." },
    { icon: <FileText className="w-6 h-6" strokeWidth={1.5} />, title: "Brief Summaries", desc: "Instantly distill long documents into high-clarity insights." },
    { icon: <Mail className="w-6 h-6" strokeWidth={1.5} />, title: "Email Drafting", desc: "Craft perfectly toned professional emails with minimal effort." },
    { icon: <PenTool className="w-6 h-6" strokeWidth={1.5} />, title: "Content Rewrite", desc: "Refine and transform your writing into any desired style or voice." },
  ];

  return (
    <div className="min-h-screen bg-[#fbfbfd] text-[#1d1d1f] flex flex-col items-center selection:bg-primary/20 mesh-gradient">
      {/* Navbar Overlay */}
      <nav className="fixed top-0 w-full z-50 glass px-6 py-4 flex items-center justify-between max-w-7xl mx-auto backdrop-blur-md">
        <div className="flex items-center gap-2 group cursor-pointer">
          <Sparkles className="text-primary w-6 h-6 transition-transform group-hover:rotate-12" strokeWidth={1.5} />
          <span className="font-semibold text-xl tracking-tight">Sarwar AI</span>
        </div>
        <Link href="/dashboard/chat" className="text-sm font-medium hover:text-primary transition-colors">
          Go to App
        </Link>
      </nav>

      {/* Hero Section */}
      <main className="flex-1 w-full max-w-5xl px-6 pt-40 pb-32 flex flex-col items-center">
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="flex flex-col items-center text-center"
        >
          <motion.div 
            variants={itemVariants}
            className="mb-8 px-4 py-1.5 rounded-full bg-white/50 border border-black/[0.05] text-xs font-semibold tracking-wider text-[#86868b] uppercase flex items-center gap-2"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            Everything is better in one place
          </motion.div>

          <motion.h1 
            variants={itemVariants}
            className="text-6xl md:text-[84px] font-bold tracking-[-0.03em] leading-[1.05] mb-8"
          >
            One interface for <br />
            <span className="text-primary">multiple AI models.</span>
          </motion.h1>

          <motion.p 
            variants={itemVariants}
            className="text-xl md:text-2xl text-[#86868b] max-w-2xl mb-12 font-medium leading-relaxed"
          >
            Experience the world's most capable models in a premium, 
            calm, and intuitive workspace designed by humans.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-5">
            <Link href="/dashboard/chat">
              <button className="px-10 py-4 bg-primary text-white rounded-full font-semibold text-lg hover:scale-[1.02] active:scale-[0.98] transition-all shadow-[0_10px_30px_-10px_rgba(0,122,255,0.4)]">
                Start Chatting
              </button>
            </Link>
            <Link href="#features">
              <button className="px-10 py-4 bg-white text-[#1d1d1f] border border-black/[0.08] rounded-full font-semibold text-lg hover:bg-zinc-50 transition-all">
                Explore Tools
              </button>
            </Link>
          </motion.div>
        </motion.div>

        {/* Feature Highlights */}
        <div id="features" className="w-full mt-40 grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -5, boxShadow: "0 20px 40px rgba(0,0,0,0.05)" }}
              className="bg-white p-10 rounded-[28px] border border-black/[0.04] transition-all flex flex-col items-start gap-4"
            >
              <div className="w-12 h-12 rounded-2xl bg-primary/5 flex items-center justify-center text-primary">
                {feature.icon}
              </div>
              <h3 className="text-2xl font-semibold tracking-tight">{feature.title}</h3>
              <p className="text-[#86868b] text-lg leading-relaxed font-medium">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </main>

      <footer className="w-full py-12 px-6 border-t border-black/[0.05] flex flex-col items-center gap-4 text-[#86868b] text-sm">
        <p>© {new Date().getFullYear()} Sarwar AI. Simply better.</p>
        <div className="flex gap-6">
          <span className="hover:text-[#1d1d1f] cursor-pointer transition-colors">Privacy</span>
          <span className="hover:text-[#1d1d1f] cursor-pointer transition-colors">Terms</span>
        </div>
      </footer>
    </div>
  );
}
