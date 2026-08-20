import React, { useState } from 'react';
import axios from 'axios';
import { Share2, Instagram, Facebook, Linkedin, MessageCircle, Sparkles, CheckCircle2, Upload, Film, Image as ImageIcon, Download } from 'lucide-react';

export default function SocialDashboard() {
  const [sourceType, setSourceType] = useState('ai'); // 'ai' or 'upload'
  const [caption, setCaption] = useState('Today I learned how Agentic AI builds autonomous workflows.');
  const [whatsappPhone, setWhatsappPhone] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadedMediaData, setUploadedMediaData] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [publishResult, setPublishResult] = useState(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadedFile(file);
    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('/api/social/upload-file', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setUploadedMediaData(res.data);
    } catch (err) {
      console.error(err);
      alert('Failed to process custom media file.');
    } finally {
      setUploading(false);
    }
  };

  const handle1ClickBroadcast = async () => {
    if (!caption.trim()) return;
    setLoading(true);
    setPublishResult(null);

    try {
      const payload = {
        content: caption,
        whatsapp_phone: whatsappPhone,
        media_url: sourceType === 'upload' ? uploadedMediaData?.media_url : null,
        is_video: sourceType === 'upload' ? uploadedMediaData?.is_video : false
      };

      const res = await axios.post('/api/social/publish', payload);
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
      return `https://api.whatsapp.com/send?phone=${phone}&text=${text}%0A%0A📸%20Media:%20${media}`;
    }
    return '#';
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold text-slate-100 flex items-center gap-3">
          <span className="fantasy-title">Multi-Platform Studio & Story Dispatch</span>
          <span className="px-3 py-1 rounded-full bg-pink-500/20 text-pink-300 text-xs font-semibold border border-pink-500/30">
            Custom Media + AI
          </span>
        </h1>
        <p className="text-sm text-slate-400">
          Upload any photo/video from your PC or generate 4K AI visual graphics, and post to Instagram Stories, Feed, Facebook, LinkedIn, and WhatsApp in 1-Click.
        </p>
      </div>

      {/* Connected Platforms Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
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
          <p className="text-xs text-slate-400">24h Stories, Reels & Feed Posts</p>
        </div>

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
          <p className="text-xs text-slate-400">Direct Timeline & Feed Share</p>
        </div>

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
          <p className="text-xs text-slate-400">Direct Message & Status Sharing</p>
        </div>
      </div>

      {/* Media Source Selector */}
      <div className="glass-panel p-4 flex flex-wrap items-center gap-3">
        <span className="text-xs font-bold text-slate-300 uppercase tracking-wider mr-2">Media Source:</span>
        <button
          onClick={() => setSourceType('ai')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            sourceType === 'ai'
              ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30'
              : 'bg-slate-900/60 text-slate-400 hover:text-white border border-white/5'
          }`}
        >
          <Sparkles className="w-4 h-4 text-pink-300" />
          ✨ Generate 4K AI Nature Graphic
        </button>

        <button
          onClick={() => setSourceType('upload')}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
            sourceType === 'upload'
              ? 'bg-gradient-to-r from-pink-500 to-rose-600 text-white shadow-lg shadow-pink-500/30'
              : 'bg-slate-900/60 text-slate-400 hover:text-white border border-white/5'
          }`}
        >
          <Upload className="w-4 h-4 text-cyan-300" />
          📂 Upload Photo/Video from PC/Phone Folder
        </button>
      </div>

      {/* Creator Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Content Editor */}
        <div className="glass-panel p-6 space-y-5">
          <div className="flex items-center gap-2 pb-3 border-b border-white/10">
            <Share2 className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-slate-100">
              {sourceType === 'upload' ? 'Upload Custom Photo or Video' : 'AI Quote Content Editor'}
            </h2>
          </div>

          {sourceType === 'upload' && (
            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-300">
                Choose Image (.jpg, .png) or Video (.mp4) from your computer:
              </label>
              <input
                type="file"
                accept="image/png, image/jpeg, image/jpg, video/mp4"
                onChange={handleFileUpload}
                className="w-full text-xs text-slate-300 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-indigo-500/20 file:text-indigo-300 hover:file:bg-indigo-500/30 cursor-pointer"
              />
              {uploading && <p className="text-xs text-cyan-400 font-mono animate-pulse">Uploading asset to CDN...</p>}
              {uploadedFile && !uploading && (
                <p className="text-xs text-emerald-400 font-mono">✓ Loaded: {uploadedFile.name}</p>
              )}
            </div>
          )}

          <div className="space-y-2">
            <label className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Caption / Message / विचार:
            </label>
            <textarea
              value={caption}
              onChange={(e) => setCaption(e.target.value)}
              rows={4}
              className="w-full glass-input p-4 text-sm resize-none"
              placeholder="Enter caption or quote..."
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
            disabled={loading || uploading || !caption.trim()}
            className="w-full py-3.5 rounded-xl font-bold text-sm text-white glow-btn flex items-center justify-center gap-2 shadow-lg disabled:opacity-50"
          >
            {loading ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin" />
                Preparing Multi-Platform Broadcast...
              </>
            ) : (
              <>
                <Share2 className="w-4 h-4" />
                🚀 Post to Instagram Story, Feed, Facebook & WhatsApp
              </>
            )}
          </button>
        </div>

        {/* Right: Live Preview & Dispatch Buttons */}
        <div className="glass-panel p-6 space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <h2 className="text-base font-bold text-slate-100">Live Visual Asset Preview</h2>
            {publishResult?.cdn_url && (
              <span className="text-xs text-emerald-400 font-bold flex items-center gap-1">
                <CheckCircle2 className="w-4 h-4" /> Ready to Broadcast
              </span>
            )}
          </div>

          {/* Media Preview Box */}
          {publishResult ? (
            <div className="space-y-4">
              {publishResult.cdn_url && (
                <div className="relative group rounded-xl overflow-hidden border border-white/10 max-h-64 bg-black flex items-center justify-center">
                  {publishResult.is_video ? (
                    <video controls src={publishResult.cdn_url} className="max-h-64 w-full object-contain" />
                  ) : (
                    <img
                      src={publishResult.cdn_url}
                      alt="Prepared Graphic"
                      className="max-h-64 w-full object-contain"
                    />
                  )}
                  <a
                    href={publishResult.cdn_url}
                    target="_blank"
                    rel="noreferrer"
                    className="absolute bottom-3 right-3 px-3 py-1.5 rounded-lg bg-black/70 text-white text-xs font-semibold flex items-center gap-1.5 backdrop-blur-md hover:bg-black/90"
                  >
                    <Download className="w-3.5 h-3.5" /> Full HD View
                  </a>
                </div>
              )}

              {/* 1-Click Sharers */}
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
                  <Instagram className="w-4 h-4" /> Open Instagram (Story/Feed)
                </a>
              </div>
            </div>
          ) : (
            <div className="h-64 flex flex-col items-center justify-center text-center p-6 border-dashed border border-white/10 rounded-xl">
              {sourceType === 'upload' ? (
                <>
                  <Film className="w-10 h-10 text-slate-600 mb-2" />
                  <p className="text-sm text-slate-400 font-medium">
                    Upload your custom image or video file on the left and click Post!
                  </p>
                </>
              ) : (
                <>
                  <ImageIcon className="w-10 h-10 text-slate-600 mb-2" />
                  <p className="text-sm text-slate-400 font-medium">
                    Click "Post to Instagram Story, Feed & WhatsApp" on the left to generate 4K visual assets.
                  </p>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
