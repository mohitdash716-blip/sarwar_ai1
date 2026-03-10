"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, User, ChevronDown, Sparkles, MessageSquare } from "lucide-react";
import { cn } from "@/lib/utils";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

const initialMessages: Message[] = [
  { id: "1", role: "assistant", content: "Hello! I'm Sarwar AI. How can I assist you today?" }
];

const models = ["GPT-4o", "Claude 3.5 Sonnet", "Gemini 1.5 Pro"];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [selectedModel, setSelectedModel] = useState(models[0]);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg: Message = { id: Date.now().toString(), role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    // Simulated AI Response
    setTimeout(() => {
      const aiMsg: Message = { 
        id: (Date.now() + 1).toString(), 
        role: "assistant", 
        content: "I've received your request about: \n\n\"" + userMsg.content + "\"\n\nHow would you like me to proceed with this?" 
      };
      setMessages(prev => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-white relative">
      {/* Chat Header */}
      <header className="h-16 px-6 border-b border-black/[0.05] flex items-center justify-between glass z-10">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
            <MessageSquare className="w-4 h-4 text-primary" />
          </div>
          <h1 className="font-semibold text-sm">New Conversation</h1>
        </div>

        <div className="relative group">
          <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-black/[0.05] hover:bg-black/[0.02] transition-all text-sm font-medium">
            {selectedModel}
            <ChevronDown className="w-4 h-4 text-[#86868b]" />
          </button>
          
          <div className="absolute right-0 mt-2 w-48 bg-white border border-black/[0.05] rounded-xl shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none group-hover:pointer-events-auto py-1">
            {models.map(m => (
              <button 
                key={m}
                onClick={() => setSelectedModel(m)}
                className="w-full text-left px-4 py-2 hover:bg-black/[0.02] text-sm font-medium"
              >
                {m}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Messages Viewport */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-4 py-8 space-y-6 scroll-smooth"
      >
        <div className="max-w-3xl mx-auto space-y-6">
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={cn(
                  "flex items-end gap-3",
                  msg.role === "user" ? "flex-row-reverse" : "flex-row"
                )}
              >
                <div className={cn(
                  "w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center",
                  msg.role === "user" ? "bg-primary text-white" : "bg-black/[0.03] text-[#1d1d1f]"
                )}>
                  {msg.role === "user" ? <User className="w-4 h-4" /> : <Sparkles className="text-primary w-4 h-4" />}
                </div>

                <div className={cn(
                  "max-w-[80%] px-4 py-3 shadow-sm",
                  msg.role === "user" 
                    ? "bg-primary text-white rounded-[20px] rounded-br-[4px]" 
                    : "bg-muted text-foreground rounded-[20px] rounded-bl-[4px]"
                )}>
                  <p className="text-[15px] leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isTyping && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center gap-2 text-[#86868b] px-12"
            >
              <div className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-[#86868b] rounded-full animate-bounce" style={{ animationDelay: "0s" }} />
                <span className="w-1.5 h-1.5 bg-[#86868b] rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                <span className="w-1.5 h-1.5 bg-[#86868b] rounded-full animate-bounce" style={{ animationDelay: "0.4s" }} />
              </div>
              <span className="text-xs font-medium italic">Sarwar is thinking...</span>
            </motion.div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 md:p-8 pt-0 z-10">
        <div className="max-w-3xl mx-auto relative group">
          <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-focus-within:opacity-30 transition-opacity" />
          <div className="relative glass border border-black/[0.08] rounded-2xl flex items-end p-2 pr-3 gap-2 shadow-sm focus-within:shadow-md transition-all">
            <textarea
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), handleSend())}
              placeholder="Message Sarwar AI..."
              className="flex-1 bg-transparent border-none focus:ring-0 resize-none py-2 px-3 text-[15px] placeholder:text-[#86868b] max-h-40"
              style={{ minHeight: "44px" }}
            />
            <button 
              onClick={handleSend}
              disabled={!input.trim()}
              className={cn(
                "w-10 h-10 rounded-xl flex items-center justify-center transition-all",
                input.trim() ? "bg-primary text-white shadow-lg shadow-primary/20" : "bg-black/[0.03] text-[#86868b]"
              )}
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          <p className="text-[10px] text-center mt-3 text-[#86868b] tracking-wide">
            Sarwar AI can make mistakes. Verify important information.
          </p>
        </div>
      </div>
    </div>
  );
}
