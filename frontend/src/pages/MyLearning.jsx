import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import { BookOpen, CheckCircle, ArrowRight, Zap, HelpCircle } from 'lucide-react';
import { Card, PageHeader, Badge, Spinner, Button } from '../components/ui/Kit';

export const MyLearning = () => {
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCurriculum = async () => {
      try {
        const subRes = await api.get('/subjects');
        setSubjects(subRes.data);
        if (subRes.data.length > 0) {
          const firstSub = subRes.data[0];
          setSelectedSubject(firstSub);
          const topRes = await api.get(`/subjects/${firstSub.id}/topics`);
          setTopics(topRes.data);
        }
      } catch (err) {
        console.error('Failed to load curriculum:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCurriculum();
  }, []);

  const handleSelectSubject = async (sub) => {
    setSelectedSubject(sub);
    setLoading(true);
    try {
      const topRes = await api.get(`/subjects/${sub.id}/topics`);
      setTopics(topRes.data);
    } catch (err) {
      console.error('Failed to load topics:', err);
    } finally {
      setLoading(false);
    }
  };

  const getMasteryTone = (score) => {
    if (score >= 90) return 'meadow';
    if (score >= 75) return 'meadow';
    if (score >= 60) return 'ocean';
    if (score >= 40) return 'sun';
    return 'coral';
  };

  const getMasteryBadgeText = (score) => {
    if (score >= 90) return 'Mastered';
    if (score >= 75) return 'Doing well';
    if (score >= 60) return 'Getting there';
    if (score >= 40) return 'Needs practice';
    return 'Just starting';
  };

  if (loading && subjects.length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Spinner size={32} className="text-ocean-500" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrowIcon={BookOpen}
        title="My Learning"
        subtitle="Your topics, notes, and how well you know each one."
      />

      {/* Subject Selector Tabs */}
      <div className="flex items-center gap-3 overflow-x-auto pb-2">
        {subjects.map((sub) => (
          <button
            key={sub.id}
            onClick={() => handleSelectSubject(sub)}
            className={`px-5 py-3 rounded-2xl text-sm font-bold shrink-0 transition cursor-pointer flex items-center gap-2 ${
              selectedSubject?.id === sub.id
                ? 'bg-ocean-500 text-white shadow-[0_3px_0_0_rgba(35,76,107,0.5)]'
                : 'bg-paper border-2 border-ink/10 text-ink-soft hover:border-ocean-500/40'
            }`}
          >
            <BookOpen className="w-4 h-4" />
            <span>{sub.name}</span>
            <span className="opacity-75">({sub.topics_count})</span>
          </button>
        ))}
      </div>

      {selectedSubject && (
        <Card className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="max-w-2xl">
            <Badge tone="ocean">Active course</Badge>
            <h2 className="text-xl font-display font-bold text-ink mt-2">{selectedSubject.name}</h2>
            <p className="text-base text-ink-soft mt-1 leading-relaxed">{selectedSubject.description}</p>
          </div>
          <Button as={Link} to={`/diagnostic/${selectedSubject.id}`} variant="soft" icon={Zap} size="sm" className="shrink-0">
            {selectedSubject.diagnostic_completed ? 'Retake check-in' : 'Take quick check-in'}
          </Button>
        </Card>
      )}

      {/* Topics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {topics.map((t, idx) => (
          <Card key={t.id} className="flex flex-col justify-between hover:border-ocean-500/30 transition">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-bold text-ink-faint">Topic {idx + 1}</span>
                <Badge tone={getMasteryTone(t.mastery_score)}>
                  {getMasteryBadgeText(t.mastery_score)} ({t.mastery_score}%)
                </Badge>
              </div>
              <h3 className="text-lg font-display font-bold text-ink mb-1">{t.name}</h3>
              <p className="text-sm text-ink-soft line-clamp-2 leading-relaxed">{t.description}</p>
            </div>

            <div className="mt-5 pt-4 border-t-2 border-ink/[0.06] flex items-center justify-between flex-wrap gap-3">
              <div className="flex items-center gap-2 text-sm text-ink-faint font-semibold">
                <CheckCircle className="w-4 h-4" />
                <span>{t.attempts} quiz attempts</span>
              </div>

              <div className="flex items-center gap-2">
                <Link
                  to={`/quizzes?topicId=${t.id}`}
                  className="px-3.5 py-2 rounded-xl bg-cream-soft hover:bg-ink/10 text-ink text-sm font-bold transition flex items-center gap-1.5"
                >
                  <HelpCircle className="w-4 h-4" /> Quiz
                </Link>
                <Link
                  to={`/learning/topic/${t.id}`}
                  className="px-3.5 py-2 rounded-xl bg-ocean-500 hover:bg-ocean-600 text-white text-sm font-bold transition flex items-center gap-1.5"
                >
                  Study <ArrowRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
