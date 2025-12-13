import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { GraduationCap, ShieldCheck, LogIn, Loader } from 'lucide-react';
import './Login.css';

const Login = () => {
  const { login } = useAuth();
  const [role, setRole] = useState('student');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login({ username, password, role });

    if (!result.success) {
      setError(result.error);
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="login-shape"></div>
        <div className="login-shape"></div>
      </div>

      <div className="login-card">
        <div className="login-header">
          <h1 className="login-title">CampusOps AI</h1>
          <p className="login-subtitle">Policy-Driven Campus Assistant</p>
        </div>

        <div className="role-selector">
          <button
            className={`role-button ${role === 'student' ? 'active' : ''}`}
            onClick={() => {
              setRole('student');
              setUsername('student');
              setPassword('student123');
              setError('');
            }}
          >
            <GraduationCap size={20} />
            <span>Student</span>
          </button>
          <button
            className={`role-button ${role === 'admin' ? 'active' : ''}`}
            onClick={() => {
              setRole('admin');
              setUsername('admin');
              setPassword('admin123');
              setError('');
            }}
          >
            <ShieldCheck size={20} />
            <span>Admin</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              className="input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder={`Enter ${role} username`}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              className="input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          {error && (
            <div className="error-message fade-in">
              {error}
            </div>
          )}

          <button type="submit" className="btn btn-primary login-button" disabled={loading}>
            {loading ? (
              <>
                <Loader size={18} className="spin" />
                <span>Signing in...</span>
              </>
            ) : (
              <>
                <LogIn size={18} />
                <span>Sign In</span>
              </>
            )}
          </button>
        </form>

        <div className="demo-credentials">
          <p className="demo-title">Demo Credentials:</p>
          <div className="demo-grid">
            <div className="demo-item">
              <strong>Student:</strong> student / student123
            </div>
            <div className="demo-item">
              <strong>Admin:</strong> admin / admin123
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

