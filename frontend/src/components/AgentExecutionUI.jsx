import React from 'react';
import { 
  CheckCircle2, 
  Clock, 
  Globe, 
  Calculator, 
  Share2, 
  ExternalLink, 
  Copy, 
  Sparkles,
  ArrowRight,
  Database
} from 'lucide-react';

export default function AgentExecutionUI({ execution, loading }) {
  if (loading) {
    return (
      <div className="glass-panel p-8 text-center animate-pulse">
        <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center">
          <Sparkles className="w-7 h-7 text-indigo-400 animate-spin" />
        </div>
        <h3 className="text-lg font-bold text-slate-100">Agentic AI is Thinking & Planning...</h3>
        <p className="text-sm text-slate-400 mt-1">Executing Llama Planner, Tool Selection, and Search Pipelines.</p>
        
        <div className="mt-6 max-w-md mx-auto space-y-2 text-left text-xs font-mono text-slate-400">
          <div className="flex items-center gap-2 text-indigo-400">
            <span className="inline-block w-2 h-2 rounded-full bg-indigo-400 animate-ping"></span>
            Initializing conversational context...
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-slate-600"></span>
            Generating 2-5 action steps...
          </div>
          <div className="flex items-center gap-2">
            <span className="inline-block w-2 h-2 rounded-full bg-slate-600"></span>
            Calling tool functions & synthesizing response...
          </div>
        </div>
      </div>
    );
  }

  if (!execution) {
    return (
      <div className="glass-panel p-12 text-center border-dashed border-white/10">
        <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-slate-800/60 border border-white/10 flex items-center justify-center">
          <Sparkles className="w-8 h-8 text-slate-500" />
        </div>
        <h3 className="text-lg font-bold text-slate-300">No Task Executed Yet</h3>
        <p className="text-sm text-slate-500 max-w-sm mx-auto mt-1">
          Type a task in the box above or pick one of the quick suggestions to watch the agent plan and execute tools.
        </p>
      </div>
    );
  }

  const { task, plan, steps = [], tools_used = [], sources = [], result } = execution;

  const copyResult = () => {
    navigator.clipboard.writeText(result);
    alert('Copied final response to clipboard!');
  };

  return (
    <div className="space-y-6">
      {/* Execution Status Header */}
      <div className="glass-panel p-6 border-indigo-500/30 bg-gradient-to-r from-indigo-950/40 via-purple-950/30 to-slate-900/60">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-2">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Task Execution Complete
            </div>
            <h2 className="text-xl font-bold text-slate-100">{task}</h2>
          </div>

          <div className="flex items-center gap-2">
            {tools_used.map((tool, idx) => (
              <span
                key={idx}
                className="px-3 py-1 rounded-lg bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 text-xs font-semibold flex items-center gap-1.5"
              >
                {tool === 'web_search' && <Globe className="w-3.5 h-3.5 text-cyan-400" />}
                {tool === 'calculator' && <Calculator className="w-3.5 h-3.5 text-amber-400" />}
                {tool === 'get_time' && <Clock className="w-3.5 h-3.5 text-emerald-400" />}
                {(tool.includes('post') || tool.includes('broadcast')) && <Share2 className="w-3.5 h-3.5 text-pink-400" />}
                {tool}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Grid: Plan & Execution Steps */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Generated Plan */}
        <div className="glass-panel p-5 lg:col-span-1">
          <div className="flex items-center gap-2 pb-3 border-b border-white/10 mb-4">
            <div className="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-xs">
              📝
            </div>
            <h3 className="text-sm font-bold text-slate-200">Planner Action Steps</h3>
          </div>
          <div className="bg-slate-950/60 p-4 rounded-xl border border-white/5 text-xs text-slate-300 font-mono whitespace-pre-line leading-relaxed">
            {plan || "1. Direct processing of user request.\n2. Execute necessary actions."}
          </div>
        </div>

        {/* Right: Real-Time Execution Pipeline */}
        <div className="glass-panel p-5 lg:col-span-2">
          <div className="flex items-center gap-2 pb-3 border-b border-white/10 mb-4">
            <div className="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-xs">
              ⚡
            </div>
            <h3 className="text-sm font-bold text-slate-200">Execution Pipeline Trace</h3>
          </div>

          <div className="space-y-3">
            {steps.map((step, idx) => (
              <div
                key={idx}
                className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-900/60 border border-white/5 text-xs"
              >
                <div className="mt-0.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-200">{step.title}</span>
                    <span className="text-[10px] text-slate-500 font-mono">Step #{idx + 1}</span>
                  </div>
                  <p className="text-slate-400 mt-1 font-mono text-[11px] break-words line-clamp-3">
                    {step.detail}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Sources Citations (if web search was used) */}
      {sources && sources.length > 0 && (
        <div className="glass-panel p-6">
          <div className="flex items-center gap-2 pb-3 border-b border-white/10 mb-4">
            <Globe className="w-5 h-5 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-200">Verified Web Sources ({sources.length})</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {sources.map((src, i) => (
              <a
                key={i}
                href={src.url}
                target="_blank"
                rel="noreferrer"
                className="p-3.5 rounded-xl bg-slate-900/70 hover:bg-slate-800/80 border border-white/5 hover:border-cyan-500/40 transition-all block group"
              >
                <div className="flex items-center justify-between text-xs font-bold text-cyan-300 group-hover:text-cyan-200 mb-1">
                  <span className="truncate">{src.title}</span>
                  <ExternalLink className="w-3.5 h-3.5 flex-shrink-0 ml-2" />
                </div>
                <p className="text-[11px] text-slate-400 line-clamp-2">{src.summary || src.url}</p>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Final Synthesized Output Card */}
      <div className="glass-panel p-6 border-indigo-500/40 bg-gradient-to-b from-slate-900/80 to-indigo-950/40">
        <div className="flex items-center justify-between pb-3 border-b border-white/10 mb-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <h3 className="text-base font-bold text-slate-100">Final Synthesized Result</h3>
          </div>
          <button
            onClick={copyResult}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-semibold text-slate-200 transition-colors"
          >
            <Copy className="w-3.5 h-3.5" />
            Copy Result
          </button>
        </div>

        <div className="text-sm text-slate-200 font-sans whitespace-pre-line leading-relaxed bg-slate-950/70 p-5 rounded-xl border border-white/5">
          {result}
        </div>
      </div>
    </div>
  );
}
