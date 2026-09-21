import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import { Award, Flame, CheckCircle2, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Card, PageHeader, Button } from '../components/ui/Kit';

export const Profile = () => {
  const { user, updateUserData, logout } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState(null);
  const [educationLevel, setEducationLevel] = useState('');
  const [learningGoal, setLearningGoal] = useState('');
  const [dailyTime, setDailyTime] = useState(45);
  const [difficulty, setDifficulty] = useState('medium');
  const [saving, setSaving] = useState(false);
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get('/students/profile');
        setProfile(res.data);
        setEducationLevel(res.data.education_level);
        setLearningGoal(res.data.learning_goal);
        setDailyTime(res.data.daily_study_target);
        setDifficulty(res.data.preferred_difficulty);
      } catch (err) {
        console.error('Failed to load profile:', err);
      }
    };
    fetchProfile();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSavedSuccess(false);
    try {
      const res = await api.put('/students/profile', {
        education_level: educationLevel,
        learning_goal: learningGoal,
        daily_study_target: parseInt(dailyTime, 10),
        preferred_difficulty: difficulty,
      });
      setProfile(res.data);
      updateUserData({ profile: res.data });
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
    } catch (err) {
      console.error('Failed to update profile:', err);
    } finally {
      setSaving(false);
    }
  };

  const badges = profile?.badges_json ? JSON.parse(profile.badges_json) : ['Welcome Pioneer'];

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <PageHeader title="My Profile" subtitle="Your details, achievements, and study preferences." />

      <Card className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-ocean-500 text-white flex items-center justify-center font-display font-bold text-2xl shrink-0">
            {user?.name?.charAt(0)?.toUpperCase() || 'S'}
          </div>
          <div>
            <h2 className="text-xl font-display font-bold text-ink">{user?.name}</h2>
            <p className="text-sm text-ink-faint mt-0.5">{user?.email}</p>
            <div className="flex items-center gap-3 mt-2 text-sm font-bold flex-wrap">
              <span className="text-sun-600 flex items-center gap-1">
                <Flame className="w-4 h-4 fill-sun-500" strokeWidth={0} /> {profile?.streak_days || 1} day streak
              </span>
              <span className="text-ink-faint">•</span>
              <span className="text-berry-600 flex items-center gap-1">
                <Award className="w-4 h-4" /> {profile?.xp_points || 50} XP
              </span>
            </div>
          </div>
        </div>

        <Button
          variant="danger"
          icon={LogOut}
          size="sm"
          className="self-start sm:self-auto"
          onClick={() => {
            logout();
            navigate('/login');
          }}
        >
          Sign out
        </Button>
      </Card>

      <Card className="space-y-4">
        <h3 className="text-lg font-display font-bold text-ink flex items-center gap-2">
          <Award className="w-5 h-5 text-sun-500" />
          Badges you've earned
        </h3>
        <div className="flex flex-wrap gap-3">
          {badges.map((b, idx) => (
            <div key={idx} className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-sun-100 text-sun-600 text-sm font-bold">
              <Award className="w-4 h-4" />
              <span>{b}</span>
            </div>
          ))}
          <div className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-cream-soft text-ink-faint text-sm font-semibold">
            <span>🔒 Finish 5 quizzes to unlock "Quiz Master"</span>
          </div>
        </div>
      </Card>

      <Card className="space-y-6">
        <h3 className="text-lg font-display font-bold text-ink pb-3 border-b-2 border-ink/[0.06]">
          Learning preferences
        </h3>

        {savedSuccess && (
          <div className="p-4 rounded-2xl bg-meadow-100 text-meadow-600 text-base font-bold flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5" />
            Saved! Your settings have been updated.
          </div>
        )}

        <form onSubmit={handleSave} className="space-y-6">
          <div>
            <label className="block text-base font-bold text-ink mb-2">Education level</label>
            <input
              type="text"
              value={educationLevel}
              onChange={(e) => setEducationLevel(e.target.value)}
              className="w-full p-3.5 bg-cream-soft border-2 border-ink/10 rounded-2xl text-base font-medium focus:outline-hidden focus:border-ocean-500"
            />
          </div>

          <div>
            <label className="block text-base font-bold text-ink mb-2">Main learning goal</label>
            <input
              type="text"
              value={learningGoal}
              onChange={(e) => setLearningGoal(e.target.value)}
              className="w-full p-3.5 bg-cream-soft border-2 border-ink/10 rounded-2xl text-base font-medium focus:outline-hidden focus:border-ocean-500"
            />
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-base font-bold text-ink">Daily study time</label>
              <span className="text-sm font-bold text-ocean-600 bg-ocean-50 px-2.5 py-1 rounded-lg">
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
          </div>

          <div>
            <label className="block text-base font-bold text-ink mb-2">Starting difficulty</label>
            <select
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
              className="w-full p-3.5 bg-cream-soft border-2 border-ink/10 rounded-2xl text-base font-medium focus:outline-hidden focus:border-ocean-500 cursor-pointer"
            >
              <option value="easy">Easy — start with basics</option>
              <option value="medium">Medium — standard pace</option>
              <option value="hard">Hard — push me</option>
            </select>
          </div>

          <div className="pt-4 flex justify-end">
            <Button type="submit" loading={saving}>
              {saving ? 'Saving…' : 'Save changes'}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
