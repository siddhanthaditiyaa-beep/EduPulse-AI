import React, { useState, useEffect } from 'react';
import { useParams, Link, useOutletContext } from 'react-router-dom';
import api from '../api/client';
import { Clock, HelpCircle, Bot, ArrowLeft, Award } from 'lucide-react';
import { Card, Badge, Spinner, Button } from '../components/ui/Kit';

export const TopicDetail = () => {
  const { id } = useParams();
  const outletCtx = useOutletContext();
  const [topic, setTopic] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTopic = async () => {
      try {
        const res = await api.get(`/subjects/topics/${id}`);
        setTopic(res.data);
      } catch (err) {
        console.error('Failed to load topic detail:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchTopic();
  }, [id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Spinner size={32} className="text-ocean-500" />
      </div>
    );
  }

  if (!topic) {
    return (
      <div className="text-center py-12">
        <p className="text-lg text-ink-soft">We couldn't find that topic.</p>
        <Link to="/learning" className="mt-2 text-ocean-600 font-bold inline-block">
          Back to My Learning
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <Link
        to="/learning"
        className="inline-flex items-center gap-2 text-base font-bold text-ink-soft hover:text-ink transition"
      >
        <ArrowLeft className="w-4 h-4" /> Back to My Learning
      </Link>

      <Card className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
        <div>
          <Badge tone="ocean">Learning material</Badge>
          <h1 className="text-2xl sm:text-3xl font-display font-bold text-ink mt-2">{topic.name}</h1>
          <p className="text-base text-ink-soft mt-1">{topic.description}</p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <Button variant="ocean" size="sm" icon={Clock} onClick={() => outletCtx?.onStartStudySession(topic.id, topic.name)}>
            Track time
          </Button>
          <Button as={Link} to={`/quizzes?topicId=${topic.id}`} variant="soft" size="sm" icon={HelpCircle}>
            Take quiz
          </Button>
          <Button
            as={Link}
            to={`/ai-tutor?topicId=${topic.id}&topicName=${encodeURIComponent(topic.name)}`}
            variant="soft"
            size="sm"
            icon={Bot}
          >
            Ask AI tutor
          </Button>
        </div>
      </Card>

      {/* Mastery Summary */}
      <div className="bg-ocean-600 rounded-2xl p-5 text-white flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-white/15 flex items-center justify-center text-gold-400">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <p className="text-sm text-white/75">Your mastery in this topic</p>
            <p className="text-xl font-display font-bold">{topic.mastery_score}%</p>
          </div>
        </div>

        <div className="text-right">
          <p className="text-sm text-white/75">Quiz accuracy</p>
          <p className="text-lg font-bold text-meadow-500">{topic.accuracy}%</p>
        </div>
      </div>

      {/* Learning Materials */}
      <div className="space-y-6">
        {topic.materials && topic.materials.length > 0 ? (
          topic.materials.map((mat) => (
            <Card key={mat.id} className="p-6 sm:p-10">
              <h2 className="text-xl font-display font-bold text-ink mb-2">{mat.title}</h2>
              <p className="text-base text-ink-soft mb-6 pb-4 border-b-2 border-ink/[0.06]">{mat.description}</p>
              <div className="max-w-none text-base leading-relaxed text-ink whitespace-pre-line">
                {mat.content}
              </div>
            </Card>
          ))
        ) : (
          <Card className="text-center py-10 text-ink-soft">
            No notes uploaded for this topic yet.
          </Card>
        )}
      </div>
    </div>
  );
};
