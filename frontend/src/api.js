import axios from "axios";

const apiBase =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: apiBase,
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("eduNavigator_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

