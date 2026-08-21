import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// Configure axios to always send and receive secure HttpOnly cookies
axios.defaults.withCredentials = true;

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('agent_token') || '');
  const [loading, setLoading] = useState(true);

  // Sync token to axios headers if available
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
  }

  // Intercept 401s to perform silent token refresh
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        if (
          error.response &&
          error.response.status === 401 &&
          !originalRequest._retry &&
          !originalRequest.url.includes('/api/auth/login') &&
          !originalRequest.url.includes('/api/auth/register') &&
          !originalRequest.url.includes('/api/auth/refresh')
        ) {
          originalRequest._retry = true;
          try {
            const refreshRes = await axios.post('/api/auth/refresh');
            if (refreshRes.data && refreshRes.data.token) {
              setToken(refreshRes.data.token);
              localStorage.setItem('agent_token', refreshRes.data.token);
              axios.defaults.headers.common['Authorization'] = `Bearer ${refreshRes.data.token}`;
              originalRequest.headers['Authorization'] = `Bearer ${refreshRes.data.token}`;
              return axios(originalRequest);
            }
          } catch (refreshErr) {
            localStorage.removeItem('agent_token');
            setToken('');
            setUser(null);
          }
        }
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  // Fetch current authenticated user on load or token change
  useEffect(() => {
    const fetchMe = async () => {
      try {
        const res = await axios.get('/api/auth/me');
        setUser(res.data);
      } catch (err) {
        // Try refreshing if access token expired
        try {
          const refreshRes = await axios.post('/api/auth/refresh');
          if (refreshRes.data && refreshRes.data.token) {
            setToken(refreshRes.data.token);
            localStorage.setItem('agent_token', refreshRes.data.token);
            const userRes = await axios.get('/api/auth/me');
            setUser(userRes.data);
            return;
          }
        } catch (e) {
          localStorage.removeItem('agent_token');
          setToken('');
          setUser(null);
        }
      } finally {
        setLoading(false);
      }
    };
    fetchMe();
  }, []);

  const login = async (email, password, rememberMe = false) => {
    const res = await axios.post('/api/auth/login', {
      email,
      password,
      remember_me: rememberMe
    });
    if (res.data.token) {
      localStorage.setItem('agent_token', res.data.token);
      setToken(res.data.token);
      setUser(res.data.user);
      return res.data;
    }
  };

  const register = async (name, email, password) => {
    const res = await axios.post('/api/auth/register', { name, email, password });
    if (res.data.token) {
      localStorage.setItem('agent_token', res.data.token);
      setToken(res.data.token);
      setUser(res.data.user);
      return res.data;
    }
  };

  const logout = async () => {
    try {
      await axios.post('/api/auth/logout');
    } catch (e) {
      // Ignore network errors on logout
    }
    localStorage.removeItem('agent_token');
    setToken('');
    setUser(null);
  };

  const logoutAll = async () => {
    try {
      await axios.post('/api/auth/logout-all');
    } catch (e) {
      // Ignore errors
    }
    localStorage.removeItem('agent_token');
    setToken('');
    setUser(null);
  };

  const getSessions = async () => {
    const res = await axios.get('/api/auth/sessions');
    return res.data;
  };

  const revokeSession = async (sessionId) => {
    const res = await axios.delete(`/api/auth/sessions/${sessionId}`);
    return res.data;
  };

  const getAuditLogs = async () => {
    const res = await axios.get('/api/audit-logs');
    return res.data;
  };

  const deleteAccount = async () => {
    const res = await axios.delete('/api/account/me');
    localStorage.removeItem('agent_token');
    setToken('');
    setUser(null);
    return res.data;
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
        logoutAll,
        getSessions,
        revokeSession,
        getAuditLogs,
        deleteAccount
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
