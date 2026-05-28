import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { toast } from 'react-hot-toast';
import { Route, MapPin } from 'lucide-react';
import { useAnalysis } from '../context/useAnalysis';
import { getCareerRoadmap } from '../services/api';

const CareerRoadmap = () => {
  const { state } = useAnalysis();
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateRoadmap = async () => {
    setLoading(true);
    const toastId = toast.loading('Gemini is designing your career roadmap...');
    try {
      const result = await getCareerRoadmap(state.resumeData, state.targetRole);
      setRoadmap(result.roadmap);
      toast.success('Roadmap generated!', { id: toastId });
    } catch {
      toast.error('Failed to generate roadmap. Ensure GEMINI_API_KEY is set.', { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  if (!roadmap && !loading) {
    return (
      <div className="card p-6 flex flex-col items-center justify-center py-16 text-center">
        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
          <MapPin className="w-8 h-8 text-primary" />
        </div>
        <h3 className="text-xl font-semibold text-text-primary mb-2">Personalized Career Roadmap</h3>
        <p className="text-text-muted mb-6 max-w-md">
          Get a detailed 30-60-90 day plan tailored to transition your current profile into a {state.targetRole}.
        </p>
        <button onClick={generateRoadmap} className="btn-primary flex items-center gap-2">
          <Route className="w-4 h-4" /> Generate Roadmap
        </button>
      </div>
    );
  }

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold text-text-primary mb-6 border-b border-white/10 pb-4">Your Career Path</h2>
      
      {loading ? (
        <div className="py-12 space-y-6">
          <div className="flex gap-4">
            <div className="w-2 h-20 bg-primary/20 rounded-full animate-pulse"></div>
            <div className="flex-1 space-y-4 animate-pulse">
              <div className="h-4 bg-white/5 rounded w-1/4"></div>
              <div className="h-4 bg-white/5 rounded w-3/4"></div>
            </div>
          </div>
          <div className="flex gap-4">
            <div className="w-2 h-20 bg-primary/20 rounded-full animate-pulse"></div>
            <div className="flex-1 space-y-4 animate-pulse">
              <div className="h-4 bg-white/5 rounded w-1/4"></div>
              <div className="h-4 bg-white/5 rounded w-2/3"></div>
            </div>
          </div>
        </div>
      ) : (
        <div className="prose prose-invert max-w-none">
          <ReactMarkdown>{roadmap}</ReactMarkdown>
        </div>
      )}
    </div>
  );
};

export default CareerRoadmap;
