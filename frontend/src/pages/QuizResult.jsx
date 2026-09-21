import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { CheckCircle, XCircle, Award, ArrowRight, Bot, RotateCcw } from 'lucide-react';
import { Card, Button, Badge } from '../components/ui/Kit';

export const QuizResult = () => {
  const location = useLocation();
  const result = location.state?.result;

  if (!result) {
    return (
      <div className="text-center py-12">
        <p className="text-lg text-ink-soft">We couldn't find a recent quiz result.</p>
        <Link to="/quizzes" className="mt-3 inline-block font-bold text-ocean-600">
          Back to Quizzes
        </Link>
      </div>
    );
  }

  const masteryDiff = (result.new_mastery - result.old_mastery).toFixed(1);

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <Card className="text-center py-8">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-ocean-100 text-ocean-600 mb-3">
          <Award className="w-8 h-8" />
        </div>
        <Badge tone="ocean">Quiz complete</Badge>
        <h1 className="text-2xl sm:text-3xl font-display font-bold text-ink mt-2">{result.topic_name}</h1>
        <p className="text-base text-ink-soft mt-1 capitalize">Difficulty: {result.difficulty}</p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">
          <div className="p-4 bg-cream-soft rounded-2xl">
            <p className="text-sm font-bold text-ink-soft">Score</p>
            <p className="text-2xl font-display font-bold text-ink mt-0.5">
              {result.score}/{result.total_questions}
            </p>
          </div>

          <div className="p-4 bg-meadow-100 rounded-2xl">
            <p className="text-sm font-bold text-meadow-600">Accuracy</p>
            <p className="text-2xl font-display font-bold text-meadow-600 mt-0.5">{result.accuracy}%</p>
          </div>

          <div className="p-4 bg-ocean-50 rounded-2xl">
            <p className="text-sm font-bold text-ocean-600">New mastery</p>
            <p className="text-2xl font-display font-bold text-ocean-600 mt-0.5">
              {result.new_mastery}%
              {parseFloat(masteryDiff) > 0 && (
                <span className="text-sm font-bold ml-1">+{masteryDiff}%</span>
              )}
            </p>
          </div>

          <div className="p-4 bg-sun-100 rounded-2xl">
            <p className="text-sm font-bold text-sun-600">XP earned</p>
            <p className="text-2xl font-display font-bold text-sun-600 mt-0.5">+{result.xp_earned}</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-3 mt-6 pt-6 border-t-2 border-ink/[0.06]">
          <Button as={Link} to={`/quizzes?topicId=${result.topic_id}`} variant="soft" icon={RotateCcw} size="sm">
            Retake quiz
          </Button>
          <Button as={Link} to="/dashboard" iconRight={ArrowRight} size="sm">
            Go to dashboard
          </Button>
        </div>
      </Card>

      <div className="space-y-4">
        <h2 className="text-xl font-display font-bold text-ink">Review your answers</h2>

        {result.details.map((q, idx) => (
          <Card
            key={q.question_id || idx}
            className={q.is_correct ? '' : 'bg-coral-100/40 border-coral-500/20'}
          >
            <div className="flex items-start justify-between gap-3 mb-3">
              <span className="text-sm font-bold text-ink-faint">Question {idx + 1}</span>
              {q.is_correct ? (
                <Badge tone="meadow" icon={CheckCircle}>Correct</Badge>
              ) : (
                <Badge tone="coral" icon={XCircle}>Incorrect</Badge>
              )}
            </div>

            <h3 className="text-base font-bold text-ink mb-4">{q.question}</h3>

            <div className="space-y-2 mb-4">
              {[
                { key: 'A', text: q.option_a },
                { key: 'B', text: q.option_b },
                { key: 'C', text: q.option_c },
                { key: 'D', text: q.option_d },
              ].map((opt) => {
                const isSelected = q.selected_answer === opt.key;
                const isCorrectOpt = q.correct_answer === opt.key;

                let cls = 'border-ink/10 bg-cream-soft text-ink-soft';
                if (isCorrectOpt) {
                  cls = 'border-meadow-500 bg-meadow-100 text-meadow-600 font-bold';
                } else if (isSelected && !q.is_correct) {
                  cls = 'border-coral-500 bg-coral-100 text-coral-600 line-through';
                }

                return (
                  <div key={opt.key} className={`p-3 rounded-xl border-2 text-sm flex items-center justify-between gap-2 flex-wrap ${cls}`}>
                    <div className="flex items-center gap-2.5">
                      <span className="font-bold">{opt.key}.</span>
                      <span>{opt.text}</span>
                    </div>
                    {isCorrectOpt && <span className="text-xs font-bold">Correct answer</span>}
                    {isSelected && !isCorrectOpt && <span className="text-xs font-bold">Your answer</span>}
                  </div>
                );
              })}
            </div>

            <div className="p-4 bg-cream-soft rounded-2xl text-sm text-ink leading-relaxed">
              <strong className="text-ink font-bold block mb-1">Why:</strong>
              {q.explanation}
            </div>

            {!q.is_correct && (
              <div className="mt-3 flex justify-end">
                <Button
                  as={Link}
                  to={`/ai-tutor?topicId=${result.topic_id}&questionId=${q.question_id}&action=explain_mistake`}
                  variant="soft"
                  icon={Bot}
                  size="sm"
                >
                  Ask AI tutor why
                </Button>
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
};
