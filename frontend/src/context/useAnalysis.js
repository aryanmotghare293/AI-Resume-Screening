import { useContext } from 'react';
import AnalysisContext from './analysisContextCore';

export const useAnalysis = () => useContext(AnalysisContext);
