import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
});

export const analyzeResume = async (resumeFile, jdText, targetRole) => {
  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('jd_text', jdText);
  formData.append('target_role', targetRole);

  const response = await api.post('/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  const data = response.data;
  return {
    resumeData: data.resume_data,
    resumeSkills: data.resume_skills,
    resumeSkillsCategorized: data.resume_skills_categorized,
    jdSkills: data.jd_skills,
    atsResult: data.ats_result,
    gapResult: data.gap_result,
    recommendations: data.recommendations,
    targetRole: data.target_role,
    jdText: jdText, // Save the job description text into the state as well
  };
};

export const getAiSuggestions = async (resumeText, jdText) => {
  const response = await api.post('/ai-suggestions', {
    resume_text: resumeText,
    jd_text: jdText,
  });
  return response.data;
};

export const getInterviewQuestions = async (skills, projects, targetRole, missingSkills) => {
  const response = await api.post('/interview-questions', {
    skills,
    projects,
    target_role: targetRole,
    missing_skills: missingSkills,
  });
  return response.data;
};

export const getCareerRoadmap = async (resumeData, targetRole) => {
  const response = await api.post('/career-roadmap', {
    resume_data: resumeData,
    target_role: targetRole,
  });
  return response.data;
};

export default api;
