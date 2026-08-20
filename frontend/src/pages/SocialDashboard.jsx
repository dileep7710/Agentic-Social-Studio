import React, { useState } from 'react';
import axios from 'axios';
import { Share2, Instagram, Facebook, Linkedin, MessageCircle, Sparkles, CheckCircle2, ExternalLink, Download } from 'lucide-react';

export default function SocialDashboard() {
  const [caption, setCaption] = useState('Small daily improvements over time lead to stunning results.');
  const [whatsappPhone, setWhatsappPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [publishResult, setPublishResult] = useState(null);

  const handle1ClickBroadcast = async () => {
    if (!caption.trim()) return;
    setLoading(true);
    setPublishResult(null);

    try {
      const res = await axios.post('/api/social/publish', {
        content: caption,
        whatsapp_phone: whatsappPhone
      });
      setPublishResult(res.data);
    } catch (err) {
      console.error(err);
      alert('Broadcast dispatch failed. Please check backend server.');
    } finally {
      setLoading(false);
    }
  };

  const getEncodedUrl = (type) => {
    const text = encodeURIComponent(caption);
    const media = publishResult?.cdn_url ? encodeURIComponent(publishResult.cdn_url) : '';

    if (type === 'fb') {
      return `https://www.facebook.com/sharer/sharer.php?u=${media || 'https://dileep-ai-studio.streamlit.app'}&quote=${text}`;
    }
    if (type === 'li') {
      return `https://www.linkedin.com/sharing/share-offsite/?url=${media || 'https://dileep-ai-studio.streamlit.app'}`;
    }
    if (type === 'wa') {
      const phone = whatsappPhone.replace('+', '').trim();
      return `https://api.whatsapp.com/send?phone=${phone}&text=${text}%0A%0A📸%204K%20Graphic:%20${media}`;
    }
    return '#';
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold text-slate-100 flex items-center gap-3">
          <span className="fantasy-title">1-Click Multi-Platform Hub</span>
          <span className="px-3 py-1 rounded-full bg-pink-500/20 text-pink-300 text-xs font-semibold border border-pink-500/30">
            Multi-Channel Engine
          </span>
        </h1>
        <p className="text-sm text-slate-400">
          Create 4K aesthetic quote graphics and dispatch simultaneously across all major social networks in 1-Click.
        </p>
      </div>

      {/* Connected Platforms Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Instagram */}
        <div className="glass-panel p-5 space-y-2 border-pink-500/30">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-yellow-500 via-pink-500 to-purple-600 flex items-center justify-center text-white">
              <Instagram className="w-5 h-5" />
            </div>
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[11px] font-bold border border-emerald-500/30">
              Connected
            </span>
          </div>
          <h3 className="font-bold text-slate-100 text-sm">Instagram</h3>
          <p className="text-xs text-slate-400">Stories (24h) & Permanent Feed Posts</p>
        </div>

        {/* Facebook */}
        <div className="glass-panel p-5 space-y-2 border-blue-500/30">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white">
              <Facebook className="w-5 h-5" />
            </div>
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[11px] font-bold border border-emerald-500/30">
              Connected
            </span>
          </div>
          <h3 className="font-bold text-slate-100 text-sm">Facebook</h3>
          <p className="text-xs text-slate-400">Direct Timeline & Feed Web Share</p>
        </div>

        {/* LinkedIn */}
        <div className="glass-panel p-5 space-y-2 border-cyan-500/30">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-xl bg-blue-700 flex items-center justify-center text-white">
              <Linkedin className="w-5 h-5" />
            </div>
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[11px] font-bold border border-emerald-500/30">
              Connected
            </span>
          </div>
          <h3 className="font-bold text-slate-100 text-sm">LinkedIn</h3>
          <p className="text-xs text-slate-400">Professional Feed & Article Share</p>
        </div>

        {/* WhatsApp */}
        <div className="glass-panel p-5 space-y-2 border-emerald-500/30">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white">
              <MessageCircle className="w-5 h-5" />
            </div>
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 text-[11px] font-bold border border-emerald-500/30">
              Connected
            </span>
          </div>
          <h3 className="font-bold text-slate-100 text-sm">WhatsApp</h3>
          <p className="text-xs text-slate-400">1-Click Direct Delivery to Contacts</p>
        </div>
      </div>

      {/* Creator Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Input Form */}
        <div className="glass-panel p-6 space-y-5">
          <div className="flex items-center gap-2 pb-3 border-b border-white/10">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-slate-100">Broadcast Content Editor</h2>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Quote / Caption Text:
            </label>
            <textarea
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              rows={4}
              className="w-full glass-input p-4 text-sm resize-none"
              placeholder="Enter your inspiring thought or caption..."
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-wider text-slate-300">
              WhatsApp Target Phone (Optional):
            </label>
            <input
              type="text"
              value={whatsappPhone}
              onChange={(e) => setWhatsappPhone(e.target.value)}
              placeholder="e.g. +919876543210"
              className="w-full glass-input p-3 text-sm"
            />
          </div>

          <button
            onClick={handle1ClickBroadcast}
            disabled={loading || !caption.trim()}
            className="w-full py-3.5 rounded-xl font-bold text-sm text-white glow-btn flex items-center justify-center gap-2 shadow-lg disabled:opacity-50"
          >
            {loading ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin" />
                Generating 4K Graphic & Uploading to CDN...
              </>
            ) : (
              <>
                <Share2 className="w-4 h-4" />
                Generate & Prepare 1-Click Broadcast
              </>
            )}
          </button>
        </div>

        {/* Right: Live Graphic & Instant Share Buttons */}
        <div className="glass-panel p-6 space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <h2 className="text-base font-bold text-slate-100">Live 1-Click Dispatch Channels</h2>
            {publishResult?.cdn_url && (
              <span className="text-xs text-emerald-400 font-bold flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4" /> 4K CDN Ready
              </span>
            )}
          </div>

          {publishResult ? (
            <div className="space-y-4">
              {publishResult.cdn_url && (
                <div className="relative group rounded-xl overflow-hidden border border-white/10 max-h-56">
                  <img
                    src={publishResult.cdn_url}
                    alt="Generated 4K Graphic"
                    className="w-full h-full object-cover"
                  />
                  <a
                    href={publishResult.cdn_url}
                    target="_blank"
                    rel="noreferrer"
                    className="absolute bottom-3 right-3 px-3 py-1.5 rounded-lg bg-black/70 text-white text-xs font-semibold flex items-center gap-1.5 backdrop-blur-md hover:bg-black/90"
                  >
                    <Download className="w-3.5 h-3.5" /> Full 4K View
                  </a>
                </div>
              )}

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                <a
                  href={getEncodedUrl('li')}
                  target="_blank"
                  rel="noreferrer"
                  className="p-3 rounded-xl bg-blue-700/80 hover:bg-blue-600 text-white text-xs font-bold flex items-center justify-center gap-2 transition-all shadow-md"
                >
                  <Linkedin className="w-4 h-4" /> 1-Click LinkedIn
                </a>

                <a
                  href={getEncodedUrl('fb')}
                  target="_blank"
                  rel="noreferrer"
                  className="p-3 rounded-xl bg-blue-600/80 hover:bg-blue-500 text-white text-xs font-bold flex items-center justify-center gap-2 transition-all shadow-md"
                >
                  <Facebook className="w-4 h-4" /> 1-Click Facebook
                </a>

                <a
                  href={getEncodedUrl('wa')}
                  target="_blank"
                  rel="noreferrer"
                  className="p-3 rounded-xl bg-emerald-600/80 hover:bg-emerald-500 text-white text-xs font-bold flex items-center justify-center gap-2 transition-all shadow-md"
                >
                  <MessageCircle className="w-4 h-4" /> 1-Click WhatsApp
                </a>

                <a
                  href="https://www.instagram.com/"
                  target="_blank"
                  rel="noreferrer"
                  className="p-3 rounded-xl bg-gradient-to-r from-pink-600 to-purple-600 hover:opacity-95 text-white text-xs font-bold flex items-center justify-center gap-2 transition-all shadow-md"
                >
                  <Instagram className="w-4 h-4" /> Open Instagram
                </a>
              </div>
            </div>
          ) : (
            <div className="h-56 flex flex-col items-center justify-center text-center p-6 border-dashed border border-white/10 rounded-xl">
              <Share2 className="w-10 h-10 text-slate-600 mb-2" />
              <p className="text-sm text-slate-400 font-medium">
                Click "Generate & Prepare" on the left to create 4K visual assets and activate 1-Click share buttons.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
