import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

export default function SignUp({ setCurrentPage, setUser }) {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!fullName || !email || !password) {
      alert("Please fill in all fields");
      return;
    }
    
    // Set user profile details
    setUser({
      name: fullName,
      email: email
    });
    
    // Proceed to onboarding flow
    setCurrentPage('onboarding-learning');
    window.scrollTo(0, 0);
  };

  const handleGoogleSignup = () => {
    setUser({
      name: "Google Student",
      email: "student@gmail.com"
    });
    setCurrentPage('onboarding-learning');
    window.scrollTo(0, 0);
  };

  return (
    <div className="auth-page-container">
      {/* Centered Logo above the card */}
      <div className="auth-logo-header" onClick={() => setCurrentPage('home')} style={{ cursor: 'pointer' }}>
        <svg width="36" height="36" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 2L36 11V29L20 38L4 29V11L20 2Z" stroke="#5D59D6" strokeWidth="3" strokeLinejoin="round"/>
          <path d="M15 16L11 20L15 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M25 16L29 20L25 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
        <span>Code<span style={{ color: 'var(--brand)' }}>Sage</span></span>
      </div>

      <div className="auth-card">
        <h2>Create your account</h2>
        <p className="auth-subtitle">Join thousands of students improving their code</p>

        <form className="auth-form" onSubmit={handleSubmit}>
          {/* Full Name field */}
          <div className="form-group">
            <label className="form-label" htmlFor="name-input">Full name</label>
            <input
              id="name-input"
              type="text"
              className="auth-input"
              placeholder="John Doe"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
            />
          </div>

          {/* Email field */}
          <div className="form-group">
            <label className="form-label" htmlFor="email-input">Email address</label>
            <input
              id="email-input"
              type="email"
              className="auth-input"
              placeholder="name@company.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* Password field */}
          <div className="form-group">
            <label className="form-label" htmlFor="password-input">Password</label>
            <div className="input-wrapper">
              <input
                id="password-input"
                type={showPassword ? "text" : "password"}
                className="auth-input"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="password-toggle-btn"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <button type="submit" className="btn btn-primary auth-submit-btn">
            Create account
          </button>
        </form>

        <div className="auth-divider">
          <span className="divider-line" />
          <span className="divider-text">OR CONTINUE WITH</span>
          <span className="divider-line" />
        </div>

        <button type="button" className="social-auth-btn" onClick={handleGoogleSignup}>
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22c-.78-2.34-.78-4.74 0-7.08z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62-.03 3.17.53 4.33 1.63L19.5 3.8C17.47 1.9 14.8 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.52z" fill="#EA4335"/>
          </svg>
          Google
        </button>

        <p className="auth-footer-text">
          Already have an account?{' '}
          <span className="auth-link" onClick={() => setCurrentPage('login')}>
            Log in
          </span>
        </p>
      </div>
    </div>
  );
}
