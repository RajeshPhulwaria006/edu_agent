import axios from "axios";
const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});
export const getStudents = () => API.get("/students/");
export const getStudent = id => API.get(`/students/${id}`);
export const getPerformance = id => API.get(`/performance/${id}`);
export const getAnalysis = id => API.get(`/performance/${id}/analysis`);
export const getAIAdvice = id => API.get(`/ai/advisor/${id}`);
export const createStudent = data => API.post("/students/", data);
export const deleteStudent = id => API.delete(`/students/${id}`);
export const addPerformance = data => API.post("/performance/", data);
