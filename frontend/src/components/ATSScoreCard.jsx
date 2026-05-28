import { motion } from 'framer-motion';

const MotionCircle = motion.circle;

const ATSScoreCard = ({ atsResult }) => {
  const score = atsResult.total_score;
  const verdict = atsResult.verdict;

  // Determine color based on score
  let strokeColor = '#FF6B6B'; // Red
  let bgColor = 'rgba(255, 107, 107, 0.1)';
  if (score >= 75) {
    strokeColor = '#00D4AA'; // Green
    bgColor = 'rgba(0, 212, 170, 0.1)';
  } else if (score >= 50) {
    strokeColor = '#FF9F43'; // Orange
    bgColor = 'rgba(255, 159, 67, 0.1)';
  }

  // Circular gauge SVG calculation
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="card p-6 h-full flex flex-col items-center justify-center text-center">
      <h2 className="text-lg font-semibold text-text-primary mb-6">ATS Compatibility</h2>
      
      <div className="relative w-48 h-48 mb-6">
        <svg className="w-full h-full transform -rotate-90">
          <circle
            cx="96"
            cy="96"
            r={radius}
            stroke="#2D3748"
            strokeWidth="12"
            fill="transparent"
          />
          <MotionCircle
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            cx="96"
            cy="96"
            r={radius}
            stroke={strokeColor}
            strokeWidth="12"
            fill="transparent"
            strokeDasharray={circumference}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-bold tracking-tight text-white">
            {score}%
          </span>
        </div>
      </div>

      <div 
        className="px-4 py-1.5 rounded-full text-sm font-semibold mb-4 border"
        style={{ color: strokeColor, backgroundColor: bgColor, borderColor: `${strokeColor}40` }}
      >
        {verdict.label}
      </div>
      
      <p className="text-sm text-text-secondary leading-relaxed">
        {verdict.recommendation}
      </p>
    </div>
  );
};

export default ATSScoreCard;
