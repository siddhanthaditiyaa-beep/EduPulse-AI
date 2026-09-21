import React from 'react';
import { GraduationCap } from 'lucide-react';

/*
  Shared shell for Login/Register/Onboarding entry screens. One warm,
  illustrated moment (the blob + graduation cap mark) does the "hero"
  job so the rest of the screen can stay calm and easy to scan.
*/
export const AuthLayout = ({ title, subtitle, children }) => (
  <div className="min-h-screen bg-cream flex flex-col justify-center py-12 px-4">
    <div className="mx-auto w-full max-w-md text-center">
      <div className="relative inline-flex items-center justify-center w-20 h-20 mb-5">
        <svg viewBox="0 0 100 100" className="absolute inset-0 w-full h-full text-sun-400" fill="currentColor">
          <path d="M50 4C68 4 84 14 92 32C99 48 96 66 82 78C68 90 46 94 30 86C14 78 4 60 4 42C4 22 24 4 50 4Z" />
        </svg>
        <GraduationCap className="relative w-10 h-10 text-white" strokeWidth={2.2} />
      </div>
      <h2 className="text-3xl font-display font-bold text-ink">{title}</h2>
      <p className="mt-2 text-lg text-ink-soft">{subtitle}</p>
    </div>

    <div className="mt-8 mx-auto w-full max-w-md">
      <div className="bg-paper py-8 px-6 sm:px-9 rounded-3xl border-2 border-ink/[0.06]">
        {children}
      </div>
    </div>
  </div>
);
