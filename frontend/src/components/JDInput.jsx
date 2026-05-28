import { FileText } from 'lucide-react';

const JDInput = ({ jdText, setJdText }) => {
  return (
    <div className="flex flex-col gap-2 w-full h-full">
      <div className="flex items-center gap-2 mb-1">
        <FileText className="w-4 h-4 text-primary" />
        <label className="text-sm font-semibold text-text-primary">Job Description</label>
      </div>
      <textarea
        value={jdText}
        onChange={(e) => setJdText(e.target.value)}
        placeholder="Paste the full job description here..."
        className="glass-input w-full p-4 min-h-[200px] flex-grow resize-none text-sm leading-relaxed"
      />
      <div className="text-xs text-text-muted text-right mt-1">
        {jdText.length} characters
      </div>
    </div>
  );
};

export default JDInput;
