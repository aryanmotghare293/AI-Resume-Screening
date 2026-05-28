import { useReducer } from 'react';
import AnalysisContext from './analysisContextCore';

const initialState = {
  isAnalyzing: false,
  isAnalyzed: false,
  error: null,
  resumeData: null,
  resumeSkills: [],
  resumeSkillsCategorized: {},
  jdSkills: [],
  atsResult: null,
  gapResult: null,
  recommendations: null,
  targetRole: 'Data Scientist',
};

const analysisReducer = (state, action) => {
  switch (action.type) {
    case 'START_ANALYSIS':
      return { ...state, isAnalyzing: true, error: null };
    case 'ANALYSIS_SUCCESS':
      return {
        ...state,
        isAnalyzing: false,
        isAnalyzed: true,
        ...action.payload,
      };
    case 'ANALYSIS_ERROR':
      return { ...state, isAnalyzing: false, error: action.payload };
    case 'RESET_ANALYSIS':
      return { ...initialState, targetRole: state.targetRole };
    case 'SET_TARGET_ROLE':
      return { ...state, targetRole: action.payload };
    default:
      return state;
  }
};

export const AnalysisProvider = ({ children }) => {
  const [state, dispatch] = useReducer(analysisReducer, initialState);

  return (
    <AnalysisContext.Provider value={{ state, dispatch }}>
      {children}
    </AnalysisContext.Provider>
  );
};
