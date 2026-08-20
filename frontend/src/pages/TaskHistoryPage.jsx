import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { History, Search, Eye, CheckCircle2, Globe, Calculator, Clock, Share2, Sparkles } from 'lucide-react';

export default function TaskHistoryPage() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTask, setSelectedTask] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const res = await axios.get('/api/tasks');
      setTasks(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredTasks = tasks.filter(t => 
    t.task.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (t.result && t.result.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-100 flex items-center gap-3">
            <span className="fantasy-title">Task History & Logs</span>
            <span className="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 text-xs font-semibold border border-amber-500/30">
              Audit Trails
            </span>
          </h1>
          <p className="text-sm text-slate-400">
            Review past agent executions, plans, tools used, and final synthesized outputs.
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            placeholder="Search past tasks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full glass-input pl-10 pr-4 py-2.5 text-xs"
          />
        </div>
      </div>

      {/* Task Table */}
      <div className="glass-panel overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">
            <Sparkles className="w-6 h-6 animate-spin mx-auto mb-2 text-indigo-400" />
            Loading task history logs...
          </div>
        ) : filteredTasks.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            No past tasks found. Run your first goal from the Agent Assistant dashboard!
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 uppercase font-bold border-b border-white/10">
                <tr>
                  <th className="p-4">ID</th>
                  <th className="p-4">Task Description</th>
                  <th className="p-4">Tools Used</th>
                  <th className="p-4">Status</th>
                  <th className="p-4">Date / Time</th>
                  <th className="p-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-slate-300">
                {filteredTasks.map((t) => (
                  <tr key={t.id} className="hover:bg-white/[0.02] transition-colors">
                    <td className="p-4 font-mono text-slate-500">#{t.id}</td>
                    <td className="p-4 font-semibold text-slate-200 max-w-xs truncate">
                      {t.task}
                    </td>
                    <td className="p-4">
                      <div className="flex flex-wrap gap-1">
                        {t.tools_used && t.tools_used.length > 0 ? (
                          t.tools_used.map((tool, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-mono text-[10px]"
                            >
                              {tool}
                            </span>
                          ))
                        ) : (
                          <span className="text-slate-500 text-[10px]">Planner only</span>
                        )}
                      </div>
                    </td>
                    <td className="p-4">
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-bold text-[10px]">
                        <CheckCircle2 className="w-3 h-3" />
                        {t.status}
                      </span>
                    </td>
                    <td className="p-4 text-slate-400 font-mono">{t.created_at}</td>
                    <td className="p-4 text-right">
                      <button
                        onClick={() => setSelectedTask(t)}
                        className="px-3 py-1.5 rounded-lg bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 font-semibold inline-flex items-center gap-1 transition-colors"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Task Inspection Modal */}
      {selectedTask && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="glass-panel max-w-2xl w-full p-6 space-y-5 max-h-[85vh] overflow-y-auto border-indigo-500/40">
            <div className="flex items-center justify-between pb-3 border-b border-white/10">
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-400" />
                Task #{selectedTask.id} Inspection
              </h2>
              <button
                onClick={() => setSelectedTask(null)}
                className="w-8 h-8 rounded-lg bg-white/10 hover:bg-white/20 text-slate-300 flex items-center justify-center font-bold text-sm"
              >
                ✕
              </button>
            </div>

            <div>
              <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">User Task</label>
              <p className="text-sm font-semibold text-slate-200 mt-1 bg-slate-900/60 p-3 rounded-xl border border-white/5">
                {selectedTask.task}
              </p>
            </div>

            {selectedTask.plan && (
              <div>
                <label className="text-xs font-bold text-amber-400 uppercase tracking-wider">Generated Plan</label>
                <p className="text-xs font-mono text-slate-300 mt-1 bg-slate-950/70 p-3.5 rounded-xl border border-white/5 whitespace-pre-line leading-relaxed">
                  {selectedTask.plan}
                </p>
              </div>
            )}

            <div>
              <label className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Final Output</label>
              <div className="text-xs text-slate-200 mt-1 bg-slate-950/80 p-4 rounded-xl border border-white/5 whitespace-pre-line leading-relaxed max-h-60 overflow-y-auto">
                {selectedTask.result}
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setSelectedTask(null)}
                className="px-5 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-xs font-bold text-white transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
