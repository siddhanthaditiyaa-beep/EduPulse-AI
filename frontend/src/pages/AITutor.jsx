import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../api/client';
import { Bot, Send, User, Lightbulb, Zap, HelpCircle, BookOpen } from 'lucide-react';
import { Card, Badge } from '../components/ui/Kit';

export const AITutor = () => {
  const [searchParams] = useSearchParams();
  const topicIdParam = searchParams.get('topicId');
  const topicNameParam = searchParams.get('topicName');
  const questionIdParam = searchParams.get('questionId');
  const initialActionParam = searchParams.get('action');

  const [topics, setTopics] = useState([]);
  const [selectedTopicId, setSelectedTopicId] = useState(topicIdParam || '');
  const [selectedTopicName, setSelectedTopicName] = useState(topicNameParam || 'Database Fundamentals');
  const [inputMessage, setInputMessage] = useState('');
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hi! I'm your EduPulse AI Tutor. I explain things at the level that's right for you.\n\nAsk me to explain a tricky idea, go over a quiz mistake, or quiz you to check you've got it. What would you like help with?`,
    },
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const res = await api.get('/subjects/1/topics');
        setTopics(res.data);
        if (!selectedTopicId && res.data.length > 0) {
          setSelectedTopicId(res.data[0].id);
          setSelectedTopicName(res.data[0].name);
        } else if (selectedTopicId && res.data.length > 0) {
          const match = res.data.find((t) => t.id === parseInt(selectedTopicId, 10));
          if (match) setSelectedTopicName(match.name);
        }
      } catch (err) {
        console.error('Failed to load topics:', err);
      }
    };
    fetchTopics();
  }, [selectedTopicId]);

  useEffect(() => {
    if (initialActionParam === 'explain_mistake' && questionIdParam) {
      handleSend('Could you explain why my answer on this quiz question was incorrect and clarify the concept?', 'explain_mistake');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialActionParam, questionIdParam]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (customText = null, actionType = 'general') => {
    const textToSend = customText || inputMessage;
    if (!textToSend.trim()) return;

    const newHistory = [...messages, { role: 'user', content: textToSend }];
    setMessages(newHistory);
    setInputMessage('');
    setLoading(true);

    try {
      const res = await api.post('/ai/tutor', {
        message: textToSend,
        topic_id: selectedTopicId ? parseInt(selectedTopicId, 10) : null,
        action_type: actionType,
        context_question_id: questionIdParam ? parseInt(questionIdParam, 10) : null,
        chat_history: newHistory.slice(-6),
      });

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.data.reply,
          masteryLevel: res.data.student_mastery_level,
          suggestions: res.data.follow_up_suggestions,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: "Sorry, something went wrong there. Could you ask that again?" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const actionChips = [
    { label: 'Explain simply', action: 'explain_simply', icon: Lightbulb, query: `Explain ${selectedTopicName} simply, in plain everyday words.` },
    { label: 'Show an example', action: 'give_example', icon: BookOpen, query: `Give me a clear example illustrating ${selectedTopicName}.` },
    { label: 'Real-world use', action: 'real_world_example', icon: Zap, query: `How is ${selectedTopicName} used in real apps like Instagram or Netflix?` },
    { label: 'Test me', action: 'test_me', icon: HelpCircle, query: `Ask me a quick question to check my understanding of ${selectedTopicName}.` },
  ];

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-9rem)]">
      <Card padded={false} className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-2xl bg-berry-500 text-white flex items-center justify-center shrink-0">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-display font-bold text-ink flex items-center gap-2 flex-wrap">
              AI Tutor
              <Badge tone="berry">Matches your level</Badge>
            </h1>
            <p className="text-sm text-ink-soft">
              Explanations that adjust to what you already know.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-sm font-bold text-ink-soft shrink-0">Topic:</span>
          <select
            value={selectedTopicId}
            onChange={(e) => {
              setSelectedTopicId(e.target.value);
              const match = topics.find((t) => t.id === parseInt(e.target.value, 10));
              if (match) setSelectedTopicName(match.name);
            }}
            className="text-sm font-semibold p-2.5 bg-cream-soft border-2 border-ink/10 rounded-xl focus:outline-hidden focus:border-ocean-500 cursor-pointer"
          >
            {topics.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name} ({t.mastery_score}%)
              </option>
            ))}
          </select>
        </div>
      </Card>

      {/* Chat Messages */}
      <Card padded={false} className="flex-1 p-4 sm:p-6 overflow-y-auto space-y-4">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex items-start gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            {m.role === 'assistant' && (
              <div className="w-9 h-9 rounded-full bg-berry-500 text-white flex items-center justify-center shrink-0 mt-1">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div
              className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 text-base leading-relaxed ${
                m.role === 'user'
                  ? 'bg-ocean-500 text-white rounded-tr-md font-semibold'
                  : 'bg-cream-soft text-ink rounded-tl-md whitespace-pre-line'
              }`}
            >
              {m.masteryLevel && (
                <div className="mb-2">
                  <Badge tone="berry">Level: {m.masteryLevel}</Badge>
                </div>
              )}

              <div>{m.content}</div>

              {m.suggestions && m.suggestions.length > 0 && (
                <div className="mt-3 pt-3 border-t-2 border-ink/[0.06] flex flex-wrap gap-2">
                  {m.suggestions.map((s, sIdx) => (
                    <button
                      key={sIdx}
                      onClick={() => handleSend(s, 'general')}
                      className="text-sm font-semibold px-3 py-1.5 rounded-xl bg-white text-ocean-600 hover:bg-ocean-50 transition cursor-pointer"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {m.role === 'user' && (
              <div className="w-9 h-9 rounded-full bg-ink text-white flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-berry-500 text-white flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-4 rounded-2xl bg-cream-soft rounded-tl-md flex items-center gap-2 text-sm text-ink-soft">
              <div className="w-2 h-2 rounded-full bg-berry-500 animate-bounce"></div>
              <div className="w-2 h-2 rounded-full bg-berry-500 animate-bounce delay-100"></div>
              <div className="w-2 h-2 rounded-full bg-berry-500 animate-bounce delay-200"></div>
              <span className="ml-1">Thinking…</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </Card>

      {/* Action Chips */}
      <div className="flex items-center gap-2 overflow-x-auto py-3 px-1">
        {actionChips.map((chip) => {
          const Icon = chip.icon;
          return (
            <button
              key={chip.action}
              onClick={() => handleSend(chip.query, chip.action)}
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-paper border-2 border-ink/10 hover:border-ocean-500/40 text-sm font-bold text-ink-soft hover:text-ocean-600 shrink-0 transition cursor-pointer"
            >
              <Icon className="w-4 h-4" />
              <span>{chip.label}</span>
            </button>
          );
        })}
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="relative mt-1"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={`Ask anything about ${selectedTopicName}…`}
          className="w-full pl-5 pr-14 py-4 bg-paper border-2 border-ink/10 rounded-2xl text-base font-medium focus:outline-hidden focus:border-ocean-500"
        />
        <button
          type="submit"
          disabled={loading || !inputMessage.trim()}
          aria-label="Send message"
          className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 flex items-center justify-center rounded-xl bg-ocean-500 text-white hover:bg-ocean-600 disabled:opacity-30 transition cursor-pointer"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
};
