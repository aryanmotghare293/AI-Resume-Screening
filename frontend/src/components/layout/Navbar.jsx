import { Link } from 'react-router-dom';
import { Target } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="border-b border-white/10 bg-bg-dark/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="p-2 bg-primary/10 rounded-lg group-hover:bg-primary/20 transition-colors">
              <Target className="w-6 h-6 text-primary" />
            </div>
            <span className="font-bold text-xl tracking-tight">
              AI <span className="gradient-text">Screener</span>
            </span>
          </Link>
          <div className="flex items-center gap-4">
            <a 
              href="https://github.com/" 
              target="_blank" 
              rel="noreferrer"
              className="text-text-secondary hover:text-white transition-colors text-sm font-medium"
            >
              GitHub
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
