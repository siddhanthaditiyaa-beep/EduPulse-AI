import React, { useState, useEffect } from 'react';
import { useOutletContext, Link } from 'react-router-dom';
import api from '../api/client';
import { CalendarCheck, CheckCircle2, Clock, Play, Award, Sparkles } from 'lucide-react';
import confetti from 'canvas-confetti';
import { Card, PageHeader, ProgressBar, Badge } from '../components/ui/Kit';

export const StudyPlan = () => {
  const outletCtx = useOutletContext();
  const [plan, setPlan] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [togglingId, setTogglingId] = useState(null);

  const fetchPlanAndRecs = async () => {
    try {
      const planRes = await api.get('/study-plan');
      setPlan(planRes.data);

      const recRes = await api.get('/performance/recommendations');
      setRecommendations(recRes.data);
    } catch (err) {
      console.error('Failed to load study plan:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlanAndRecs();
  }, []);

  const handleToggleItem = async (itemId) => {
    setTogglingId(itemId);
    try {
      const res = await api.post(`/study-plan/item/${itemId}/toggle`);
      if (res.data.completed) {
        confetti({ particleCount: 50, spread: 50, origin: { y: 0.7 } });
      }
      fetchPlanAndRecs();
    } catch (err) {
      console.error('Failed to toggle plan item:', err);
    } finally {
      setTogglingId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-8 h-8 border-4 border-ocean-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <PageHeader
        eyebrowIcon={CalendarCheck}
        title="Study Plan"
        subtitle="Built around your time and your weakest topics — check things off as you go."
      />

      <Card className="p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b-2 border-ink/[0.06]">
          <div>
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ocean-100 text-ocean-600 text-sm font-bold mb-2">
              <Sparkles className="w-4 h-4" /> Adjusts to your pace
            </div>
            <h2 className="text-xl font-display font-bold text-ink">{plan?.title || 'Daily Learning Plan'}</h2>
            <p className="text-sm text-ink-soft mt-0.5">{plan?.description}</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2.5 bg-cream-soft rounded-2xl text-right">
              <span className="text-sm font-bold text-ink-faint block">Total time</span>
              <span className="text-base font-bold text-ocean-600">{plan?.duration || 45} min</span>
            </div>
            <div className="px-4 py-2.5 bg-meadow-100 rounded-2xl text-right">
              <span className="text-sm font-bold text-meadow-600 block">Done</span>
              <span className="text-base font-bold text-meadow-600">
                {plan?.completed_count}/{plan?.total_count}
              </span>
            </div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-base font-bold text-ink-soft mb-2">
            <span>Today's progress</span>
            <span>{plan?.progress_percentage || 0}%</span>
          </div>
          <ProgressBar value={plan?.progress_percentage || 0} tone="meadow" />
        </div>

        <div className="space-y-3 pt-2">
          {plan?.items && plan.items.length > 0 ? (
            plan.items.map((it, idx) => (
              <div
                key={it.id || idx}
                className={`flex items-center justify-between p-4 sm:p-5 rounded-2xl border-2 transition gap-3 flex-wrap ${
                  it.completed ? 'bg-cream-soft border-ink/[0.04] opacity-60' : 'bg-paper border-ink/[0.06] hover:border-ocean-500/30'
                }`}
              >
                <div className="flex items-center gap-3.5">
                  <button
                    onClick={() => handleToggleItem(it.id)}
                    disabled={togglingId === it.id}
                    aria-label={it.completed ? 'Mark as not done' : 'Mark as done'}
                    className={`w-8 h-8 rounded-xl border-2 flex items-center justify-center transition cursor-pointer shrink-0 ${
                      it.completed ? 'bg-meadow-500 border-meadow-500 text-white' : 'border-ink/15 hover:border-ocean-500 bg-white'
                    }`}
                  >
                    {it.completed && <CheckCircle2 className="w-5 h-5" />}
                  </button>

                  <div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className={`text-base font-bold text-ink ${it.completed ? 'line-through text-ink-faint' : ''}`}>
                        {it.topic_name}
                      </h3>
                      {it.priority === 'high' && !it.completed && <Badge tone="coral">Priority</Badge>}
                    </div>
                    <p className="text-sm text-ink-faint mt-0.5">{it.activity_type}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-sm font-semibold text-ink-faint flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {it.duration_minutes} min
                  </span>
                  <button
                    onClick={() => outletCtx?.onStartStudySession(it.topic_id, it.topic_name)}
                    className="w-10 h-10 flex items-center justify-center rounded-xl bg-cream-soft hover:bg-ocean-100 hover:text-ocean-600 text-ink-soft transition cursor-pointer"
                    title="Start studying now"
                  >
                    <Play className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-6 text-ink-soft text-base">
              No tasks yet — take a quick check-in to build your plan.
            </div>
          )}
        </div>
      </Card>

      <Card className="p-6 sm:p-8 space-y-4">
        <div className="flex items-center gap-2.5 pb-2">
          <Award className="w-6 h-6 text-ocean-500" />
          <h2 className="text-lg font-display font-bold text-ink">Why we picked these</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map((r) => (
            <div key={r.id} className="p-4 rounded-2xl bg-cream-soft flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-1.5 gap-2 flex-wrap">
                  <span className="text-base font-bold text-ink">{r.topic_name}</span>
                  <Badge tone={r.priority === 'high' ? 'coral' : 'ocean'}>{r.priority} priority</Badge>
                </div>
                <p className="text-sm text-ink-soft leading-relaxed">{r.reason}</p>
              </div>

              <div className="mt-4 pt-3 border-t-2 border-ink/[0.06] flex items-center justify-end">
                <Link to={`/learning/topic/${r.topic_id}`} className="text-sm font-bold text-ocean-600 hover:text-ocean-700 transition">
                  Review this topic →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
