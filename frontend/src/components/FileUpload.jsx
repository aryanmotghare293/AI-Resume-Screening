import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File as FileIcon, X } from 'lucide-react';

const FileUpload = ({ file, setFile }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles?.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, [setFile]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1,
    multiple: false
  });

  if (file) {
    return (
      <div className="card p-6 flex items-center justify-between bg-primary/5 border-primary/30">
        <div className="flex items-center gap-4 truncate">
          <div className="p-3 bg-primary/20 rounded-xl text-primary">
            <FileIcon className="w-6 h-6" />
          </div>
          <div className="truncate">
            <p className="text-sm font-semibold text-text-primary truncate">{file.name}</p>
            <p className="text-xs text-text-muted">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
        </div>
        <button 
          onClick={(e) => { e.stopPropagation(); setFile(null); }}
          className="p-2 hover:bg-white/10 rounded-lg transition-colors text-text-secondary hover:text-accent-warm"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    );
  }

  return (
    <div 
      {...getRootProps()} 
      className={`card p-8 border-2 border-dashed flex flex-col items-center justify-center text-center cursor-pointer transition-colors
        ${isDragActive ? 'border-primary bg-primary/10 scale-[1.02]' : 'border-white/20 hover:border-primary/50 hover:bg-white/5'}
        ${isDragReject ? 'border-accent-warm bg-accent-warm/10' : ''}
      `}
    >
      <input {...getInputProps()} />
      <div className="p-4 bg-primary/10 rounded-full mb-4">
        <UploadCloud className={`w-8 h-8 ${isDragActive ? 'text-primary' : 'text-text-muted'}`} />
      </div>
      <p className="font-medium text-text-primary mb-1">
        {isDragActive ? "Drop resume here..." : "Click or drag resume to upload"}
      </p>
      <p className="text-sm text-text-muted">Supports PDF and DOCX</p>
    </div>
  );
};

export default FileUpload;
