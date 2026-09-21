import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../api/client';
import { Clock, ArrowRight, ArrowLeft, CheckCircle2 } from 'lucide-react';
import confetti from 'canvas-confetti';
import { Card, Badge, ProgressBar, Button } from '../components/ui/Kit';

export const QuizAttempt = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const quizData = location.state?.quizData;
  const topicId = location.state?.topicId;
  const difficulty = location.state?.difficulty || 'medium';

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [responseTimes, setResponseTimes] = useState({});
  const [elapsed, setElapsed] = useState(0);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!quizData || !quizData.questions || quizData.questions.length === 0) {
      navigate('/quizzes');
    }
  }, [quizData, navigate]);

  useEffect(() => {
    const timer = setInterval(() => {
      setElapsed((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  if (!quizData || !quizData.questions) return null;

  const currentQ = quizData.questions[currentIndex];
  const totalQuestions = quizData.questions.length;

  const handleSelectOption = (optKey) => {
    setAnswers((prev) => ({ ...prev, [currentQ.id]: optKey }));
    setResponseTimes((prev) => ({
      ...prev,
      [currentQ.id]: (prev[currentQ.id] || 0) + 1,
    }));
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length < totalQuestions) {
      if (!window.confirm('You still have unanswered questions. Submit anyway?')) {
        return;
      }
    }

    setSubmitting(true);
    const answersPayload = quizData.questions.map((q) => ({
      question_id: q.id,
      selected_answer: answers[q.id] || '',
      response_time: responseTimes[q.id] || 10,
    }));

    try {
      const res = await api.post('/quiz/submit', {
        topic_id: parseInt(topicId, 10),
        difficulty,
        answers: answersPayload,
      });

      confetti({ particleCount: 80, spread: 60, origin: { y: 0.6 } });
      navigate('/quiz/result', { state: { result: res.data } });
    } catch (err) {
      console.error('Failed to submit quiz:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const formatTimer = (secs) => {
    const mins = Math.floor(secs / 60);
    const remainingSecs = secs % 60;
    return `${mins.toString().padStart(2, '0')}:${remainingSecs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <Card className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <Badge tone="ocean">{quizData.topic_name}</Badge>
          <h2 className="text-lg font-display font-bold text-ink mt-2">
            Question {currentIndex + 1} of {totalQuestions}
          </h2>
        </div>

        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1.5 px-3.5 py-2 bg-cream-soft rounded-xl text-sm font-bold text-ink">
            <Clock className="w-4 h-4 text-ink-soft" />
            <span>{formatTimer(elapsed)}</span>
          </div>
          <Badge tone="sun" className="capitalize">{difficulty}</Badge>
        </div>
      </Card>

      <ProgressBar value={((currentIndex + 1) / totalQuestions) * 100} tone="ocean" height="h-2.5" />

      <Card className="p-6 sm:p-10 space-y-6">
        <h3 className="text-xl font-bold text-ink leading-snug">{currentQ.question}</h3>

        <div className="space-y-3">
          {[
            { key: 'A', text: currentQ.option_a },
            { key: 'B', text: currentQ.option_b },
            { key: 'C', text: currentQ.option_c },
            { key: 'D', text: currentQ.option_d },
          ].map((opt) => {
            const isSelected = answers[currentQ.id] === opt.key;
            return (
              <button
                key={opt.key}
                type="button"
                onClick={() => handleSelectOption(opt.key)}
                className={`w-full text-left p-4 rounded-2xl border-2 text-base font-semibold transition flex items-start gap-3.5 cursor-pointer ${
                  isSelected
                    ? 'border-ocean-500 bg-ocean-50 text-ink'
                    : 'border-ink/10 hover:border-ocean-500/40 text-ink bg-paper'
                }`}
              >
                <span
                  className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-sm shrink-0 ${
                    isSelected ? 'bg-ocean-500 text-white' : 'bg-cream-soft text-ink-soft'
                  }`}
                >
                  {opt.key}
                </span>
                <span className="mt-0.5 leading-relaxed">{opt.text}</span>
              </button>
            );
          })}
        </div>
      </Card>

      <div className="flex items-center justify-between pt-2 gap-3">
        <Button
          variant="soft"
          icon={ArrowLeft}
          onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
          disabled={currentIndex === 0}
        >
          Previous
        </Button>

        {currentIndex < totalQuestions - 1 ? (
          <Button
            variant="ocean"
            iconRight={ArrowRight}
            onClick={() => setCurrentIndex((prev) => Math.min(totalQuestions - 1, prev + 1))}
          >
            Next
          </Button>
        ) : (
          <Button variant="primary" iconRight={CheckCircle2} loading={submitting} onClick={handleSubmit}>
            {submitting ? 'Submitting…' : 'Finish & see score'}
          </Button>
        )}
      </div>
    </div>
  );
};
