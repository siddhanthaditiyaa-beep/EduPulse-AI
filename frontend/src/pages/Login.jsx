import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, ArrowRight, AlertCircle } from 'lucide-react';
import { AuthLayout } from '../components/AuthLayout';
import { Field, inputClass, Button } from '../components/ui/Kit';

export const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(
        err.response?.data?.detail || 'That email or password doesn\u2019t match. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Welcome back!" subtitle="Sign in to keep learning with EduPulse AI">
      {error && (
        <div className="mb-6 p-4 rounded-2xl bg-coral-100 text-coral-600 text-base font-semibold flex items-start gap-2.5">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <form className="space-y-5" onSubmit={handleSubmit}>
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

        <Field label="Password" icon={Lock}>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            className={inputClass()}
          />
        </Field>

        <Button type="submit" loading={loading} iconRight={ArrowRight} size="lg" className="w-full mt-2">
          Sign in
        </Button>
      </form>

      <div className="mt-8 pt-6 border-t-2 border-ink/[0.06] text-center">
        <p className="text-base text-ink-soft">
          New here?{' '}
          <Link to="/register" className="font-bold text-ocean-600 hover:text-ocean-700">
            Create a free account
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
};
