import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import {
  Share2, Instagram, Facebook, Linkedin, MessageCircle, Sparkles,
  CheckCircle2, XCircle, AlertCircle, Upload, Film, Image as ImageIcon,
  Download, Plus, Trash2, CheckSquare, Square, ShieldCheck
} from 'lucide-react';

export default function SocialDashboard() {
  const { user } = useAuth();
  const [sourceType, setSourceType] = useState('ai');
  const [caption, setCaption] = useState('Today I learned how Agentic AI builds autonomous multi-account workflows.');
  const [whatsappPhone, setWhatsappPhone] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploadedMediaData, setUploadedMediaData] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [publishResult, setPublishResult] = useState(null);

  // Multi-Account States
  const [accounts, setAccounts] = useState([]);
  const [selectedAccountIds, setSelectedAccountIds] = useState([]);
  const [showAddAccountModal, setShowAddAccountModal] = useState(false);
  const [newAccPlatform, setNewAccPlatform] = useState('instagram');
  const [newAccName, setNewAccName] = useState('');
  const [newAccId, setNewAccId] = useState('');
  const [newAccToken, setNewAccToken] = useState('');
  const [addingAccount, setAddingAccount] = useState(false);

  // Fetch connected accounts on load
  const fetchAccounts = async () => {
    try {
      const res = await axios.get('/api/social/accounts');
      setAccounts(res.data);
      // Default: select all active accounts
      setSelectedAccountIds(res.data.map(a => a.id));
    } catch (err) {
      console.error('Error fetching accounts:', err);
    }
  };

  useEffect(() => {
    fetchAccounts();
  }, []);

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

  const handleToggleAccount = (id) => {
    if (selectedAccountIds.includes(id)) {
      setSelectedAccountIds(selectedAccountIds.filter(x => x !== id));
    } else {
      setSelectedAccountIds([...selectedAccountIds, id]);
    }
  };

  const handleSelectAll = () => {
    if (selectedAccountIds.length === accounts.length) {
      setSelectedAccountIds([]);
    } else {
      setSelectedAccountIds(accounts.map(a => a.id));
    }
  };

  const handleAddAccount = async (e) => {
    e.preventDefault();
    if (!newAccName.trim() || !newAccId.trim()) {
      alert('Please enter account name and ID/Phone.');
      return;
    }

    setAddingAccount(true);
    try {
      await axios.post('/api/social/accounts', {
        platform: newAccPlatform,
        platform_account_name: newAccName,
        platform_account_id: newAccId,
        access_token: newAccToken
      });
      setNewAccName('');
      setNewAccId('');
      setNewAccToken('');
      setShowAddAccountModal(false);
      await fetchAccounts();
    } catch (err) {
      console.error(err);
      alert('Failed to connect account.');
    } finally {
      setAddingAccount(false);
    }
  };

  const handleDeleteAccount = async (id, name) => {
    if (!window.confirm(`Are you sure you want to disconnect ${name}?`)) return;
    try {
      await axios.delete(`/api/social/accounts/${id}`);
      await fetchAccounts();
    } catch (err) {
      console.error(err);
      alert('Failed to disconnect account.');
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
        is_video: sourceType === 'upload' ? uploadedMediaData?.is_video : false,
        account_ids: selectedAccountIds.length > 0 ? selectedAccountIds : null
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

  const getPlatformIcon = (platform) => {
    switch (platform?.toLowerCase()) {
      case 'instagram':
        return <Instagram className="w-4 h-4 text-pink-400" />;
      case 'facebook':
        return <Facebook className="w-4 h-4 text-blue-400" />;
      case 'linkedin':
        return <Linkedin className="w-4 h-4 text-cyan-400" />;
      case 'whatsapp':
        return <MessageCircle className="w-4 h-4 text-emerald-400" />;
      default:
        return <Share2 className="w-4 h-4 text-indigo-400" />;
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold text-slate-100 flex items-center gap-3">
          <span className="fantasy-title">Multi-Account 1-Click Social Studio</span>
          <span className="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold border border-indigo-500/30">
            Multi-Account Partial-Success Engine
          </span>
        </h1>
        <p className="text-sm text-slate-400">
          Connect multiple Instagram, Facebook, LinkedIn & WhatsApp accounts, select desired targets, and publish across all in 1-Click with complete account isolation.
        </p>
      </div>

      {/* Connected Accounts Manager */}
      <div className="glass-panel p-6 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 pb-3 border-b border-white/10">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <h2 className="text-base font-bold text-slate-100">
              Connected Social Accounts ({accounts.length})
            </h2>
          </div>

          <div className="flex items-center gap-3">
            {accounts.length > 0 && (
              <button
                onClick={handleSelectAll}
                className="px-3 py-1.5 rounded-lg bg-slate-800 text-xs font-medium text-slate-300 hover:text-white border border-white/10 flex items-center gap-1.5"
              >
                {selectedAccountIds.length === accounts.length ? (
                  <>
                    <CheckSquare className="w-3.5 h-3.5 text-indigo-400" /> Deselect All
                  </>
                ) : (
                  <>
                    <Square className="w-3.5 h-3.5 text-slate-400" /> Select All ({accounts.length})
                  </>
                )}
              </button>
            )}

            <button
              onClick={() => setShowAddAccountModal(true)}
              className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 text-white text-xs font-bold flex items-center gap-1.5 shadow-md hover:opacity-95"
            >
              <Plus className="w-3.5 h-3.5" /> Connect New Account
            </button>
          </div>
        </div>

        {/* Accounts Grid */}
        {accounts.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 pt-1">
            {accounts.map((acc) => {
              const isSelected = selectedAccountIds.includes(acc.id);
              return (
                <div
                  key={acc.id}
                  onClick={() => handleToggleAccount(acc.id)}
                  className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? 'bg-indigo-500/15 border-indigo-500/50 shadow-md shadow-indigo-500/10'
                      : 'bg-slate-900/40 border-white/5 opacity-60 hover:opacity-90'
                  }`}
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center">
                      {getPlatformIcon(acc.platform)}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-bold text-slate-200 truncate">{acc.platform_account_name}</p>
                      <p className="text-[11px] text-slate-400 capitalize flex items-center gap-1">
                        <span>{acc.platform}</span>
                        <span>•</span>
                        <span className="text-emerald-400 font-mono text-[10px]">Active</span>
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => {}}
                      className="rounded border-slate-700 text-indigo-500 focus:ring-indigo-400"
                    />
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteAccount(acc.id, acc.platform_account_name);
                      }}
                      className="p-1 rounded text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition-all"
                      title="Disconnect Account"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="p-4 rounded-xl bg-slate-900/40 border border-dashed border-white/10 text-center space-y-2">
            <p className="text-xs text-slate-400">No social accounts connected yet.</p>
            <p className="text-[11px] text-slate-500">
              Click <strong>"Connect New Account"</strong> above to add multiple Instagram, Facebook, LinkedIn or WhatsApp accounts.
            </p>
          </div>
        )}
      </div>

      {/* Connect Account Modal */}
      {showAddAccountModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel max-w-md w-full p-6 space-y-4 border-indigo-500/30">
            <div className="flex items-center justify-between pb-2 border-b border-white/10">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <Plus className="w-4 h-4 text-indigo-400" /> Connect Social Account
              </h3>
              <button
                onClick={() => setShowAddAccountModal(false)}
                className="text-slate-400 hover:text-white text-xs font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleAddAccount} className="space-y-3">
              <div>
                <label className="text-xs font-bold text-slate-300">Platform:</label>
                <select
                  value={newAccPlatform}
                  onChange={(e) => setNewAccPlatform(e.target.value)}
                  className="w-full glass-input p-2.5 text-xs mt-1"
                >
                  <option value="instagram">Instagram Account</option>
                  <option value="facebook">Facebook Business Page</option>
                  <option value="linkedin">LinkedIn Profile / Page</option>
                  <option value="whatsapp">WhatsApp Business / Contact</option>
                </select>
              </div>

              <div>
                <label className="text-xs font-bold text-slate-300">Account / Page Name:</label>
                <input
                  type="text"
                  value={newAccName}
                  onChange={(e) => setNewAccName(e.target.value)}
                  placeholder="e.g. @dileep_personal or Tech Page"
                  className="w-full glass-input p-2.5 text-xs mt-1"
                  required
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-300">Platform ID / Phone / URN:</label>
                <input
                  type="text"
                  value={newAccId}
                  onChange={(e) => setNewAccId(e.target.value)}
                  placeholder="e.g. 17841448994358440 or +917710278967"
                  className="w-full glass-input p-2.5 text-xs mt-1"
                  required
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-300">Access Token (Optional for API):</label>
                <input
                  type="password"
                  value={newAccToken}
                  onChange={(e) => setNewAccToken(e.target.value)}
                  placeholder="Paste account token..."
                  className="w-full glass-input p-2.5 text-xs mt-1"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowAddAccountModal(false)}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-slate-800 text-slate-300 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={addingAccount}
                  className="px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-md disabled:opacity-50"
                >
                  {addingAccount ? 'Connecting...' : 'Save & Connect'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

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

      {/* Creator & Live Dispatch Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Content Editor */}
        <div className="glass-panel p-6 space-y-5">
          <div className="flex items-center gap-2 pb-3 border-b border-white/10">
            <Share2 className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-slate-100">Content & Broadcast Config</h2>
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
              WhatsApp Fallback Phone (Optional):
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
            className="w-full py-4 rounded-xl font-bold text-sm text-white glow-btn flex items-center justify-center gap-2 shadow-lg disabled:opacity-50"
          >
            {loading ? (
              <>
                <Sparkles className="w-4 h-4 animate-spin" />
                Broadcasting to {selectedAccountIds.length} Connected Accounts...
              </>
            ) : (
              <>
                <Share2 className="w-4 h-4" />
                🚀 ONE CLICK PUBLISH TO {selectedAccountIds.length} SELECTED ACCOUNTS
              </>
            )}
          </button>
        </div>

        {/* Right: Live Preview & Granular Execution Results */}
        <div className="glass-panel p-6 space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <h2 className="text-base font-bold text-slate-100">Live Multi-Account Execution Stream</h2>
            {publishResult && (
              <span className={`px-2.5 py-1 rounded-full text-xs font-bold border ${
                publishResult.overall_status === 'SUCCESS'
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                  : publishResult.overall_status === 'PARTIAL_SUCCESS'
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/30'
                  : 'bg-rose-500/20 text-rose-300 border-rose-500/30'
              }`}>
                {publishResult.overall_status}
              </span>
            )}
          </div>

          {publishResult ? (
            <div className="space-y-4">
              {/* Media preview */}
              {publishResult.media_url && (
                <div className="relative group rounded-xl overflow-hidden border border-white/10 max-h-48 bg-black flex items-center justify-center">
                  {publishResult.is_video ? (
                    <video controls src={publishResult.media_url} className="max-h-48 w-full object-contain" />
                  ) : (
                    <img
                      src={publishResult.media_url}
                      alt="Prepared Graphic"
                      className="max-h-48 w-full object-contain"
                    />
                  )}
                  <a
                    href={publishResult.media_url}
                    target="_blank"
                    rel="noreferrer"
                    className="absolute bottom-2 right-2 px-2.5 py-1 rounded-lg bg-black/70 text-white text-[11px] font-semibold flex items-center gap-1 backdrop-blur-md"
                  >
                    <Download className="w-3 h-3" /> 4K View
                  </a>
                </div>
              )}

              {/* Granular Per-Account Result Badges */}
              <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
                <p className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                  Account Execution Results ({publishResult.success_count}/{publishResult.total_accounts} Succeeded):
                </p>

                {publishResult.platforms?.map((p, idx) => (
                  <div
                    key={idx}
                    className={`p-3 rounded-xl border flex items-center justify-between text-xs ${
                      p.status === 'SUCCESS'
                        ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-200'
                        : p.status === 'ACTION_REQUIRED'
                        ? 'bg-blue-500/10 border-blue-500/30 text-blue-200'
                        : 'bg-rose-500/10 border-rose-500/30 text-rose-200'
                    }`}
                  >
                    <div className="flex items-center gap-2.5 min-w-0">
                      {getPlatformIcon(p.platform)}
                      <div className="min-w-0">
                        <p className="font-bold truncate">{p.account_name}</p>
                        <p className="text-[10px] opacity-80 truncate">{p.message || (p.post_id ? `Post ID: ${p.post_id}` : p.status)}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      {p.status === 'SUCCESS' && (
                        <span className="flex items-center gap-1 text-emerald-400 font-bold">
                          <CheckCircle2 className="w-4 h-4" /> Success
                        </span>
                      )}
                      {p.status === 'ACTION_REQUIRED' && p.action_url && (
                        <a
                          href={p.action_url}
                          target="_blank"
                          rel="noreferrer"
                          className="px-2.5 py-1 rounded bg-blue-600 text-white font-bold hover:bg-blue-500"
                        >
                          1-Click Open
                        </a>
                      )}
                      {p.status === 'FAILED' && (
                        <span className="flex items-center gap-1 text-rose-400 font-bold">
                          <XCircle className="w-4 h-4" /> Failed
                        </span>
                      )}
                    </div>
                  </div>
                ))}
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
                    Click "ONE CLICK PUBLISH" to broadcast across all selected accounts.
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
