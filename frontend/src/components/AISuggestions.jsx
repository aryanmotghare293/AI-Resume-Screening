import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { toast } from 'react-hot-toast';
import { Copy, Sparkles } from 'lucide-react';
import { useAnalysis } from '../context/useAnalysis';
import { getAiSuggestions } from '../services/api';

const AISuggestions = () => {
  const { state } = useAnalysis();
  const [activeTab, setActiveTab] = useState('bullets');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState({
    bullets: null,
    keywords: null,
    summary: null
  });

  const generateSuggestions = async () => {
    setLoading(true);
    const toastId = toast.loading('Gemini is analyzing your resume...');
    try {
      const result = await getAiSuggestions(state.resumeData.raw_text, state.jdText || 'N/A');
      setSuggestions(result);
      toast.success('Suggestions generated!', { id: toastId });
    } catch {
      toast.error('Failed to generate suggestions. Ensure GEMINI_API_KEY is set.', { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const renderContent = () => {
    if (!suggestions.bullets && !loading) {
      return (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
          <h3 className="text-xl font-semibold text-text-primary mb-2">AI Resume Optimization</h3>
          <p className="text-text-muted mb-6 max-w-md">
            Click below to let Gemini rewrite your weak bullets, suggest missing ATS keywords, and generate a powerful professional summary.
          </p>
          <button onClick={generateSuggestions} className="btn-primary flex items-center gap-2">
            <Sparkles className="w-4 h-4" /> Generate Optimizations
          </button>
        </div>
      );
    }

    if (loading) {
      return (
        <div className="py-12 space-y-4 animate-pulse">
          <div className="h-4 bg-white/5 rounded w-3/4"></div>
          <div className="h-4 bg-white/5 rounded w-full"></div>
          <div className="h-4 bg-white/5 rounded w-5/6"></div>
        </div>
      );
    }

    return (
      <div>
        <div className="flex gap-4 mb-6 border-b border-white/10 pb-4">
          <button onClick={() => setActiveTab('bullets')} className={`px-4 py-2 font-medium rounded-lg ${activeTab === 'bullets' ? 'bg-primary text-white' : 'text-text-secondary hover:bg-white/10'}`}>Bullet Points</button>
          <button onClick={() => setActiveTab('keywords')} className={`px-4 py-2 font-medium rounded-lg ${activeTab === 'keywords' ? 'bg-primary text-white' : 'text-text-secondary hover:bg-white/10'}`}>ATS Keywords</button>
          <button onClick={() => setActiveTab('summary')} className={`px-4 py-2 font-medium rounded-lg ${activeTab === 'summary' ? 'bg-primary text-white' : 'text-text-secondary hover:bg-white/10'}`}>Summary</button>
        </div>
        <div className="relative bg-bg-dark border border-white/10 p-6 rounded-xl prose prose-invert max-w-none">
          <button 
            onClick={() => copyToClipboard(suggestions[activeTab])}
            className="absolute top-4 right-4 p-2 bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
          >
            <Copy className="w-4 h-4 text-text-secondary" />
          </button>
          <ReactMarkdown>{suggestions[activeTab] || 'No content generated.'}</ReactMarkdown>
        </div>
      </div>
    );
  };

  return <div className="card p-6">{renderContent()}</div>;
};

export default AISuggestions;
