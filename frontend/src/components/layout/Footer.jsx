const Footer = () => {
  return (
    <footer className="border-t border-white/5 py-8 mt-12 bg-bg-dark">
      <div className="max-w-7xl mx-auto px-4 text-center">
        <p className="text-text-muted text-sm">
          Built with ❤️ using React, Tailwind CSS, Recharts & Google Gemini AI
        </p>
        <p className="text-text-muted/60 text-xs mt-2">
          © {new Date().getFullYear()} AI Resume Screener — All Rights Reserved
        </p>
      </div>
    </footer>
  );
};

export default Footer;
