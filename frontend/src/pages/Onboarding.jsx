import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import { Sparkles, GraduationCap, Target, Clock, Zap, ArrowRight } from 'lucide-react';
import { Button } from '../components/ui/Kit';

const OptionCard = ({ active, onClick, title, desc }) => (
  <button
    type="button"
    onClick={onClick}
    className={`text-left p-4 rounded-2xl border-2 transition cursor-pointer ${
      active
        ? 'border-ocean-500 bg-ocean-50'
        : 'border-ink/10 hover:border-ocean-500/40 bg-paper'
    }`}
  >
    <p className={`text-base font-bold ${active ? 'text-ocean-600' : 'text-ink'}`}>{title}</p>
    {desc && <p className="text-sm text-ink-soft mt-1">{desc}</p>}
  </button>
);

export const Onboarding = () => {
  const { user, updateUserData } = useAuth();
  const navigate = useNavigate();

  const [educationLevel, setEducationLevel] = useState('Undergraduate (B.Tech / BCA / B.Sc)');
  const [learningGoal, setLearningGoal] = useState('Semester Exam Preparation');
  const [dailyTime, setDailyTime] = useState(45);
  const [difficulty, setDifficulty] = useState('medium');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await api.put('/students/profile', {
        education_level: educationLevel,
        learning_goal: learningGoal,
        daily_study_target: parseInt(dailyTime, 10),
        preferred_difficulty: difficulty,
      });

      updateUserData({ profile: res.data });
      navigate('/diagnostic/1');
    } catch (err) {
      console.error('Failed to update student profile:', err);
      navigate('/dashboard');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-cream py-12 px-4 flex items-center justify-center">
      <div className="max-w-2xl w-full bg-paper rounded-3xl border-2 border-ink/[0.06] p-6 sm:p-12">
        <div className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sun-100 text-sun-600 text-sm font-bold mb-4">
            <Sparkles className="w-4 h-4" /> Let's set things up
          </div>
          <h2 className="text-3xl font-display font-bold text-ink">
            Welcome, {user?.name || 'Student'}! 👋
          </h2>
          <p className="mt-2 text-lg text-ink-soft">
            A few quick questions so your AI tutor can match its pace to you.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-9">
          <div>
            <label className="flex items-center gap-2 text-lg font-bold text-ink mb-3">
              <GraduationCap className="w-5 h-5 text-ocean-500" />
              What's your current education level?
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {[
                'Undergraduate (B.Tech / BCA / B.Sc)',
                'Postgraduate (M.Tech / MCA / M.Sc)',
                'Higher Secondary / High School',
                'Self-Directed / Career Transition',
              ].map((lvl) => (
                <OptionCard key={lvl} active={educationLevel === lvl} onClick={() => setEducationLevel(lvl)} title={lvl} />
              ))}
            </div>
          </div>

          <div>
            <label className="flex items-center gap-2 text-lg font-bold text-ink mb-3">
              <Target className="w-5 h-5 text-ocean-500" />
              What's your main learning goal?
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { label: 'Semester Exam Prep', desc: 'Do well in tests & viva' },
                { label: 'Campus Placements', desc: 'Crack technical interviews' },
                { label: 'Deep Conceptual Mastery', desc: 'Really understand the core ideas' },
              ].map((goal) => (
                <OptionCard key={goal.label} active={learningGoal === goal.label} onClick={() => setLearningGoal(goal.label)} title={goal.label} desc={goal.desc} />
              ))}
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="flex items-center gap-2 text-lg font-bold text-ink">
                <Clock className="w-5 h-5 text-ocean-500" />
                How much time can you study daily?
              </label>
              <span className="text-base font-bold text-ocean-600 bg-ocean-50 px-3 py-1.5 rounded-xl">
                {dailyTime} minutes
              </span>
            </div>
            <input
              type="range"
              min="15"
              max="180"
              step="15"
              value={dailyTime}
              onChange={(e) => setDailyTime(e.target.value)}
              className="w-full accent-ocean-500 cursor-pointer h-2"
            />
            <div className="flex justify-between text-sm text-ink-faint mt-1.5 font-semibold">
              <span>15 min</span>
              <span>45 min</span>
              <span>180 min</span>
            </div>
          </div>

          <div>
            <label className="flex items-center gap-2 text-lg font-bold text-ink mb-3">
              <Zap className="w-5 h-5 text-ocean-500" />
              Where should we start?
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { id: 'easy', label: 'Beginner', desc: 'Start with the basics' },
                { id: 'medium', label: 'Balanced', desc: 'Standard pace' },
                { id: 'hard', label: 'Challenging', desc: 'Push me harder' },
              ].map((diff) => (
                <OptionCard key={diff.id} active={difficulty === diff.id} onClick={() => setDifficulty(diff.id)} title={diff.label} desc={diff.desc} />
              ))}
            </div>
          </div>

          <div className="pt-6 border-t-2 border-ink/[0.06] flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-base text-ink-soft text-center sm:text-left">
              Next: a quick 8-question check-in so we know where to begin.
            </p>
            <Button type="submit" loading={submitting} iconRight={ArrowRight} size="lg" className="w-full sm:w-auto">
              {submitting ? 'Setting up…' : "Let's go"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};
