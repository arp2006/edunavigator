import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api } from "../api";

const AuthContext = createContext(null);

function loadUser() {
  const token = localStorage.getItem("eduNavigator_token");
  const userJson = localStorage.getItem("eduNavigator_user");
  if (!token || !userJson) return { token: null, user: null };
  try {
    return { token, user: JSON.parse(userJson) };
  } catch {
    return { token: null, user: null };
  }
}

export function AuthProvider({ children }) {
  const [{ token, user }, setAuthState] = useState(() => loadUser());

  useEffect(() => {
    const current = loadUser();
    setAuthState(current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = async ({ email, password }) => {
    const res = await api.post("/auth/login", { email, password });
    const nextToken = res.data.access_token;
    const userData = {
      id: res.data.access_user,
      stream: res.data.stream,
      profile_id: res.data.profile_id
    };
    localStorage.setItem("eduNavigator_token", nextToken);
    localStorage.setItem("eduNavigator_user", JSON.stringify(userData));
    setAuthState({ token: nextToken, user: userData });
    return res.data;
  };

  const register = async ({ email, password, name, stream }) => {
    const res = await api.post("/auth/signup", { email, password, name, stream });
    const nextToken = res.data.access_token;
    const userData = {
      id: res.data.access_user,
      stream: res.data.stream,
      profile_id: res.data.profile_id
    };
    localStorage.setItem("eduNavigator_token", nextToken);
    localStorage.setItem("eduNavigator_user", JSON.stringify(userData));
    setAuthState({ token: nextToken, user: userData });
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem("eduNavigator_token");
    localStorage.removeItem("eduNavigator_user");
    setAuthState({ token: null, user: null });
  };

  const value = useMemo(
    () => ({ token, user, login, register, logout, isAdmin: user?.role === "admin" }),
    [token, user]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

