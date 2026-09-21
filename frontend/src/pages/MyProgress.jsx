import React, { useState, useEffect } from 'react';
import api from '../api/client';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts';
import { AlertTriangle, Layers, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Card, PageHeader, Badge, ProgressBar, Spinner } from '../components/ui/Kit';

export const MyProgress = () => {
  const [timeframe, setTimeframe] = useState('30d');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchAnalytics = async (tf = timeframe) => {
    setLoading(true);
    try {
      const res = await api.get(`/performance?timeframe=${tf}`);
      setData(res.data);
    } catch (err) {
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics(timeframe);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeframe]);

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Spinner size={32} className="text-ocean-500" />
      </div>
    );
  }

  const barTone = (score) => {
    if (score < 40) return 'coral';
    if (score < 60) return 'sun';
    if (score < 75) return 'ocean';
    return 'meadow';
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <PageHeader
          eyebrowIcon={Layers}
          title="My Progress"
          subtitle="How you're doing over time, topic by topic."
        />

        <div className="flex items-center p-1 bg-paper rounded-2xl border-2 border-ink/[0.06] self-start sm:self-auto mb-8">
          {[
            { id: '7d', label: '7 days' },
            { id: '30d', label: '30 days' },
            { id: 'all', label: 'All time' },
          ].map((tf) => (
            <button
              key={tf.id}
              onClick={() => setTimeframe(tf.id)}
              className={`px-4 py-2 rounded-xl text-sm font-bold transition cursor-pointer ${
                timeframe === tf.id ? 'bg-ocean-500 text-white' : 'text-ink-soft hover:text-ink'
              }`}
            >
              {tf.label}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <span className="text-sm font-bold text-ink-soft">Overall mastery</span>
          <div className="text-2xl sm:text-3xl font-display font-bold text-ink mt-1">{data?.overall_mastery || 0}%</div>
          <span className="text-sm text-ink-faint mt-1 block">Across all topics</span>
        </Card>

        <Card>
          <span className="text-sm font-bold text-ink-soft">Quiz average</span>
          <div className="text-2xl sm:text-3xl font-display font-bold text-meadow-600 mt-1">{data?.quiz_average || 0}%</div>
          <span className="text-sm text-ink-faint mt-1 block">{data?.total_quizzes_taken || 0} quizzes taken</span>
        </Card>

        <Card>
          <span className="text-sm font-bold text-ink-soft">Study time</span>
          <div className="text-2xl sm:text-3xl font-display font-bold text-ocean-600 mt-1">
            {Math.round((data?.total_study_minutes || 0) / 60)} hrs
          </div>
          <span className="text-sm text-ink-faint mt-1 block">{data?.total_study_minutes || 0} minutes total</span>
        </Card>

        <Card className="bg-berry-100 border-berry-100">
          <span className="text-sm font-bold text-berry-600">AI predicted score</span>
          <div className="text-2xl sm:text-3xl font-display font-bold text-berry-600 mt-1">
            {data?.predicted_score ? `${data.predicted_score}%` : 'Calibrating'}
          </div>
          <span className="text-sm font-semibold text-berry-600/80 mt-1 block">
            Estimate: {data?.prediction_range || '55 - 75%'}
          </span>
        </Card>
      </div>

      {/* Knowledge Map */}
      <Card className="p-6 sm:p-8 space-y-6">
        <div className="flex items-center justify-between pb-4 border-b-2 border-ink/[0.06] flex-wrap gap-2">
          <div>
            <div className="flex items-center gap-2">
              <Layers className="w-5 h-5 text-ocean-500" />
              <h2 className="text-lg font-display font-bold text-ink">Knowledge map</h2>
            </div>
            <p className="text-sm text-ink-soft mt-0.5">
              Topics under 60% are marked as needing focus.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {data?.topics_mastery && data.topics_mastery.map((item) => (
            <div key={item.topic_id} className="space-y-1.5">
              <div className="flex items-center justify-between text-base font-bold gap-2 flex-wrap">
                <div className="flex items-center gap-2">
                  <span className="text-ink">{item.topic_name}</span>
                  {item.needs_attention && <Badge tone="coral">Needs focus</Badge>}
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-ink-faint font-semibold text-sm hidden sm:inline">{item.mastery_level}</span>
                  <span className="text-ink font-bold">{item.mastery_score}%</span>
                </div>
              </div>
              <ProgressBar value={item.mastery_score} tone={barTone(item.mastery_score)} height="h-3.5" />
            </div>
          ))}
        </div>
      </Card>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="p-6 sm:p-7 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-display font-bold text-ink">Quiz accuracy over time</h3>
          </div>

          <div className="h-64 w-full">
            {data?.accuracy_trend && data.accuracy_trend.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data.accuracy_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e9e3d5" />
                  <XAxis dataKey="date" tick={{ fontSize: 13, fill: '#9791a8' }} />
                  <YAxis domain={[0, 100]} tick={{ fontSize: 13, fill: '#9791a8' }} />
                  <Tooltip contentStyle={{ backgroundColor: '#2a2340', borderRadius: '14px', border: 'none', color: '#fff' }} />
                  <Line type="monotone" dataKey="accuracy" stroke="#2f6690" strokeWidth={3} dot={{ r: 4, fill: '#2f6690' }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full text-base text-ink-soft text-center px-4">
                Not enough quizzes yet — take one to see your trend!
              </div>
            )}
          </div>
        </Card>

        <Card className="p-6 sm:p-7 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-display font-bold text-ink">Daily study minutes</h3>
          </div>

          <div className="h-64 w-full">
            {data?.study_time_trend && data.study_time_trend.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data.study_time_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e9e3d5" />
                  <XAxis dataKey="date" tick={{ fontSize: 13, fill: '#9791a8' }} />
                  <YAxis tick={{ fontSize: 13, fill: '#9791a8' }} />
                  <Tooltip contentStyle={{ backgroundColor: '#2a2340', borderRadius: '14px', border: 'none', color: '#fff' }} />
                  <Bar dataKey="minutes" fill="#ff8a3d" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-full text-base text-ink-soft text-center px-4">
                No study sessions logged yet in this timeframe.
              </div>
            )}
          </div>
        </Card>
      </div>

      {/* Recent Mistakes */}
      <Card className="p-6 sm:p-8 space-y-4">
        <div className="flex items-center gap-2.5 pb-2 border-b-2 border-ink/[0.06]">
          <AlertTriangle className="w-5 h-5 text-coral-500" />
          <h2 className="text-lg font-display font-bold text-ink">Recent mistakes to review</h2>
        </div>

        {data?.recent_mistakes && data.recent_mistakes.length > 0 ? (
          <div className="space-y-3">
            {data.recent_mistakes.map((m, idx) => (
              <div key={idx} className="p-4 rounded-2xl bg-coral-100/50 space-y-2">
                <div className="flex items-center justify-between text-sm flex-wrap gap-1">
                  <span className="font-bold text-ink">{m.topic_name}</span>
                  <span className="text-ink-faint">{m.date}</span>
                </div>
                <p className="text-base font-bold text-ink">{m.question}</p>
                <div className="flex flex-wrap items-center gap-4 text-sm">
                  <span className="text-coral-600 font-semibold">Your answer: <strong>{m.your_answer}</strong></span>
                  <span className="text-meadow-600 font-semibold">Correct: <strong>{m.correct_answer}</strong></span>
                </div>
                <p className="text-sm text-ink-soft bg-white p-3 rounded-xl leading-relaxed">
                  {m.explanation}
                </p>
                <div className="flex justify-end pt-1">
                  <Link
                    to={`/ai-tutor?questionId=${m.question_id}&action=explain_mistake`}
                    className="text-sm font-bold text-ocean-600 hover:text-ocean-700 inline-flex items-center gap-1.5"
                  >
                    Ask AI tutor to explain <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-6 text-base text-ink-soft">
            No recent mistakes in this timeframe — keep it up!
          </div>
        )}
      </Card>
    </div>
  );
};
