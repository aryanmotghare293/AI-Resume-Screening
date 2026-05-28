import { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const ResumePreview = ({ resumeData }) => {
  const [openSection, setOpenSection] = useState(null);

  const sections = [
    { id: 'name', title: 'Name', content: resumeData.name },
    { id: 'contact', title: 'Contact Info', content: JSON.stringify(resumeData.contact, null, 2) },
    { id: 'summary', title: 'Summary', content: resumeData.summary },
    { id: 'skills', title: 'Skills', content: resumeData.skills },
    { id: 'education', title: 'Education', content: resumeData.education },
    { id: 'experience', title: 'Experience', content: resumeData.experience },
    { id: 'projects', title: 'Projects', content: resumeData.projects },
  ];

  return (
    <div className="card overflow-hidden">
      <div className="p-4 border-b border-white/10 bg-black/20">
        <h2 className="font-semibold text-text-primary">Parsed Resume Data</h2>
      </div>
      <div>
        {sections.map((sec) => (
          <div key={sec.id} className="border-b border-white/5 last:border-0">
            <button
              onClick={() => setOpenSection(openSection === sec.id ? null : sec.id)}
              className="w-full flex items-center justify-between p-4 hover:bg-white/5 transition-colors text-left"
            >
              <span className="font-medium text-text-secondary">{sec.title}</span>
              {openSection === sec.id ? <ChevronUp className="w-4 h-4 text-text-muted" /> : <ChevronDown className="w-4 h-4 text-text-muted" />}
            </button>
            {openSection === sec.id && (
              <div className="p-4 bg-black/20 text-sm text-text-muted whitespace-pre-wrap font-mono">
                {sec.content || 'Not found.'}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ResumePreview;
