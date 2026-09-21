import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, MerchantWorkspace, AuthResponse } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  activeWorkspace: MerchantWorkspace | null;
  workspaces: MerchantWorkspace[];
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
  setActiveWorkspace: (ws: MerchantWorkspace) => void;
  refreshWorkspaces: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const API_BASE = import.meta.env.VITE_API_URL ?? '';

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('ctl_auth_token'));
  const [workspaces, setWorkspaces] = useState<MerchantWorkspace[]>([]);
  const [activeWorkspace, setActiveWorkspace] = useState<MerchantWorkspace | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const fetchWorkspaces = async (authToken: string) => {
    try {
      const res = await fetch(`${API_BASE}/api/workspaces`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });
      if (res.ok) {
        const data: MerchantWorkspace[] = await res.json();
        setWorkspaces(data);
        if (data.length > 0) {
          // Keep current if still valid, or default to first
          setActiveWorkspace((prev) => {
            const found = data.find((w) => w.id === prev?.id);
            return found || data[0];
          });
        }
      }
    } catch (err) {
      console.error('Failed to fetch workspaces', err);
    }
  };

  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem('ctl_auth_token');
      if (savedToken) {
        try {
          const res = await fetch(`${API_BASE}/api/auth/me`, {
            headers: { Authorization: `Bearer ${savedToken}` },
          });
          if (res.ok) {
            const userData = await res.json();
            setUser(userData);
            setToken(savedToken);
            await fetchWorkspaces(savedToken);
          } else {
            localStorage.removeItem('ctl_auth_token');
            setToken(null);
            setUser(null);
          }
        } catch {
          // If offline or network issue, maintain local state if desired or clear
        }
      }
      setIsLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Login failed. Please check your credentials.');
      }
      const data: AuthResponse = await res.json();
      localStorage.setItem('ctl_auth_token', data.access_token);
      setToken(data.access_token);
      setUser(data.user);
      await fetchWorkspaces(data.access_token);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (email: string, password: string, fullName: string = '') => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, full_name: fullName }),
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Registration failed. Email may already be registered.');
      }
      const data: AuthResponse = await res.json();
      localStorage.setItem('ctl_auth_token', data.access_token);
      setToken(data.access_token);
      setUser(data.user);
      await fetchWorkspaces(data.access_token);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('ctl_auth_token');
    setToken(null);
    setUser(null);
    setWorkspaces([]);
    setActiveWorkspace(null);
  };

  const refreshWorkspaces = async () => {
    if (token) {
      await fetchWorkspaces(token);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        activeWorkspace,
        workspaces,
        isLoading,
        login,
        register,
        logout,
        setActiveWorkspace,
        refreshWorkspaces,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
