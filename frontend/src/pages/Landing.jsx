import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { motion } from 'framer-motion';
import { Target, BarChart2, Zap, FileSearch } from 'lucide-react';
import { useAnalysis } from '../context/useAnalysis';
import { analyzeResume } from '../services/api';
import FileUpload from '../components/FileUpload';
import JDInput from '../components/JDInput';

const MotionDiv = motion.div;
const MotionH1 = motion.h1;
const MotionP = motion.p;

const Landing = () => {
  const [file, setFile] = useState(null);
  const [jdText, setJdText] = useState('');
  const { state, dispatch } = useAnalysis();
  const navigate = useNavigate();

  const handleAnalyze = async () => {
    if (!file) {
      toast.error('Please upload a resume first.');
      return;
    }
    if (!jdText.trim()) {
      toast.error('Please paste a job description.');
      return;
    }

    dispatch({ type: 'START_ANALYSIS' });
    toast.loading('Analyzing resume...', { id: 'analyze' });

    try {
      const result = await analyzeResume(file, jdText, state.targetRole);
      dispatch({ type: 'ANALYSIS_SUCCESS', payload: result });
      toast.success('Analysis complete!', { id: 'analyze' });
      navigate('/dashboard');
    } catch (error) {
      const errorMsg = error.response?.data?.detail || 'Analysis failed. Please try again.';
      dispatch({ type: 'ANALYSIS_ERROR', payload: errorMsg });
      toast.error(errorMsg, { id: 'analyze' });
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16 relative">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary/20 rounded-full blur-[100px] -z-10" />
        <MotionH1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl md:text-6xl font-bold mb-6 tracking-tight"
        >
          AI Resume Screener <br className="hidden md:block"/> 
          <span className="gradient-text">& ATS Optimizer</span>
        </MotionH1>
        <MotionP
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-lg text-text-secondary max-w-2xl mx-auto"
        >
          Upload your resume, paste a job description, and get instant ATS analysis, 
          skill gap detection, and AI-powered improvements.
        </MotionP>
      </div>

      {/* Main Upload Area */}
      <MotionDiv
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className="max-w-4xl mx-auto card p-8 backdrop-blur-sm bg-bg-card/80 mb-16"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="h-full flex flex-col">
            <FileUpload file={file} setFile={setFile} />
          </div>
          <div className="h-full flex flex-col">
            <JDInput jdText={jdText} setJdText={setJdText} />
          </div>
        </div>
        
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-white/10 pt-6">
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <label className="text-sm font-medium text-text-secondary whitespace-nowrap">Target Role:</label>
            <select 
              value={state.targetRole}
              onChange={(e) => dispatch({ type: 'SET_TARGET_ROLE', payload: e.target.value })}
              className="glass-input px-4 py-2 w-full sm:w-48 text-sm"
            >
              <option value="Data Scientist">Data Scientist</option>
              <option value="Machine Learning Engineer">Machine Learning Engineer</option>
              <option value="AI Engineer">AI Engineer</option>
              <option value="Data Analyst">Data Analyst</option>
              <option value="Software Engineer">Software Engineer</option>
              <option value="Full Stack Developer">Full Stack Developer</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <button 
            onClick={handleAnalyze}
            disabled={state.isAnalyzing}
            className="btn-primary w-full sm:w-auto flex items-center justify-center gap-2"
          >
            {state.isAnalyzing ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                Analyze Resume
              </>
            )}
          </button>
        </div>
      </MotionDiv>

      {/* Features Grid */}
      <MotionDiv
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto"
      >
        {[
          { icon: Target, title: 'ATS Scoring', desc: 'Get instant compatibility scores with detailed breakdowns' },
          { icon: FileSearch, title: 'Skill Gap Analysis', desc: 'Identify missing skills and get customized learning paths' },
          { icon: Zap, title: 'AI Improvements', desc: 'AI-powered resume rewriting and keyword optimization' },
          { icon: BarChart2, title: 'Interview Prep', desc: 'Role-specific questions tailored to your skill gaps' }
        ].map((feature, i) => (
          <div key={i} className="card p-6 text-center hover:-translate-y-1 group">
            <div className="w-12 h-12 mx-auto bg-primary/10 rounded-2xl flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
              <feature.icon className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-semibold text-text-primary mb-2">{feature.title}</h3>
            <p className="text-sm text-text-muted">{feature.desc}</p>
          </div>
        ))}
      </MotionDiv>
    </div>
  );
};

export default Landing;
