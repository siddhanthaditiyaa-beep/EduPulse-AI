import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from '../components/Sidebar';
import { Navbar } from '../components/Navbar';
import { StudySessionModal } from '../components/StudySessionModal';

export const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [studyModalOpen, setStudyModalOpen] = useState(false);
  const [activeTopic, setActiveTopic] = useState({ id: 1, name: 'Database Fundamentals' });

  const handleOpenStudy = (topicId = 1, topicName = 'Database Fundamentals') => {
    setActiveTopic({ id: topicId, name: topicName });
    setStudyModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-cream flex">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="flex-1 flex flex-col lg:pl-72 min-w-0">
        <Navbar
          onOpenSidebar={() => setSidebarOpen(true)}
          onOpenStudyModal={() => handleOpenStudy(1, 'Database Fundamentals')}
        />

        <main className="flex-1 p-4 sm:p-6 lg:p-10 max-w-6xl w-full mx-auto">
          <Outlet context={{ onStartStudySession: handleOpenStudy }} />
        </main>
      </div>

      <StudySessionModal
        isOpen={studyModalOpen}
        onClose={() => setStudyModalOpen(false)}
        topicId={activeTopic.id}
        topicName={activeTopic.name}
      />
    </div>
  );
};
