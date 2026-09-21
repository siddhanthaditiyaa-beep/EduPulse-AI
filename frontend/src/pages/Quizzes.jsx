import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '../api/client';
import { HelpCircle, Sparkles, Play, History } from 'lucide-react';
import { Card, PageHeader, Button, Spinner } from '../components/ui/Kit';

export const Quizzes = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const preselectedTopicId = searchParams.get('topicId');

  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(preselectedTopicId || '');
  const [difficulty, setDifficulty] = useState('medium');
  const [questionCount, setQuestionCount] = useState(5);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const topRes = await api.get('/subjects/1/topics');
        setTopics(topRes.data);
        if (!selectedTopic && topRes.data.length > 0) {
          setSelectedTopic(preselectedTopicId || topRes.data[0].id);
        }

        const histRes = await api.get('/quiz/history');
        setHistory(histRes.data);
      } catch (err) {
        console.error('Failed to load quizzes info:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [preselectedTopicId]);

  const handleStartQuiz = async () => {
    if (!selectedTopic) return;
    setGenerating(true);
    try {
      const res = await api.post('/quiz/generate', {
        topic_id: parseInt(selectedTopic, 10),
        difficulty,
        number_of_questions: parseInt(questionCount, 10),
      });

      navigate('/quiz/attempt', {
        state: { quizData: res.data, topicId: selectedTopic, difficulty },
      });
    } catch (err) {
      console.error('Failed to generate quiz:', err);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Spinner size={32} className="text-ocean-500" />
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      <PageHeader
        eyebrowIcon={HelpCircle}
        title="Quizzes"
        subtitle="Pick a topic and test yourself — questions adjust to how you're doing."
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <Card className="lg:col-span-2 p-6 sm:p-8 space-y-7">
          <div className="flex items-center gap-3 pb-4 border-b-2 border-ink/[0.06]">
            <div className="w-10 h-10 rounded-xl bg-ocean-500 text-white flex items-center justify-center shrink-0">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-display font-bold text-ink">Build your quiz</h2>
              <p className="text-sm text-ink-soft">Set it up the way you like</p>
            </div>
          </div>

          <div>
            <label className="block text-base font-bold text-ink mb-2">
              Which topic?
            </label>
            <select
              value={selectedTopic}
              onChange={(e) => setSelectedTopic(e.target.value)}
              className="w-full p-3.5 bg-cream-soft border-2 border-ink/10 rounded-2xl text-base font-semibold text-ink focus:outline-hidden focus:border-ocean-500 cursor-pointer"
            >
              {topics.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} (Mastery: {t.mastery_score}%)
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-base font-bold text-ink mb-2">
              How hard?
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { id: 'easy', label: 'Easy', desc: 'Basics' },
                { id: 'medium', label: 'Medium', desc: 'Standard' },
                { id: 'hard', label: 'Hard', desc: 'Tricky' },
              ].map((d) => (
                <button
                  type="button"
                  key={d.id}
                  onClick={() => setDifficulty(d.id)}
                  className={`p-3.5 rounded-2xl border-2 text-center transition cursor-pointer ${
                    difficulty === d.id
                      ? 'border-ocean-500 bg-ocean-50'
                      : 'border-ink/10 hover:border-ocean-500/40'
                  }`}
                >
                  <p className={`text-base font-bold ${difficulty === d.id ? 'text-ocean-600' : 'text-ink'}`}>{d.label}</p>
                  <p className="text-sm text-ink-faint mt-0.5">{d.desc}</p>
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-base font-bold text-ink">
                How many questions?
              </label>
              <span className="text-sm font-bold text-ocean-600 bg-ocean-50 px-2.5 py-1 rounded-lg">
                {questionCount}
              </span>
            </div>
            <input
              type="range"
              min="3"
              max="10"
              value={questionCount}
              onChange={(e) => setQuestionCount(e.target.value)}
              className="w-full accent-ocean-500 cursor-pointer h-2"
            />
            <div className="flex justify-between text-sm text-ink-faint mt-1.5 font-semibold">
              <span>3 quick</span>
              <span>5 usual</span>
              <span>10 full</span>
            </div>
          </div>

          <Button
            onClick={handleStartQuiz}
            loading={generating}
            disabled={!selectedTopic}
            icon={Play}
            size="lg"
            className="w-full"
          >
            {generating ? 'Building your quiz…' : 'Start quiz'}
          </Button>
        </Card>

        {/* Past Quiz History Sidebar */}
        <Card className="flex flex-col">
          <div className="flex items-center gap-2 mb-4 pb-3 border-b-2 border-ink/[0.06]">
            <History className="w-5 h-5 text-ink-soft" />
            <h3 className="text-lg font-display font-bold text-ink">Recent attempts</h3>
          </div>

          {history && history.length > 0 ? (
            <div className="space-y-3 overflow-y-auto max-h-[380px] pr-1">
              {history.map((h) => (
                <div key={h.id} className="p-3.5 bg-cream-soft rounded-2xl text-sm">
                  <div className="flex items-center justify-between font-bold text-ink gap-2">
                    <span className="truncate">{h.topic_name}</span>
                    <span
                      className={
                        h.accuracy >= 75 ? 'text-meadow-600' : h.accuracy >= 50 ? 'text-sun-600' : 'text-coral-600'
                      }
                    >
                      {h.accuracy}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm text-ink-faint mt-1">
                    <span>{h.score}/{h.total_questions} correct</span>
                    <span className="capitalize">{h.difficulty}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 text-base text-ink-soft">
              No quizzes yet — take your first one to start tracking your progress!
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};
