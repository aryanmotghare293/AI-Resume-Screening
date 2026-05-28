import { useState } from 'react';
import { Award, Code, Wrench, ListTodo } from 'lucide-react';

const Recommendations = ({ recommendations }) => {
  const [activeTab, setActiveTab] = useState('certifications');

  const tabs = [
    { id: 'certifications', label: 'Certifications', icon: Award },
    { id: 'projects', label: 'Projects', icon: Code },
    { id: 'tools', label: 'Tools', icon: Wrench },
    { id: 'priorities', label: 'Priority', icon: ListTodo },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'certifications':
        return recommendations.certifications?.length > 0 ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {recommendations.certifications.map((item, i) => (
              <div key={i} className="bg-bg-dark border border-white/10 p-4 rounded-xl border-l-2 border-l-primary hover:border-l-accent transition-colors">
                <h4 className="font-semibold text-text-primary mb-2 capitalize">{item.skill}</h4>
                <ul className="text-sm text-text-secondary space-y-1 list-disc list-inside">
                  {item.certifications.map((c, j) => <li key={j}>{c}</li>)}
                </ul>
              </div>
            ))}
          </div>
        ) : <p className="text-text-muted text-sm">No specific certification recommendations.</p>;

      case 'projects':
        return recommendations.projects?.length > 0 ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {recommendations.projects.map((item, i) => (
              <div key={i} className="bg-bg-dark border border-white/10 p-4 rounded-xl border-l-2 border-l-accent-orange hover:border-l-accent-warm transition-colors">
                <h4 className="font-semibold text-text-primary mb-2 capitalize">{item.skill}</h4>
                <ul className="text-sm text-text-secondary space-y-1 list-disc list-inside">
                  {item.projects.map((p, j) => <li key={j}>{p}</li>)}
                </ul>
              </div>
            ))}
          </div>
        ) : <p className="text-text-muted text-sm">No specific project recommendations.</p>;

      case 'tools':
        return recommendations.tools?.length > 0 ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {recommendations.tools.map((item, i) => (
              <div key={i} className="bg-bg-dark border border-white/10 p-4 rounded-xl border-l-2 border-l-accent-blue hover:border-l-primary transition-colors">
                <h4 className="font-semibold text-text-primary mb-2 capitalize">{item.skill}</h4>
                <div className="flex flex-wrap gap-2 mt-2">
                  {item.tools.map((t, j) => (
                    <span key={j} className="text-xs px-2 py-1 bg-white/5 rounded-md text-text-secondary">{t}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : <p className="text-text-muted text-sm">No specific tool recommendations.</p>;

      case 'priorities':
        return recommendations.priorities?.length > 0 ? (
          <div className="space-y-3">
            {recommendations.priorities.map((item, i) => {
              let colorClasses = "bg-[#FF6B6B]/10 text-[#FF6B6B] border-[#FF6B6B]/20";
              if (item.rank > 3 && item.rank <= 6) colorClasses = "bg-[#FF9F43]/10 text-[#FF9F43] border-[#FF9F43]/20";
              if (item.rank > 6) colorClasses = "bg-[#00D4AA]/10 text-[#00D4AA] border-[#00D4AA]/20";

              return (
                <div key={i} className="flex items-center justify-between p-3 bg-bg-dark rounded-xl border border-white/5">
                  <div className="flex items-center gap-3">
                    <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold border ${colorClasses}`}>
                      {item.rank}
                    </span>
                    <span className="font-medium text-text-primary capitalize">{item.skill}</span>
                  </div>
                  <div className="text-xs text-text-muted">Score: {item.priority_score}</div>
                </div>
              );
            })}
          </div>
        ) : <p className="text-text-muted text-sm">No missing skills to prioritize.</p>;
        
      default: return null;
    }
  };

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold text-text-primary mb-1">Learning Recommendations</h2>
      <p className="text-sm text-text-muted mb-6">How to bridge your skill gap</p>
      
      <div className="flex gap-2 mb-6 border-b border-white/10 pb-2 overflow-x-auto scrollbar-none">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-colors whitespace-nowrap ${
              activeTab === tab.id ? 'bg-white/10 text-white' : 'text-text-secondary hover:bg-white/5 hover:text-white'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      <div className="min-h-[200px]">
        {renderContent()}
      </div>
    </div>
  );
};

export default Recommendations;
