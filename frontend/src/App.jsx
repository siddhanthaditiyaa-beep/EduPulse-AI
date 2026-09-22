import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { DashboardLayout } from './layouts/DashboardLayout';

// Pages
import { Landing } from './pages/Landing';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Onboarding } from './pages/Onboarding';
import { Dashboard } from './pages/Dashboard';
import { MyLearning } from './pages/MyLearning';
import { TopicDetail } from './pages/TopicDetail';
import { DiagnosticTest } from './pages/DiagnosticTest';
import { Quizzes } from './pages/Quizzes';
import { QuizAttempt } from './pages/QuizAttempt';
import { QuizResult } from './pages/QuizResult';
import { AITutor } from './pages/AITutor';
import { StudyPlan } from './pages/StudyPlan';
import { MyProgress } from './pages/MyProgress';
import { Profile } from './pages/Profile';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Landing Page */}
          <Route path="/" element={<Landing />} />

          {/* Public Auth Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Student Onboarding */}
          <Route
            path="/onboarding"
            element={
              <ProtectedRoute>
                <Onboarding />
              </ProtectedRoute>
            }
          />

          {/* Diagnostic Assessment Direct Route */}
          <Route
            path="/diagnostic/:subjectId"
            element={
              <ProtectedRoute>
                <DiagnosticTest />
              </ProtectedRoute>
            }
          />

          {/* Protected Application Routes inside DashboardLayout */}
          <Route
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/learning" element={<MyLearning />} />
            <Route path="/learning/topic/:id" element={<TopicDetail />} />
            <Route path="/quizzes" element={<Quizzes />} />
            <Route path="/quiz/attempt" element={<QuizAttempt />} />
            <Route path="/quiz/result" element={<QuizResult />} />
            <Route path="/ai-tutor" element={<AITutor />} />
            <Route path="/study-plan" element={<StudyPlan />} />
            <Route path="/progress" element={<MyProgress />} />
            <Route path="/profile" element={<Profile />} />
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
