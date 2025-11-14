import axios from "axios";

const baseUrl: string =
  process.env.NEXT_PUPLIC_API_URL || "http://127.0.0.1:8000";

const axiosInstance = axios.create({
  baseURL: baseUrl,
  timeout: 10_000,
});

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("token") as string | null;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default axiosInstance;
