import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { User, Mail, Lock, ArrowRight, AlertCircle, ShieldCheck } from 'lucide-react';
import { AuthLayout } from '../components/AuthLayout';
import { Field, inputClass, Button } from '../components/ui/Kit';

export const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password.length < 6) {
      setError('Please use a password with at least 6 characters.');
      return;
    }

    setLoading(true);
    try {
      await register(name, email, password);
      navigate('/onboarding');
    } catch (err) {
      setError(
        err.response?.data?.detail || 'We couldn\u2019t create that account. That email may already be registered.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Let's get you started" subtitle="Create your free EduPulse AI account">
      {error && (
        <div className="mb-6 p-4 rounded-2xl bg-coral-100 text-coral-600 text-base font-semibold flex items-start gap-2.5">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <form className="space-y-5" onSubmit={handleSubmit}>
        <Field label="Full name" icon={User}>
          <input
            type="text"
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Yuvraj Yadav"
            className={inputClass()}
          />
        </Field>

        <Field label="Email address" icon={Mail}>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className={inputClass()}
          />
        </Field>

        <Field label="Create a password" icon={Lock}>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="At least 6 characters"
            className={inputClass()}
          />
        </Field>

        <div className="p-4 bg-meadow-100 rounded-2xl flex items-start gap-3 text-sm text-meadow-600 font-semibold">
          <ShieldCheck className="w-5 h-5 shrink-0 mt-0.5" />
          <span>This space is just for you \u2014 no teacher dashboards, no one watching over your shoulder.</span>
        </div>

        <Button type="submit" loading={loading} iconRight={ArrowRight} size="lg" className="w-full mt-2">
          Create my account
        </Button>
      </form>

      <div className="mt-8 pt-6 border-t-2 border-ink/[0.06] text-center">
        <p className="text-base text-ink-soft">
          Already have an account?{' '}
          <Link to="/login" className="font-bold text-ocean-600 hover:text-ocean-700">
            Sign in
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
};
