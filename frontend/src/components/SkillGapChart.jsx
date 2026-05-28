import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { motion } from 'framer-motion';

const MotionSpan = motion.span;

const SkillGapChart = ({ gapResult }) => {
  // Format data for Radar Chart
  const allCategories = Array.from(new Set([
    ...Object.keys(gapResult.matched_categorized),
    ...Object.keys(gapResult.missing_categorized)
  ]));

  const radarData = allCategories.map(cat => ({
    subject: cat.replace('Programming ', '').replace('Data Science & ', 'DS/').replace(' & Software', '').slice(0, 15),
    matched: gapResult.matched_categorized[cat]?.length || 0,
    missing: gapResult.missing_categorized[cat]?.length || 0,
    fullMark: Math.max((gapResult.matched_categorized[cat]?.length || 0) + (gapResult.missing_categorized[cat]?.length || 0), 10)
  }));

  // Match Ratio Data
  const pieData = [
    { name: 'Matched', value: gapResult.total_matched, color: '#00D4AA' },
    { name: 'Missing', value: gapResult.total_missing, color: '#FF6B6B' }
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      {/* Charts Column */}
      <div className="card p-6 flex flex-col gap-8">
        <div>
          <h2 className="text-lg font-semibold text-text-primary mb-1">Category Analysis</h2>
          <p className="text-sm text-text-muted mb-4">Resume vs Job Description skills</p>
          <div className="h-[250px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={radarData}>
                <PolarGrid stroke="rgba(108,99,255,0.2)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#A0AEC0', fontSize: 11 }} />
                <Radar name="Matched" dataKey="matched" stroke="#00D4AA" fill="#00D4AA" fillOpacity={0.4} />
                <Radar name="Missing" dataKey="missing" stroke="#FF6B6B" fill="#FF6B6B" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-semibold text-text-primary">Match Ratio</h2>
              <div className="flex gap-4 mt-2">
                <span className="text-sm text-[#00D4AA] font-medium">{gapResult.match_percentage}% Match</span>
                <span className="text-sm text-[#FF6B6B] font-medium">{gapResult.gap_percentage}% Gap</span>
              </div>
            </div>
            <div className="w-24 h-24 relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={30}
                    outerRadius={45}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>

      {/* Skills Lists Column */}
      <div className="card p-6 flex flex-col gap-6">
        <div>
          <h2 className="text-lg font-semibold text-text-primary border-b border-white/10 pb-2 mb-4">
            ✅ Matched Skills ({gapResult.total_matched})
          </h2>
          <div className="flex flex-wrap gap-2">
            {gapResult.matched.length > 0 ? gapResult.matched.map((skill, i) => (
              <MotionSpan
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                key={i} 
                className="px-3 py-1 bg-[#00D4AA]/10 text-[#00D4AA] border border-[#00D4AA]/30 rounded-full text-xs font-semibold"
              >
                {skill}
              </MotionSpan>
            )) : <p className="text-sm text-text-muted">No matched skills found.</p>}
          </div>
        </div>

        <div>
          <h2 className="text-lg font-semibold text-text-primary border-b border-white/10 pb-2 mb-4">
            ❌ Missing Skills ({gapResult.total_missing})
          </h2>
          <div className="flex flex-wrap gap-2">
            {gapResult.missing.length > 0 ? gapResult.missing.map((skill, i) => (
              <MotionSpan
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                key={i} 
                className="px-3 py-1 bg-[#FF6B6B]/10 text-[#FF6B6B] border border-[#FF6B6B]/30 rounded-full text-xs font-semibold"
              >
                {skill}
              </MotionSpan>
            )) : <p className="text-sm text-[#00D4AA]">Your resume covers all required skills! 🎉</p>}
          </div>
        </div>
      </div>
      
    </div>
  );
};

export default SkillGapChart;
