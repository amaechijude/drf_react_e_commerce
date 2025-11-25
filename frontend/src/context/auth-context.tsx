"use client";

import React, { createContext, useState, useEffect } from "react";
import { axiosInstance } from "@/lib/axios.config";
import { LoginSchema } from "../components/auth/login-form";

interface User {
  id: number;
  email: string;
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isLoggedIn: boolean;
  login: (data: LoginSchema) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Check authentication status on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axiosInstance.get("api/auth/user");
      setUser(response.data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (data: LoginSchema) => {
    const response = await axiosInstance.post("api/auth/login", data);
    setUser(response.data.user);
  };

  const logout = async () => {
    await axiosInstance.post("api/auth/logout");
    setUser(null);
  };

  // const register = async () => {
  //   await axiosInstance.post("api/reg")
  // }

  const isLoggedIn = !!user;

  return (
    <AuthContext.Provider
      value={{ user, loading, isLoggedIn, login, logout, checkAuth }}
    >
      {children}
    </AuthContext.Provider>
  );
}
