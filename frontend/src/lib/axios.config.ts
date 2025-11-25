import axios from "axios";

export const baseUrl: string = "http://localhost:8000";

export const axiosInstance = axios.create({
  baseURL: baseUrl,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});
