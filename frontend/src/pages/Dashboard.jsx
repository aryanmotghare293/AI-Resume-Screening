import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAnalysis } from '../context/useAnalysis';

import ATSScoreCard from '../components/ATSScoreCard';
import ScoreBreakdown from '../components/ScoreBreakdown';
import SkillGapChart from '../components/SkillGapChart';
import Recommendations from '../components/Recommendations';
import AISuggestions from '../components/AISuggestions';
import InterviewQuestions from '../components/InterviewQuestions';
import CareerRoadmap from '../components/CareerRoadmap';
import ResumePreview from '../components/ResumePreview';

const MotionDiv = motion.div;

const TABS = [
  { id: 'score', label: '📊 ATS Score' },
  { id: 'skills', label: '🔍 Skill Gap' },
  { id: 'ai', label: '✨ AI Help' },
  { id: 'interview', label: '❓ Interview Prep' },
  { id: 'roadmap', label: '🗺️ Career Roadmap' },
];

const Dashboard = () => {
  const { state } = useAnalysis();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('score');

  useEffect(() => {
    if (!state.isAnalyzed && !state.isAnalyzing) {
      navigate('/');
    }
  }, [state.isAnalyzed, state.isAnalyzing, navigate]);

  if (!state.isAnalyzed) return null;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Tab Navigation */}
      <div className="flex overflow-x-auto space-x-2 mb-8 pb-2 scrollbar-none border-b border-white/10">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`whitespace-nowrap px-6 py-3 font-medium text-sm rounded-t-xl transition-all relative ${
              activeTab === tab.id 
                ? 'text-white bg-primary/10 border-t border-x border-primary/20' 
                : 'text-text-secondary hover:text-white hover:bg-white/5'
            }`}
          >
            {tab.label}
            {activeTab === tab.id && (
              <MotionDiv
                layoutId="active-tab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
              />
            )}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <MotionDiv
          key={activeTab}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === 'score' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                  <ATSScoreCard atsResult={state.atsResult} />
                </div>
                <div className="lg:col-span-2">
                  <ScoreBreakdown breakdown={state.atsResult.breakdown} />
                </div>
              </div>
              <ResumePreview resumeData={state.resumeData} />
            </div>
          )}

          {activeTab === 'skills' && (
            <div className="space-y-6">
              <SkillGapChart gapResult={state.gapResult} />
              <Recommendations recommendations={state.recommendations} />
            </div>
          )}

          {activeTab === 'ai' && (
            <AISuggestions />
          )}

          {activeTab === 'interview' && (
            <InterviewQuestions />
          )}

          {activeTab === 'roadmap' && (
            <CareerRoadmap />
          )}
        </MotionDiv>
      </AnimatePresence>
    </div>
  );
};

export default Dashboard;
