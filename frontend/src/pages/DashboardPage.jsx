import React, { useState } from 'react';
import axios from 'axios';
import { Send, Sparkles, Globe, Share2, Calculator, Clock, CheckCircle } from 'lucide-react';
import AgentExecutionUI from '../components/AgentExecutionUI';

const SUGGESTIONS = [
  {
    icon: <Globe className="w-4 h-4 text-cyan-400" />,
    label: "Web Research",
    query: "Search latest information about Agentic AI and give me 5 important points."
  },
  {
    icon: <Share2 className="w-4 h-4 text-pink-400" />,
    label: "Multi-Platform Broadcast",
    query: "Broadcast this quote on all platforms: Small daily improvements lead to stunning results."
  },
  {
    icon: <Calculator className="w-4 h-4 text-amber-400" />,
    label: "Math Calculation",
    query: "Calculate 50 multiplied by 20."
  },
  {
    icon: <Clock className="w-4 h-4 text-emerald-400" />,
    label: "System Clock",
    query: "What is the current time right now?"
  }
];

export default function DashboardPage() {
  const [taskInput, setTaskInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [execution, setExecution] = useState(null);
  const [error, setError] = useState('');

  const handleRunAgent = async (taskToRun) => {
    const query = (taskToRun || taskInput).trim();
    if (!query) return;

    setLoading(true);
    setError('');
    setExecution(null);

    try {
      const res = await axios.post('/api/agent/run', { task: query });
      setExecution(res.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to execute agent task. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (query) => {
    setTaskInput(query);
    handleRunAgent(query);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold text-slate-100 flex items-center gap-3">
          <span className="fantasy-title">Agentic AI Assistant</span>
          <span className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold border border-indigo-500/30">
            Llama 3.2 Autonomous Engine
          </span>
        </h1>
        <p className="text-sm text-slate-400">
          Give any goal or instruction — the agent plans, selects tools, queries web data, and executes tasks automatically.
        </p>
      </div>

      {/* Task Input Box */}
      <div className="glass-panel p-6 border-indigo-500/30 space-y-4 shadow-xl shadow-indigo-950/20">
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-300">
          Enter Your Task or Instruction:
        </label>
        
        <div className="relative">
          <textarea
            value={taskInput}
            onChange={(e) => setTaskInput(e.target.value)}
            placeholder="e.g. 'Search latest information about Agentic AI and give 5 points' or 'Broadcast this quote on all platforms...'"
            rows={3}
            className="w-full glass-input p-4 text-sm resize-none pr-32 focus:ring-2 focus:ring-indigo-500/50"
            disabled={loading}
          />
          <button
            onClick={() => handleRunAgent()}
            disabled={loading || !taskInput.trim()}
            className="absolute bottom-4 right-4 px-5 py-2.5 rounded-xl font-bold text-xs text-white glow-btn flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
          >
            {loading ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin" />
                Thinking...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Run Agent
              </>
            )}
          </button>
        </div>

        {/* Quick Suggestion Chips */}
        <div className="flex flex-wrap items-center gap-2 pt-2">
          <span className="text-xs text-slate-400 font-semibold mr-1">Quick Prompts:</span>
          {SUGGESTIONS.map((item, idx) => (
            <button
              key={idx}
              onClick={() => handleSuggestionClick(item.query)}
              disabled={loading}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/60 hover:bg-slate-800/80 border border-white/10 text-xs text-slate-300 font-medium transition-all hover:border-indigo-500/40"
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-sm flex items-center gap-2">
          ⚠️ {error}
        </div>
      )}

      {/* Execution Results Visualizer */}
      <AgentExecutionUI execution={execution} loading={loading} />
    </div>
  );
}
