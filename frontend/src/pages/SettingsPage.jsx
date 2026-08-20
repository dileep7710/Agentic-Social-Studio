import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Settings, Save, CheckCircle2, User, Phone, Cpu, Database, Shield } from 'lucide-react';

export default function SettingsPage() {
  const [watermark, setWatermark] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const res = await axios.get('/api/settings');
      setWatermark(res.data.watermark_name || '');
      setPhone(res.data.whatsapp_phone || '');
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSavedSuccess(false);

    try {
      await axios.post('/api/settings', {
        watermark_name: watermark,
        whatsapp_phone: phone
      });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error(err);
      alert('Failed to save settings.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold text-slate-100 flex items-center gap-3">
          <span className="fantasy-title">Studio Settings</span>
          <span className="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-semibold border border-cyan-500/30">
            Configuration
          </span>
        </h1>
        <p className="text-sm text-slate-400">
          Manage your personal branding, signature watermarks, and AI engine parameters.
        </p>
      </div>

      {savedSuccess && (
        <div className="p-4 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-sm font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5" />
          Settings successfully updated and saved to SQLite database!
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSave} className="glass-panel p-6 space-y-6">
        <div className="flex items-center gap-2 pb-3 border-b border-white/10">
          <User className="w-5 h-5 text-indigo-400" />
          <h2 className="text-base font-bold text-slate-100">Personal Brand & Watermark</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Signature Watermark Name:
            </label>
            <input
              type="text"
              value={watermark}
              onChange={(e) => setWatermark(e.target.value)}
              placeholder="e.g. Dileep Yadav"
              className="w-full glass-input p-3 text-sm"
            />
            <p className="text-[11px] text-slate-500">
              Appears on generated 4K graphics in the bottom card.
            </p>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Default WhatsApp Number:
            </label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="e.g. +919876543210"
              className="w-full glass-input p-3 text-sm"
            />
            <p className="text-[11px] text-slate-500">
              Pre-fills 1-Click WhatsApp delivery links.
            </p>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 rounded-xl font-bold text-sm text-white glow-btn flex items-center gap-2 disabled:opacity-50"
        >
          <Save className="w-4 h-4" />
          {loading ? 'Saving...' : 'Save Settings'}
        </button>
      </form>

      {/* Engine & Diagnostics Info Card */}
      <div className="glass-panel p-6 space-y-4">
        <div className="flex items-center gap-2 pb-3 border-b border-white/10">
          <Cpu className="w-5 h-5 text-purple-400" />
          <h2 className="text-base font-bold text-slate-100">AI Engine & Storage Architecture</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-1">
            <div className="text-slate-400 font-semibold">AI Neural Model</div>
            <div className="text-slate-200 font-mono font-bold">Llama 3.2 (3B) Autonomous</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-1">
            <div className="text-slate-400 font-semibold">Memory Buffer</div>
            <div className="text-emerald-400 font-mono font-bold">memory.json (Persistent)</div>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-white/5 space-y-1">
            <div className="text-slate-400 font-semibold">Database Engine</div>
            <div className="text-indigo-400 font-mono font-bold">SQLite + SQLAlchemy</div>
          </div>
        </div>
      </div>
    </div>
  );
}
