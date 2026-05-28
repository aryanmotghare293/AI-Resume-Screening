import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const COLORS = ['#6C63FF', '#54A0FF', '#00D4AA', '#FF9F43', '#FF6B6B'];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-bg-card border border-white/10 p-3 rounded-lg shadow-xl">
        <p className="font-medium text-white">{payload[0].payload.originalKey}</p>
        <p className="text-primary font-bold">{payload[0].value}%</p>
      </div>
    );
  }
  return null;
};

const ScoreBreakdown = ({ breakdown }) => {
  // Format data for Recharts
  const data = Object.entries(breakdown).map(([key, value]) => {
    // Extract base name without percentage text
    const name = key.replace(/\s\(\d+%\)/, '');
    return { name, score: value, originalKey: key };
  });

  return (
    <div className="card p-6 h-full">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-text-primary">Score Breakdown</h2>
        <p className="text-sm text-text-muted">Weighted component analysis</p>
      </div>
      
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
            barSize={20}
          >
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis 
              type="category" 
              dataKey="name" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: '#FAFAFA', fontSize: 12 }} 
            />
            <Tooltip cursor={{ fill: 'rgba(255,255,255,0.05)' }} content={<CustomTooltip />} />
            <Bar dataKey="score" radius={[0, 4, 4, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ScoreBreakdown;
