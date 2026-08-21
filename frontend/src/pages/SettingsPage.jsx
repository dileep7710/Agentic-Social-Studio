import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import {
  Settings,
  Save,
  CheckCircle2,
  User,
  Phone,
  Cpu,
  Shield,
  Laptop,
  Smartphone,
  LogOut,
  Trash2,
  Clock,
  Key,
  AlertTriangle
} from 'lucide-react';

export default function SettingsPage() {
  const { user, logout, logoutAll, getSessions, revokeSession, getAuditLogs, deleteAccount } = useAuth();
  const [watermark, setWatermark] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Security & Sessions State
  const [sessions, setSessions] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [sessionsLoading, setSessionsLoading] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleteConfirmText, setDeleteConfirmText] = useState('');
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchSettings();
    loadSecurityData();
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

  const loadSecurityData = async () => {
    setSessionsLoading(true);
    try {
      const [sessData, auditData] = await Promise.all([
        getSessions(),
        getAuditLogs()
      ]);
      setSessions(sessData || []);
      setAuditLogs(auditData || []);
    } catch (err) {
      console.error(err);
    } finally {
      setSessionsLoading(false);
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

  const handleRevokeSession = async (id) => {
    if (!window.confirm('Are you sure you want to log out this device?')) return;
    try {
      await revokeSession(id);
      loadSecurityData();
    } catch (err) {
      alert('Failed to revoke device session.');
    }
  };

  const handleLogoutAll = async () => {
    if (!window.confirm('Are you sure you want to log out of ALL devices? You will need to log in again.')) return;
    try {
      await logoutAll();
      window.location.href = '/login';
    } catch (err) {
      alert('Failed to log out all devices.');
    }
  };

  const handleDeleteAccount = async () => {
    if (deleteConfirmText !== 'DELETE') {
      alert('Please type DELETE in all caps to confirm.');
      return;
    }
    setDeleting(true);
    try {
      await deleteAccount();
      alert('Your account and all associated tokens, media, and data have been permanently deleted.');
      window.location.href = '/login';
    } catch (err) {
      alert('Failed to delete account.');
      setDeleting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-16">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-3xl font-extrabold text-slate-100 flex items-center gap-3">
          <span className="fantasy-title">Security & Account Settings</span>
          <span className="px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-semibold border border-cyan-500/30">
            Enterprise Security
          </span>
        </h1>
        <p className="text-sm text-slate-400">
          Manage your personal branding, active devices, AES-256-GCM token encryption, and privacy controls.
        </p>
      </div>

      {savedSuccess && (
        <div className="p-4 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-sm font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5" />
          Settings successfully updated and saved securely!
        </div>
      )}

      {/* 1. Personal Brand & Watermark */}
      <form onSubmit={handleSave} className="glass-panel p-6 space-y-6 border-indigo-500/20">
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

      {/* 2. Active Devices & Sessions */}
      <div className="glass-panel p-6 space-y-6 border-cyan-500/20">
        <div className="flex items-center justify-between pb-3 border-b border-white/10">
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-cyan-400" />
            <div>
              <h2 className="text-base font-bold text-slate-100">Active Devices & Sessions</h2>
              <p className="text-xs text-slate-400">Manage where your account is currently signed in</p>
            </div>
          </div>
          <button
            onClick={handleLogoutAll}
            className="px-4 py-2 rounded-xl text-xs font-bold text-red-400 bg-red-500/10 border border-red-500/30 hover:bg-red-500/20 flex items-center gap-1.5 transition-all"
          >
            <LogOut className="w-3.5 h-3.5" />
            Log Out of All Devices
          </button>
        </div>

        {sessionsLoading ? (
          <div className="text-xs text-slate-400 py-4 text-center">Loading active devices...</div>
        ) : sessions.length === 0 ? (
          <div className="text-xs text-slate-400 py-4 text-center">No other active devices found.</div>
        ) : (
          <div className="space-y-3">
            {sessions.map((sess) => (
              <div
                key={sess.id}
                className={`p-4 rounded-xl flex items-center justify-between border ${
                  sess.is_current
                    ? 'bg-indigo-500/10 border-indigo-500/30'
                    : 'bg-slate-900/60 border-white/5'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center text-slate-300">
                    {sess.device_info.toLowerCase().includes('mobile') || sess.device_info.toLowerCase().includes('android') || sess.device_info.toLowerCase().includes('iphone') ? (
                      <Smartphone className="w-5 h-5 text-cyan-400" />
                    ) : (
                      <Laptop className="w-5 h-5 text-indigo-400" />
                    )}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-slate-200 truncate max-w-xs">
                        {sess.device_info}
                      </span>
                      {sess.is_current && (
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                          Current Device
                        </span>
                      )}
                    </div>
                    <div className="text-xs text-slate-400 flex items-center gap-2">
                      <span>IP: {sess.ip_address || 'Localhost'}</span>
                      <span>•</span>
                      <span>Last Active: {sess.last_active || sess.created_at}</span>
                    </div>
                  </div>
                </div>

                {!sess.is_current && (
                  <button
                    onClick={() => handleRevokeSession(sess.id)}
                    className="px-3 py-1.5 rounded-lg text-xs font-semibold text-red-300 hover:bg-red-500/20 border border-red-500/20 transition-all"
                  >
                    Revoke
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 3. Security Audit Trail */}
      <div className="glass-panel p-6 space-y-4 border-purple-500/20">
        <div className="flex items-center gap-2 pb-3 border-b border-white/10">
          <Clock className="w-5 h-5 text-purple-400" />
          <h2 className="text-base font-bold text-slate-100">Security Audit Trail</h2>
        </div>

        <div className="max-h-56 overflow-y-auto space-y-2 pr-2">
          {auditLogs.length === 0 ? (
            <div className="text-xs text-slate-400 py-2">No recent audit records.</div>
          ) : (
            auditLogs.map((log) => (
              <div
                key={log.id}
                className="p-2.5 rounded-lg bg-slate-900/50 border border-white/5 flex items-center justify-between text-xs"
              >
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-indigo-300">{log.event_type}</span>
                  <span className="text-slate-400">({log.ip_address || '127.0.0.1'})</span>
                </div>
                <span className="text-slate-500">{log.timestamp}</span>
              </div>
            ))
          )}
        </div>
      </div>

      {/* 4. Danger Zone & Account Deletion */}
      <div className="glass-panel p-6 space-y-4 border-red-500/30 bg-red-950/10">
        <div className="flex items-center gap-2 pb-3 border-b border-red-500/20 text-red-400">
          <AlertTriangle className="w-5 h-5" />
          <h2 className="text-base font-bold text-red-200">Danger Zone — Permanent Account Deletion</h2>
        </div>

        <p className="text-xs text-slate-400">
          Permanently delete your account and all associated encrypted OAuth tokens, media files, post history, and active sessions. This action is irreversible.
        </p>

        <button
          onClick={() => setShowDeleteModal(true)}
          className="px-5 py-2.5 rounded-xl font-bold text-xs text-white bg-red-600 hover:bg-red-500 flex items-center gap-2 shadow-lg transition-all"
        >
          <Trash2 className="w-4 h-4" />
          Delete My Account & All Data
        </button>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-panel max-w-md w-full p-6 space-y-5 border-red-500/40 bg-slate-950">
            <div className="flex items-center gap-2 text-red-400">
              <AlertTriangle className="w-6 h-6" />
              <h3 className="text-lg font-extrabold text-white">Confirm Account Deletion</h3>
            </div>
            <p className="text-xs text-slate-300">
              This will permanently purge your account (<span className="text-white font-bold">{user?.email}</span>), all encrypted OAuth tokens, media files, and post logs.
            </p>
            <div className="space-y-1">
              <label className="text-xs font-bold text-slate-400">Type "DELETE" below to confirm:</label>
              <input
                type="text"
                value={deleteConfirmText}
                onChange={(e) => setDeleteConfirmText(e.target.value)}
                placeholder="DELETE"
                className="w-full glass-input p-2.5 text-sm uppercase font-mono"
              />
            </div>
            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteAccount}
                disabled={deleteConfirmText !== 'DELETE' || deleting}
                className="px-5 py-2 rounded-xl text-xs font-bold text-white bg-red-600 hover:bg-red-500 disabled:opacity-40 transition-all"
              >
                {deleting ? 'Purging...' : 'Permanently Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
