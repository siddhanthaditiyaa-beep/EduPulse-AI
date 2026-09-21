import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  BookOpen,
  Bot,
  HelpCircle,
  CalendarCheck,
  LineChart,
  User,
  GraduationCap,
  Flame,
  Award,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Sidebar = ({ isOpen, onClose }) => {
  const { user } = useAuth();
  const profile = user?.profile;

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'My Learning', path: '/learning', icon: BookOpen },
    { name: 'AI Tutor', path: '/ai-tutor', icon: Bot, badge: 'New' },
    { name: 'Quizzes', path: '/quizzes', icon: HelpCircle },
    { name: 'Study Plan', path: '/study-plan', icon: CalendarCheck },
    { name: 'My Progress', path: '/progress', icon: LineChart },
    { name: 'Profile', path: '/profile', icon: User },
  ];

  return (
    <>
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 z-40 bg-ink/40 backdrop-blur-xs lg:hidden"
        />
      )}

      <aside
        className={`fixed top-0 left-0 z-40 h-screen w-72 bg-paper border-r-2 border-ink/[0.06] transition-transform duration-200 ease-in-out flex flex-col ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="h-20 px-6 flex items-center gap-3 border-b-2 border-ink/[0.06]">
          <div className="w-11 h-11 rounded-2xl bg-ocean-500 flex items-center justify-center text-white shadow-[0_3px_0_0_rgba(35,76,107,0.5)] shrink-0">
            <GraduationCap className="w-6 h-6" strokeWidth={2.2} />
          </div>
          <div className="min-w-0">
            <h1 className="text-lg font-display font-bold text-ink leading-tight truncate">EduPulse AI</h1>
            <p className="text-sm font-semibold text-ink-faint truncate">Your learning buddy</p>
          </div>
        </div>

        <nav className="flex-1 px-4 py-5 space-y-2 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center justify-between px-4 py-3.5 rounded-2xl text-base font-bold transition-all ${
                    isActive
                      ? 'bg-ocean-500 text-white shadow-[0_3px_0_0_rgba(35,76,107,0.5)]'
                      : 'text-ink-soft hover:text-ink hover:bg-cream-soft'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <div className="flex items-center gap-3">
                      <Icon className="w-5 h-5" strokeWidth={2.3} />
                      <span>{item.name}</span>
                    </div>
                    {item.badge && (
                      <span
                        className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          isActive ? 'bg-white/25 text-white' : 'bg-sun-100 text-sun-600'
                        }`}
                      >
                        {item.badge}
                      </span>
                    )}
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        <div className="p-4 mx-4 mb-4 rounded-2xl bg-ocean-600 text-white">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-1.5 text-gold-400 text-sm font-bold">
              <Flame className="w-5 h-5 fill-gold-400" strokeWidth={0} />
              <span>{profile?.streak_days || 1} day streak</span>
            </div>
            <div className="flex items-center gap-1 text-white/85 text-sm font-bold">
              <Award className="w-4 h-4" />
              <span>{profile?.xp_points || 50} XP</span>
            </div>
          </div>
          <p className="text-sm text-white/75 leading-snug">
            Come back tomorrow to keep your streak going!
          </p>
        </div>

        <div className="p-4 border-t-2 border-ink/[0.06] flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-sun-100 text-sun-600 font-display font-bold text-base flex items-center justify-center shrink-0">
            {user?.name?.charAt(0)?.toUpperCase() || 'S'}
          </div>
          <div className="min-w-0">
            <p className="text-base font-bold text-ink truncate">{user?.name || 'Student'}</p>
            <p className="text-sm text-ink-faint truncate">{user?.email}</p>
          </div>
        </div>
      </aside>
    </>
  );
};
