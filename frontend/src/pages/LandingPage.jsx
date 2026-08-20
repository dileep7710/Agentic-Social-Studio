import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, Globe, Share2, Zap, Shield, Cpu, Terminal, CheckCircle2 } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="space-y-24 py-6">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-4xl mx-auto pt-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-bold tracking-wide animate-pulse">
          <Sparkles className="w-4 h-4 text-pink-400" />
          Production Full-Stack Edition
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight leading-tight">
          Supercharge Your Workflow With <br />
          <span className="fantasy-title">Autonomous Agentic AI</span>
        </h1>

        <p className="text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          From multi-step web research to 1-click multi-platform broadcasting across Instagram, LinkedIn, Facebook, and WhatsApp. Powered by Llama 3.2, real tool calling, and persistent memory.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            to="/dashboard"
            className="px-8 py-3.5 rounded-xl font-bold text-base text-white glow-btn flex items-center gap-2 shadow-xl shadow-indigo-500/30"
          >
            Launch Agent Assistant
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/social"
            className="px-6 py-3.5 rounded-xl font-semibold text-base text-slate-200 bg-white/10 hover:bg-white/15 border border-white/10 transition-colors flex items-center gap-2"
          >
            <Share2 className="w-5 h-5 text-pink-400" />
            Social Studio
          </Link>
        </div>
      </section>

      {/* Live Pipeline Architecture Visual */}
      <section className="max-w-5xl mx-auto glass-panel p-8 border-indigo-500/30">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-slate-100">End-to-End Autonomous Pipeline</h2>
          <p className="text-sm text-slate-400 mt-1">How user prompts flow from React UI through FastAPI to the existing Agent Engine</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 text-center">
          <div className="p-4 rounded-xl bg-slate-900/80 border border-white/10">
            <div className="text-2xl mb-2">👤</div>
            <div className="text-xs font-bold text-slate-200">1. User Task</div>
            <div className="text-[11px] text-slate-400 mt-1">Prompt in React UI</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-indigo-500/30">
            <div className="text-2xl mb-2">🧠</div>
            <div className="text-xs font-bold text-indigo-300">2. Llama Planner</div>
            <div className="text-[11px] text-slate-400 mt-1">Action steps planned</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-purple-500/30">
            <div className="text-2xl mb-2">🛠️</div>
            <div className="text-xs font-bold text-purple-300">3. Tool Calling</div>
            <div className="text-[11px] text-slate-400 mt-1">Search, Calc, Social</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-pink-500/30">
            <div className="text-2xl mb-2">⚡</div>
            <div className="text-xs font-bold text-pink-300">4. Live Execution</div>
            <div className="text-[11px] text-slate-400 mt-1">Results synthesized</div>
          </div>
          <div className="p-4 rounded-xl bg-slate-900/80 border border-emerald-500/30">
            <div className="text-2xl mb-2">📊</div>
            <div className="text-xs font-bold text-emerald-300">5. Dashboard UI</div>
            <div className="text-[11px] text-slate-400 mt-1">Final result & sources</div>
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="max-w-6xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-extrabold text-slate-100">Engineered For Autonomous Intelligence</h2>
          <p className="text-sm text-slate-400">Preserving 100% of the core agent engine inside a modern web SaaS experience</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-panel p-6 space-y-3">
            <div className="w-12 h-12 rounded-xl bg-cyan-500/20 text-cyan-400 flex items-center justify-center">
              <Globe className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Live Web Search</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Real-time DuckDuckGo search integration that discovers latest news, documentation, and extracts verified sources with citations.
            </p>
          </div>

          <div className="glass-panel p-6 space-y-3">
            <div className="w-12 h-12 rounded-xl bg-pink-500/20 text-pink-400 flex items-center justify-center">
              <Share2 className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">1-Click Multi-Platform</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Generate 4K aesthetic quote graphics and broadcast simultaneously across Instagram, Facebook, LinkedIn, and WhatsApp.
            </p>
          </div>

          <div className="glass-panel p-6 space-y-3">
            <div className="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center">
              <Cpu className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-slate-100">Persistent Memory</h3>
            <p className="text-sm text-slate-400 leading-relaxed">
              Conversational context retained across sessions via <code className="text-amber-300">memory.json</code> and SQLite task audit logs.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
