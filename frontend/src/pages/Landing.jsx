import React from 'react';
import { Link } from 'react-router-dom';
import {
  GraduationCap, Sparkles, ClipboardCheck, TrendingUp, Bot, CalendarCheck, ArrowRight,
} from 'lucide-react';
import { Button, Card, Badge } from '../components/ui/Kit';

const FeatureCard = ({ icon: Icon, tone, title, desc }) => {
  const toneMap = {
    ocean: 'bg-ocean-100 text-ocean-600',
    meadow: 'bg-meadow-100 text-meadow-600',
    berry: 'bg-berry-100 text-berry-600',
    sun: 'bg-sun-100 text-sun-600',
  };
  return (
    <Card className="flex flex-col gap-3">
      <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${toneMap[tone]}`}>
        <Icon className="w-6 h-6" strokeWidth={2.2} />
      </div>
      <h3 className="text-lg font-display font-bold text-ink">{title}</h3>
      <p className="text-base text-ink-soft leading-relaxed">{desc}</p>
    </Card>
  );
};

export const Landing = () => {
  return (
    <div className="min-h-screen bg-cream">
      {/* Top bar */}
      <header className="px-4 sm:px-8 h-20 flex items-center justify-between max-w-6xl mx-auto">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-2xl bg-ocean-500 flex items-center justify-center text-white shadow-[0_3px_0_0_rgba(35,76,107,0.5)]">
            <GraduationCap className="w-6 h-6" strokeWidth={2.2} />
          </div>
          <span className="text-lg font-display font-bold text-ink">EduPulse AI</span>
        </div>
        <Button as={Link} to="/login" variant="soft" size="sm">
          Log in
        </Button>
      </header>

      {/* Hero */}
      <section className="max-w-4xl mx-auto text-center px-4 pt-10 pb-16">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-sun-100 text-sun-600 text-sm font-bold mb-6">
          <Sparkles className="w-4 h-4" /> Learning, personalized just for you
        </div>
        <h1 className="text-4xl sm:text-5xl font-display font-bold text-ink leading-tight">
          Study smarter, not harder — with an AI that knows where you're stuck.
        </h1>
        <p className="mt-5 text-lg sm:text-xl text-ink-soft max-w-2xl mx-auto leading-relaxed">
          EduPulse AI finds your weak topics, predicts your exam performance, and builds
          you a daily study plan — with a friendly AI tutor to explain anything you get wrong.
        </p>

        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Button as={Link} to="/register" size="lg" iconRight={ArrowRight}>
            Create a free account
          </Button>
          <Button as={Link} to="/login" variant="soft" size="lg">
            I already have an account
          </Button>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-4 pb-20">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <FeatureCard
            icon={ClipboardCheck}
            tone="ocean"
            title="Quick diagnostic"
            desc="A short check-in finds your starting point in minutes — no guesswork."
          />
          <FeatureCard
            icon={TrendingUp}
            tone="berry"
            title="AI performance prediction"
            desc="See a realistic forecast of your exam score, based on how you're actually doing."
          />
          <FeatureCard
            icon={CalendarCheck}
            tone="sun"
            title="Daily study plan"
            desc="A short, focused plan every day that targets your weakest topics first."
          />
          <FeatureCard
            icon={Bot}
            tone="meadow"
            title="AI tutor, on demand"
            desc="Stuck on something? Ask and get an explanation pitched at your level."
          />
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="bg-ocean-600 py-14 px-4">
        <div className="max-w-3xl mx-auto text-center text-white">
          <Badge tone="gold" className="mb-4">Free to use</Badge>
          <h2 className="text-2xl sm:text-3xl font-display font-bold">
            Ready to find out what you actually know?
          </h2>
          <p className="mt-2 text-white/85 text-lg">
            It takes less than a minute to get started.
          </p>
          <Button as={Link} to="/register" size="lg" className="mt-6">
            Get started — it's free
          </Button>
        </div>
      </section>
    </div>
  );
};
