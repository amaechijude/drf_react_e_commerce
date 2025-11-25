"use client";

import { AuthContext } from "@/context/auth-context";
import { useContext } from "react";

// hooks/useAuth.ts
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
