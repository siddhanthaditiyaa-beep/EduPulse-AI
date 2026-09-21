import React, { useState, useEffect } from 'react';
import { Play, Pause, Square, CheckCircle, Clock, X, Award } from 'lucide-react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';
import confetti from 'canvas-confetti';
import { Button, Badge } from './ui/Kit';

export const StudySessionModal = ({ isOpen, onClose, topicId, topicName }) => {
  const { updateUserData } = useAuth();
  const [seconds, setSeconds] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [completedTopic, setCompletedTopic] = useState(false);
  const [isFinishing, setIsFinishing] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [successResult, setSuccessResult] = useState(null);

  useEffect(() => {
    let interval = null;
    if (isActive) {
      interval = setInterval(() => {
        setSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      clearInterval(interval);
    }
    return () => clearInterval(interval);
  }, [isActive]);

  useEffect(() => {
    if (isOpen) {
      setSeconds(0);
      setIsActive(true);
      setIsFinishing(false);
      setSuccessResult(null);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const formatTime = (totalSecs) => {
    const mins = Math.floor(totalSecs / 60);
    const secs = totalSecs % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStop = () => {
    setIsActive(false);
    setIsFinishing(true);
  };

  const handleSaveSession = async () => {
    setSubmitting(true);
    const durationMins = Math.max(1, Math.round(seconds / 60));
    try {
      const res = await api.post('/study-session/log', {
        topic_id: topicId,
        duration_minutes: durationMins,
        completed_topic: completedTopic,
      });
      setSuccessResult(res.data);
      confetti({ particleCount: 70, spread: 60, origin: { y: 0.7 } });
      updateUserData({ xp_points: (prev) => (prev || 0) + res.data.xp_earned });
    } catch (err) {
      console.error('Failed to log study session:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/50 backdrop-blur-xs p-4">
      <div className="bg-paper rounded-3xl shadow-xl w-full max-w-md overflow-hidden border-2 border-ink/[0.06]">
        <div className="px-6 py-4 bg-cream-soft flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-ocean-500" />
            <h3 className="font-display font-bold text-ink">Study timer</h3>
          </div>
          <button onClick={onClose} aria-label="Close" className="w-9 h-9 flex items-center justify-center rounded-xl text-ink-faint hover:text-ink hover:bg-white transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6">
          <p className="text-sm font-bold text-ocean-600 mb-1">Focusing on</p>
          <h4 className="text-xl font-display font-bold text-ink mb-6">{topicName}</h4>

          {!successResult ? (
            !isFinishing ? (
              <div className="flex flex-col items-center justify-center py-4">
                <div className="text-5xl font-display font-bold text-ink tracking-tight mb-8">
                  {formatTime(seconds)}
                </div>

                <div className="flex items-center gap-3">
                  {isActive ? (
                    <Button variant="soft" icon={Pause} onClick={() => setIsActive(false)}>
                      Pause
                    </Button>
                  ) : (
                    <Button variant="ocean" icon={Play} onClick={() => setIsActive(true)}>
                      Resume
                    </Button>
                  )}
                  <Button variant="primary" icon={Square} onClick={handleStop}>
                    Finish
                  </Button>
                </div>
              </div>
            ) : (
              <div className="space-y-5">
                <div className="p-4 bg-ocean-50 rounded-2xl text-center">
                  <p className="text-base text-ink">
                    Session length: <strong className="text-ocean-600 font-bold">{Math.max(1, Math.round(seconds / 60))} minute(s)</strong>
                  </p>
                </div>

                <div className="flex items-start gap-3 p-4 bg-cream-soft rounded-2xl">
                  <input
                    type="checkbox"
                    id="completedTopic"
                    checked={completedTopic}
                    onChange={(e) => setCompletedTopic(e.target.checked)}
                    className="mt-1 w-5 h-5 text-ocean-500 rounded border-ink/20 focus:ring-ocean-500 cursor-pointer"
                  />
                  <label htmlFor="completedTopic" className="text-base font-semibold text-ink cursor-pointer">
                    Did you finish this topic?
                    <span className="block text-sm text-ink-faint font-normal mt-0.5">
                      Check this if you're ready for a quiz. (+25 bonus XP)
                    </span>
                  </label>
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    onClick={() => setIsFinishing(false)}
                    className="px-4 py-2.5 text-base font-bold text-ink-soft hover:text-ink"
                  >
                    Back to timer
                  </button>
                  <Button onClick={handleSaveSession} loading={submitting} size="sm">
                    {submitting ? 'Saving…' : 'Save session'}
                  </Button>
                </div>
              </div>
            )
          ) : (
            <div className="text-center py-4 space-y-4">
              <div className="w-14 h-14 rounded-full bg-meadow-100 text-meadow-600 flex items-center justify-center mx-auto">
                <CheckCircle className="w-7 h-7" />
              </div>
              <h5 className="text-xl font-display font-bold text-ink">Session saved!</h5>
              <p className="text-base text-ink-soft">{successResult.message}</p>
              <Badge tone="sun" icon={Award}>+{successResult.xp_earned} XP earned</Badge>
              <div className="pt-2">
                <Button onClick={onClose} className="w-full" size="lg">
                  Done
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
