import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/client';
import { Sparkles, CheckCircle2, ArrowRight } from 'lucide-react';
import confetti from 'canvas-confetti';
import { Card, Badge, Spinner, Button } from '../components/ui/Kit';

export const DiagnosticTest = () => {
  const { subjectId = 1 } = useParams();

  const [testData, setTestData] = useState(null);
  const [answers, setAnswers] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await api.get(`/diagnostic/${subjectId}/questions`);
        setTestData(res.data);
      } catch (err) {
        console.error('Failed to load diagnostic questions:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchQuestions();
  }, [subjectId]);

  const handleSelectOption = (qId, opt) => {
    setAnswers((prev) => ({ ...prev, [qId]: opt }));
  };

  const handleSubmit = async () => {
    if (Object.keys(answers).length < testData.questions.length) {
      if (!window.confirm('You still have unanswered questions. Submit anyway?')) {
        return;
      }
    }

    setSubmitting(true);
    const answersPayload = testData.questions.map((q) => ({
      question_id: q.id,
      selected_answer: answers[q.id] || '',
      topic_id: q.topic_id,
    }));

    try {
      const res = await api.post('/diagnostic/submit', {
        subject_id: parseInt(subjectId, 10),
        answers: answersPayload,
      });
      setResult(res.data);
      confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
    } catch (err) {
      console.error('Failed to submit diagnostic assessment:', err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Spinner size={34} className="text-ocean-500" />
      </div>
    );
  }

  if (result) {
    return (
      <div className="max-w-3xl mx-auto space-y-8">
        <Card className="text-center py-8">
          <div className="w-16 h-16 rounded-full bg-meadow-100 text-meadow-600 flex items-center justify-center mx-auto mb-4">
            <CheckCircle2 className="w-8 h-8" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-display font-bold text-ink">Nice work — you're all done!</h1>
          <p className="text-base text-ink-soft mt-2 max-w-lg mx-auto">
            We've checked your answers and built your first personalized study plan.
          </p>

          <div className="mt-8 grid grid-cols-3 gap-4 max-w-md mx-auto">
            <div className="p-4 bg-ocean-50 rounded-2xl">
              <p className="text-sm font-bold text-ocean-600">Score</p>
              <p className="text-2xl font-display font-bold text-ocean-600 mt-1">{result.overall_score}%</p>
            </div>
            <div className="p-4 bg-meadow-100 rounded-2xl">
              <p className="text-sm font-bold text-meadow-600">Correct</p>
              <p className="text-2xl font-display font-bold text-meadow-600 mt-1">
                {result.correct_answers}/{result.total_questions}
              </p>
            </div>
            <div className="p-4 bg-sun-100 rounded-2xl">
              <p className="text-sm font-bold text-sun-600">XP earned</p>
              <p className="text-2xl font-display font-bold text-sun-600 mt-1">+100</p>
            </div>
          </div>
        </Card>

        <Card className="p-6 sm:p-8">
          <h2 className="text-xl font-display font-bold text-ink mb-4">How you did, topic by topic</h2>
          <div className="space-y-3">
            {result.topic_breakdown.map((t) => (
              <div key={t.topic_id} className="p-4 rounded-2xl bg-cream-soft flex items-center justify-between gap-3 flex-wrap">
                <div>
                  <h3 className="text-base font-bold text-ink">{t.topic_name}</h3>
                  <p className="text-sm text-ink-faint mt-0.5">
                    {t.correct} of {t.total} correct
                  </p>
                </div>
                <Badge tone={t.accuracy >= 75 ? 'meadow' : t.accuracy >= 50 ? 'sun' : 'coral'}>
                  {t.accuracy}% accuracy
                </Badge>
              </div>
            ))}
          </div>

          <div className="mt-8 pt-6 border-t-2 border-ink/[0.06] flex flex-col sm:flex-row items-center justify-between gap-4">
            <p className="text-base text-ink-soft">
              Your weaker topics come first in today's plan.
            </p>
            <Button as={Link} to="/dashboard" iconRight={ArrowRight} className="w-full sm:w-auto">
              Go to my dashboard
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <Card className="p-6 sm:p-8">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-ocean-100 text-ocean-600 text-sm font-bold mb-3">
          <Sparkles className="w-4 h-4" /> Quick check-in
        </div>
        <h1 className="text-2xl sm:text-3xl font-display font-bold text-ink">
          {testData?.subject_name} check-in
        </h1>
        <p className="text-base text-ink-soft mt-2 leading-relaxed">
          Just do your best — there's no penalty for a wrong answer. This only helps us find the right starting point for you.
        </p>

        <div className="mt-4 flex items-center gap-3 text-sm font-bold text-ink-soft flex-wrap">
          <span>{testData?.total_questions} questions</span>
          <span>•</span>
          <span>Answered: {Object.keys(answers).length} / {testData?.total_questions}</span>
        </div>
      </Card>

      <div className="space-y-6">
        {testData?.questions.map((q, idx) => (
          <Card key={q.id} className="p-6 sm:p-8">
            <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
              <span className="text-sm font-bold text-ocean-600">Question {idx + 1} of {testData.total_questions}</span>
              <span className="text-sm font-semibold text-ink-faint bg-cream-soft px-2.5 py-1 rounded-lg">
                {q.topic_name}
              </span>
            </div>

            <h3 className="text-lg font-bold text-ink leading-snug mb-5">{q.question}</h3>

            <div className="space-y-2.5">
              {[
                { key: 'A', text: q.option_a },
                { key: 'B', text: q.option_b },
                { key: 'C', text: q.option_c },
                { key: 'D', text: q.option_d },
              ].map((opt) => {
                const isSelected = answers[q.id] === opt.key;
                return (
                  <button
                    key={opt.key}
                    type="button"
                    onClick={() => handleSelectOption(q.id, opt.key)}
                    className={`w-full text-left p-4 rounded-2xl border-2 text-base transition flex items-start gap-3 cursor-pointer ${
                      isSelected
                        ? 'border-ocean-500 bg-ocean-50 text-ink font-semibold'
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
                    <span className="mt-0.5">{opt.text}</span>
                  </button>
                );
              })}
            </div>
          </Card>
        ))}
      </div>

      <Card className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <p className="text-base text-ink-soft">
          Ready to submit your answers?
        </p>
        <Button onClick={handleSubmit} loading={submitting} size="lg" className="w-full sm:w-auto">
          {submitting ? 'Checking your answers…' : 'Submit'}
        </Button>
      </Card>
    </div>
  );
};
