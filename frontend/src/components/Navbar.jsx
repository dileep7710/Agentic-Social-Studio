import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Sparkles, LogOut, User as UserIcon, LayoutDashboard, Share2, History, Settings } from 'lucide-react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-white/10 px-6 py-3.5 mb-6 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform">
            <Sparkles className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight fantasy-title">
              Agentic AI Omni-Studio
            </h1>
            <p className="text-xs text-slate-400 font-medium">Autonomous Multi-Platform Engine</p>
          </div>
        </Link>

        {/* Center Links for Authenticated Users */}
        {user ? (
          <nav className="hidden md:flex items-center gap-2 bg-slate-900/60 p-1.5 rounded-xl border border-white/5">
            <Link
              to="/dashboard"
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
            >
              <LayoutDashboard className="w-4 h-4 text-indigo-400" />
              Agent Assistant
            </Link>
            <Link
              to="/social"
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
            >
              <Share2 className="w-4 h-4 text-pink-400" />
              Social Studio
            </Link>
            <Link
              to="/history"
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
            >
              <History className="w-4 h-4 text-amber-400" />
              Task History
            </Link>
            <Link
              to="/settings"
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
            >
              <Settings className="w-4 h-4 text-cyan-400" />
              Settings
            </Link>
          </nav>
        ) : null}

        {/* User Right Profile / Auth CTA */}
        <div className="flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-200 text-sm font-medium">
                <UserIcon className="w-4 h-4 text-purple-400" />
                <span>{user.name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-300 border border-red-500/20 text-xs font-semibold transition-colors"
                title="Logout"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-300 hover:text-white transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 rounded-xl text-sm font-bold glow-btn text-white"
              >
                Get Started Free
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
