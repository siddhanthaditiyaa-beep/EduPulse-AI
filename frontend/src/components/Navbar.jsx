import React from 'react';
import { Menu, Flame, Award, Clock, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const Navbar = ({ onOpenSidebar, onOpenStudyModal }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const profile = user?.profile;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-30 h-20 bg-paper/95 backdrop-blur-md border-b-2 border-ink/[0.06] px-4 lg:px-8 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenSidebar}
          aria-label="Open menu"
          className="lg:hidden w-11 h-11 flex items-center justify-center rounded-2xl text-ink-soft hover:text-ink hover:bg-cream-soft transition"
        >
          <Menu className="w-6 h-6" />
        </button>

        <div className="hidden sm:block">
          <span className="text-sm font-bold px-3 py-1.5 rounded-full bg-meadow-100 text-meadow-600">
            Learning mode: adaptive
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2 sm:gap-3">
        <button
          onClick={onOpenStudyModal}
          className="flex items-center gap-2 px-3.5 sm:px-4 py-2.5 rounded-2xl bg-ocean-50 hover:bg-ocean-100 text-ocean-600 font-bold text-sm transition"
          title="Track your active reading or study session"
        >
          <Clock className="w-4 h-4" />
          <span className="hidden sm:inline">Track study time</span>
        </button>

        <div className="flex items-center gap-1.5 px-3 py-2 rounded-2xl bg-sun-100 text-sun-600 text-sm font-bold">
          <Flame className="w-4 h-4 fill-sun-500" strokeWidth={0} />
          <span>{profile?.streak_days || 1}d</span>
        </div>

        <div className="hidden md:flex items-center gap-1.5 px-3 py-2 rounded-2xl bg-berry-100 text-berry-600 text-sm font-bold">
          <Award className="w-4 h-4" />
          <span>{profile?.xp_points || 50} XP</span>
        </div>

        <button
          onClick={handleLogout}
          aria-label="Log out"
          className="w-11 h-11 flex items-center justify-center rounded-2xl text-ink-faint hover:text-coral-600 hover:bg-coral-100 transition"
          title="Log out"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};
