import React, { useState, useEffect } from 'react';
import { Link, useOutletContext } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/client';
import {
  Sparkles,
  TrendingUp,
  Award,
  Flame,
  CheckCircle2,
  Clock,
  ArrowRight,
  BookOpen,
  Bot,
  HelpCircle,
  AlertTriangle,
  Play,
  CheckSquare,
} from 'lucide-react';
import { Card, ProgressBar, Spinner, Badge } from '../components/ui/Kit';

const StatCard = ({ label, icon: Icon, tone, value, sub, barValue }) => {
  const toneMap = {
    ocean: { icon: 'bg-ocean-500 text-white', bar: 'ocean' },
    meadow: { icon: 'bg-meadow-500 text-white', bar: 'meadow' },
    sun: { icon: 'bg-sun-500 text-white', bar: 'sun' },
    berry: { icon: 'bg-berry-500 text-white', bar: 'berry' },
  };
  const t = toneMap[tone];
  return (
    <Card className="flex flex-col justify-between">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-bold text-ink-soft">{label}</span>
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${t.icon}`}>
          <Icon className="w-5 h-5" strokeWidth={2.3} />
        </div>
      </div>
      <div className="text-3xl font-display font-bold text-ink">{value}</div>
      {barValue !== undefined && <ProgressBar value={barValue} tone={t.bar} className="mt-3" height="h-2.5" />}
      {sub && <p className="text-sm text-ink-faint mt-2">{sub}</p>}
    </Card>
  );
};

const QuickAction = ({ to, icon: Icon, label, tone }) => {
  const toneMap = {
    ocean: 'bg-ocean-100 text-ocean-600',
    meadow: 'bg-meadow-100 text-meadow-600',
    berry: 'bg-berry-100 text-berry-600',
    sun: 'bg-sun-100 text-sun-600',
  };
  return (
    <Link
      to={to}
      className="p-4 bg-paper rounded-2xl border-2 border-ink/[0.06] hover:border-ocean-500/40 transition flex flex-col items-center text-center gap-2"
    >
      <div className={`w-11 h-11 rounded-2xl flex items-center justify-center ${toneMap[tone]}`}>
        <Icon className="w-5 h-5" strokeWidth={2.3} />
      </div>
      <span className="text-sm font-bold text-ink">{label}</span>
    </Link>
  );
};

export const Dashboard = () => {
  const { user } = useAuth();
  const outletCtx = useOutletContext();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [togglingItem, setTogglingItem] = useState(null);

  const fetchDashboard = async () => {
    try {
      const res = await api.get('/students/dashboard');
      setData(res.data);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const handleTogglePlanItem = async (itemId) => {
    setTogglingItem(itemId);
    try {
      await api.post(`/study-plan/item/${itemId}/toggle`);
      fetchDashboard();
    } catch (err) {
      console.error('Failed to toggle plan item:', err);
    } finally {
      setTogglingItem(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center gap-4">
          <Spinner size={36} className="text-ocean-500" />
          <p className="text-lg font-bold text-ink-soft">Getting your dashboard ready…</p>
        </div>
      </div>
    );
  }

  const studentName = data?.student_name || user?.name || 'Student';

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-ocean-600 rounded-3xl p-6 sm:p-8 text-white relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/15 text-white text-sm font-bold mb-3">
            <Sparkles className="w-4 h-4 text-gold-400" />
            Your plan updates as you learn
          </div>
          <h1 className="text-2xl sm:text-3xl font-display font-bold">
            {getGreeting()}, {studentName} 👋
          </h1>
          <p className="mt-2 text-base text-white/85 leading-relaxed">
            Here's what to focus on today. Your weak spots, quizzes, and progress are all in one place.
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Overall mastery"
          icon={Award}
          tone="ocean"
          value={`${data?.overall_mastery || 0}%`}
          barValue={data?.overall_mastery || 0}
          sub="Across all your topics"
        />
        <StatCard
          label="Quiz accuracy"
          icon={CheckCircle2}
          tone="meadow"
          value={`${data?.quiz_average || 0}%`}
          barValue={data?.quiz_average || 0}
          sub="Average quiz score"
        />
        <StatCard
          label="Study streak"
          icon={Flame}
          tone="sun"
          value={`${data?.study_streak || 1} days`}
          sub={`🔥 Total XP: ${data?.xp_points || 50}`}
        />
        <Card className="flex flex-col justify-between bg-berry-100 border-berry-100">
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-bold text-berry-600">AI predicted score</span>
            <div className="w-10 h-10 rounded-xl bg-berry-500 text-white flex items-center justify-center">
              <TrendingUp className="w-5 h-5" strokeWidth={2.3} />
            </div>
          </div>
          <div className="text-3xl font-display font-bold text-berry-600">
            {data?.predicted_score ? `${data.predicted_score}%` : 'Calibrating'}
          </div>
          <p className="text-sm font-bold text-berry-600/80 mt-2">
            Estimated range: {data?.prediction_range || '55 - 75%'}
          </p>
          <p className="text-xs text-berry-600/60 mt-1">A statistical estimate, not a guaranteed mark.</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          <Card padded={false} className="p-6 sm:p-7">
            <div className="flex items-center justify-between mb-6 pb-4 border-b-2 border-ink/[0.06]">
              <div>
                <h2 className="text-xl font-display font-bold text-ink flex items-center gap-2">
                  <CheckSquare className="w-5 h-5 text-ocean-500" />
                  Today's plan
                </h2>
                <p className="text-sm text-ink-soft mt-0.5">
                  Matched to your time and the topics you need most.
                </p>
              </div>
              <Badge tone="ocean">{data?.today_plan?.duration || 45} min total</Badge>
            </div>

            {data?.today_plan?.items && data.today_plan.items.length > 0 ? (
              <div className="space-y-3">
                {data.today_plan.items.map((item, idx) => (
                  <div
                    key={item.id || idx}
                    className={`flex items-center justify-between p-4 rounded-2xl border-2 transition ${
                      item.completed
                        ? 'bg-cream-soft border-ink/[0.04] opacity-60'
                        : 'bg-paper border-ink/[0.06] hover:border-ocean-500/30'
                    }`}
                  >
                    <div className="flex items-center gap-3.5">
                      <button
                        onClick={() => handleTogglePlanItem(item.id)}
                        disabled={togglingItem === item.id}
                        aria-label={item.completed ? 'Mark as not done' : 'Mark as done'}
                        className={`w-8 h-8 rounded-xl border-2 flex items-center justify-center transition cursor-pointer shrink-0 ${
                          item.completed
                            ? 'bg-meadow-500 border-meadow-500 text-white'
                            : 'border-ink/15 hover:border-ocean-500 bg-white'
                        }`}
                      >
                        {item.completed && <CheckCircle2 className="w-5 h-5" />}
                      </button>

                      <div>
                        <p className={`text-base font-bold text-ink ${item.completed ? 'line-through text-ink-faint' : ''}`}>
                          {item.topic_name}
                        </p>
                        <p className="text-sm text-ink-faint">{item.activity_type}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="text-sm font-semibold text-ink-faint flex items-center gap-1 hidden sm:flex">
                        <Clock className="w-4 h-4" />
                        {item.duration_minutes} min
                      </span>
                      <button
                        onClick={() => outletCtx?.onStartStudySession(item.topic_id, item.topic_name)}
                        className="w-10 h-10 flex items-center justify-center rounded-xl bg-cream-soft hover:bg-ocean-100 hover:text-ocean-600 text-ink-soft transition"
                        title="Start studying now"
                      >
                        <Play className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-base text-ink-soft">No plan yet — let's build one.</p>
                <Link
                  to="/diagnostic/1"
                  className="mt-3 inline-flex items-center gap-2 text-base font-bold text-ocean-600 hover:underline"
                >
                  Take the quick check-in <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            )}
          </Card>

          {/* Quick Action Hub */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <QuickAction to="/learning" icon={BookOpen} label="Keep learning" tone="ocean" />
            <QuickAction to="/quizzes" icon={HelpCircle} label="Take a quiz" tone="meadow" />
            <QuickAction to="/ai-tutor" icon={Bot} label="Ask AI tutor" tone="berry" />
            <QuickAction to="/study-plan" icon={CheckSquare} label="See full plan" tone="sun" />
          </div>
        </div>

        {/* Right Column: Strong & Weak Topics */}
        <div className="space-y-6">
          <Card>
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-xl bg-coral-100 text-coral-600 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <h3 className="font-display font-bold text-ink text-lg">Needs a little practice</h3>
            </div>

            {data?.weak_topics && data.weak_topics.length > 0 ? (
              <div className="space-y-2.5">
                {data.weak_topics.map((wt) => (
                  <div
                    key={wt.topic_id}
                    className="p-3.5 bg-coral-100/60 rounded-2xl flex items-center justify-between gap-2"
                  >
                    <div>
                      <p className="text-sm font-bold text-ink">{wt.topic_name}</p>
                      <p className="text-sm text-coral-600 font-semibold">Mastery: {wt.mastery_score}%</p>
                    </div>
                    <Link
                      to={`/learning/topic/${wt.topic_id}`}
                      className="px-3 py-1.5 rounded-xl bg-white text-coral-600 text-sm font-bold hover:bg-coral-100 transition shrink-0"
                    >
                      Study
                    </Link>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-base text-ink-soft py-3">
                No weak spots right now — take a few more quizzes to check the harder topics.
              </p>
            )}
          </Card>

          <Card>
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-xl bg-meadow-100 text-meadow-600 flex items-center justify-center">
                <Award className="w-5 h-5" />
              </div>
              <h3 className="font-display font-bold text-ink text-lg">You've got this down</h3>
            </div>

            {data?.strong_topics && data.strong_topics.length > 0 ? (
              <div className="space-y-2.5">
                {data.strong_topics.map((st) => (
                  <div key={st.topic_id} className="p-3.5 bg-meadow-100/60 rounded-2xl flex items-center justify-between">
                    <div>
                      <p className="text-sm font-bold text-ink">{st.topic_name}</p>
                      <p className="text-sm text-meadow-600 font-semibold">Mastery: {st.mastery_score}%</p>
                    </div>
                    <Badge tone="meadow">Strong</Badge>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-base text-ink-soft py-3">
                Take quizzes to see the topics you've mastered show up here.
              </p>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
