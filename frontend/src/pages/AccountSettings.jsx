import React, { useState } from 'react';
import { User, Mail, Lock, ChevronLeft, Check, Eye, EyeOff, Sprout, Terminal, Sun, Moon } from 'lucide-react';
import { useTheme } from '../ThemeContext.jsx';

export default function AccountSettings({ setCurrentPage }) {
  const { theme, setTheme } = useTheme();
  const [name, setName] = useState('Student Name');
  const [email, setEmail] = useState('student@example.com');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [skillLevel, setSkillLevel] = useState('Beginner');
  const [showCurPw, setShowCurPw] = useState(false);
  const [showNewPw, setShowNewPw] = useState(false);
  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  return (
    <div className="account-settings-page animate-fade container">
      <div className="settings-header-row">
        <button className="btn btn-back" onClick={() => setCurrentPage('dashboard')}>
          <ChevronLeft size={18} /> Back to Dashboard
        </button>
        <h2>Account Settings</h2>
      </div>

      <div className="settings-card card">
        <div className="settings-avatar-section">
          <div className="settings-avatar">
            <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100" alt="Avatar" />
            <div className="settings-avatar-overlay">Change</div>
          </div>
          <div>
            <h3>{name}</h3>
            <p className="text-muted">{email}</p>
          </div>
        </div>

        <form className="settings-form" onSubmit={handleSave}>
          <div className="form-group">
            <label className="form-label">Full name</label>
            <div className="input-wrapper">
              <User size={16} className="input-icon" />
              <input
                className="auth-input input-with-icon"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Email</label>
            <div className="input-wrapper">
              <Mail size={16} className="input-icon" />
              <input
                className="auth-input input-with-icon"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <hr className="settings-divider" />

          <h4 className="settings-section-title">Change password</h4>

          <div className="form-group">
            <label className="form-label">Current password</label>
            <div className="input-wrapper">
              <Lock size={16} className="input-icon" />
              <input
                className="auth-input input-with-icon"
                type={showCurPw ? 'text' : 'password'}
                placeholder="Enter current password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
              />
              <button type="button" className="password-toggle-btn" onClick={() => setShowCurPw(!showCurPw)}>
                {showCurPw ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">New password</label>
            <div className="input-wrapper">
              <Lock size={16} className="input-icon" />
              <input
                className="auth-input input-with-icon"
                type={showNewPw ? 'text' : 'password'}
                placeholder="Enter new password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <button type="button" className="password-toggle-btn" onClick={() => setShowNewPw(!showNewPw)}>
                {showNewPw ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <hr className="settings-divider" />

          <h4 className="settings-section-title">Learning preferences</h4>

          <div className="form-group">
            <label className="form-label">Skill level</label>
            <div className="settings-level-options">
              <div
                className={`settings-level-option ${skillLevel === 'Beginner' ? 'active' : ''}`}
                onClick={() => setSkillLevel('Beginner')}
              >
                <Sprout size={18} />
                Beginner
              </div>
              <div
                className={`settings-level-option ${skillLevel === 'Intermediate' ? 'active' : ''}`}
                onClick={() => setSkillLevel('Intermediate')}
              >
                <Terminal size={18} />
                Intermediate
              </div>
            </div>
          </div>

          <hr className="settings-divider" />

          <h4 className="settings-section-title">Appearance</h4>

          <div className="form-group">
            <label className="form-label">Theme</label>
            <div className="settings-level-options">
              <div
                className={`settings-level-option ${theme === 'light' ? 'active' : ''}`}
                onClick={() => setTheme('light')}
              >
                <Sun size={18} />
                Light mode
              </div>
              <div
                className={`settings-level-option ${theme === 'dark' ? 'active' : ''}`}
                onClick={() => setTheme('dark')}
              >
                <Moon size={18} />
                Dark mode
              </div>
            </div>
          </div>

          <div className="settings-actions">
            <button type="submit" className="btn btn-primary">
              {saved ? <><Check size={16} /> Saved!</> : 'Save changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
