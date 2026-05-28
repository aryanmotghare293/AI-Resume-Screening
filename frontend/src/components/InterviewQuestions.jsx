import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { toast } from 'react-hot-toast';
import { Copy, MessageSquareCode } from 'lucide-react';
import { useAnalysis } from '../context/useAnalysis';
import { getInterviewQuestions } from '../services/api';

const InterviewQuestions = () => {
  const { state } = useAnalysis();
  const [questions, setQuestions] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateQuestions = async () => {
    setLoading(true);
    const toastId = toast.loading('Gemini is crafting interview questions...');
    try {
      const result = await getInterviewQuestions(
        state.resumeSkills,
        state.resumeData?.projects || '',
        state.targetRole,
        state.gapResult?.missing || []
      );
      setQuestions(result.questions);
      toast.success('Questions generated!', { id: toastId });
    } catch {
      toast.error('Failed to generate questions. Ensure GEMINI_API_KEY is set.', { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(questions);
    toast.success('Copied to clipboard!');
  };

  if (!questions && !loading) {
    return (
      <div className="card p-6 flex flex-col items-center justify-center py-16 text-center">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
          <MessageSquareCode className="w-8 h-8 text-primary" />
        </div>
        <h3 className="text-xl font-semibold text-text-primary mb-2">Interview Prep</h3>
        <p className="text-text-muted mb-6 max-w-md">
          Generate role-specific interview questions based on your resume, target role ({state.targetRole}), and skill gaps.
        </p>
        <button onClick={generateQuestions} className="btn-primary flex items-center gap-2">
          <MessageSquareCode className="w-4 h-4" /> Generate Questions
        </button>
      </div>
    );
  }

  return (
    <div className="card p-6 relative">
      <div className="flex items-center justify-between mb-6 border-b border-white/10 pb-4">
        <h2 className="text-lg font-semibold text-text-primary">Interview Questions</h2>
        {questions && (
          <button onClick={copyToClipboard} className="flex items-center gap-2 text-sm text-text-secondary hover:text-white transition-colors">
            <Copy className="w-4 h-4" /> Copy All
          </button>
        )}
      </div>
      
      {loading ? (
        <div className="py-12 space-y-4 animate-pulse">
          <div className="h-4 bg-white/5 rounded w-3/4"></div>
          <div className="h-4 bg-white/5 rounded w-full"></div>
          <div className="h-4 bg-white/5 rounded w-5/6"></div>
          <div className="h-4 bg-white/5 rounded w-2/3"></div>
        </div>
      ) : (
        <div className="prose prose-invert max-w-none bg-bg-dark border border-white/10 p-6 rounded-xl">
          <ReactMarkdown>{questions}</ReactMarkdown>
        </div>
      )}
    </div>
  );
};

export default InterviewQuestions;
