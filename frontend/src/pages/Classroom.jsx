import { useState } from 'react';
import { Plus, LogIn, Users, Copy, Check, DoorOpen } from 'lucide-react';

export default function Classroom({ setCurrentPage }) {
  const [mode, setMode] = useState(null);
  const [className, setClassName] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [createdCode, setCreatedCode] = useState(null);
  const [copied, setCopied] = useState(false);
  const [joined, setJoined] = useState(null);
  const [classrooms, setClassrooms] = useState([]);

  const generateCode = () => {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let code = '';
    for (let i = 0; i < 6; i++) {
      code += chars[Math.floor(Math.random() * chars.length)];
    }
    return code;
  };

  const handleCreate = (e) => {
    e.preventDefault();
    if (!className.trim()) return;
    const code = generateCode();
    setCreatedCode(code);
    setClassrooms([...classrooms, { id: code, name: className, created: new Date().toISOString() }]);
  };

  const handleJoin = (e) => {
    e.preventDefault();
    if (!joinCode.trim()) return;
    setJoined(joinCode.toUpperCase());
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(createdCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (createdCode) {
    return (
      <div className="classroom-page">
        <div className="classroom-container">
          <div className="classroom-card classroom-success-card">
            <div className="success-check"><DoorOpen size={40} /></div>
            <h2>Classroom Created!</h2>
            <p className="classroom-desc">Share this code with your students to let them join:</p>
            <div className="classroom-code-display">
              <span className="classroom-code-text">{createdCode}</span>
              <button className="btn btn-secondary classroom-code-copy" onClick={handleCopy}>
                {copied ? <Check size={18} /> : <Copy size={18} />}
                {copied ? 'Copied!' : 'Copy'}
              </button>
            </div>
            <p className="classroom-code-hint">Students can use this code in the "Join Classroom" section.</p>
            <div className="classroom-success-actions">
              <button className="btn btn-primary" onClick={() => setCurrentPage('dashboard')}>
                Go to Dashboard
              </button>
              <button className="btn btn-secondary" onClick={() => { setCreatedCode(null); setClassName(''); setMode(null); }}>
                Create Another
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (joined) {
    return (
      <div className="classroom-page">
        <div className="classroom-container">
          <div className="classroom-card classroom-success-card">
            <div className="success-check"><Users size={40} /></div>
            <h2>Joined Classroom!</h2>
            <p className="classroom-desc">You have successfully joined classroom <strong>{joined}</strong>.</p>
            <div className="classroom-success-actions">
              <button className="btn btn-primary" onClick={() => setCurrentPage('dashboard')}>
                Go to Dashboard
              </button>
              <button className="btn btn-secondary" onClick={() => { setJoined(null); setJoinCode(''); setMode(null); }}>
                Join Another
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="classroom-page">
      <div className="classroom-container">
        <div className="section-header text-center">
          <h2 className="section-title">Classroom</h2>
          <p className="section-subtitle">Create a classroom for your students or join one with a code.</p>
        </div>

        {!mode && (
          <div className="classroom-grid">
            <div className="classroom-card card classroom-option" onClick={() => setMode('create')}>
              <div className="classroom-option-icon"><Plus size={32} /></div>
              <h3>Create Classroom</h3>
              <p>Set up a new classroom and get a shareable code for your students.</p>
              <ul className="classroom-option-features">
                <li>✓ Unique classroom code</li>
                <li>✓ Track student progress</li>
                <li>✓ Shared error analytics</li>
              </ul>
            </div>
            <div className="classroom-card card classroom-option" onClick={() => setMode('join')}>
              <div className="classroom-option-icon"><LogIn size={32} /></div>
              <h3>Join Classroom</h3>
              <p>Enter a classroom code shared by your teacher to join an existing class.</p>
              <ul className="classroom-option-features">
                <li>✓ Enter 6-character code</li>
                <li>✓ Access class materials</li>
                <li>✓ Compare with peers</li>
              </ul>
            </div>
          </div>
        )}

        {mode === 'create' && (
          <div className="classroom-card card">
            <button className="classroom-back-btn" onClick={() => setMode(null)}>
              ← Back
            </button>
            <h3 className="classroom-form-title">Create a Classroom</h3>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Classroom name</label>
                <input
                  className="auth-input"
                  type="text"
                  placeholder="e.g. CS101 Spring 2026"
                  value={className}
                  onChange={(e) => setClassName(e.target.value)}
                  required
                />
              </div>
              <button className="btn btn-primary classroom-submit-btn" type="submit">
                <Plus size={18} /> Create Classroom
              </button>
            </form>
          </div>
        )}

        {mode === 'join' && (
          <div className="classroom-card card">
            <button className="classroom-back-btn" onClick={() => setMode(null)}>
              ← Back
            </button>
            <h3 className="classroom-form-title">Join a Classroom</h3>
            <form onSubmit={handleJoin}>
              <div className="form-group">
                <label className="form-label">Classroom code</label>
                <input
                  className="auth-input classroom-code-input"
                  type="text"
                  placeholder="e.g. ABC123"
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value.toUpperCase().slice(0, 6))}
                  maxLength="6"
                  required
                />
              </div>
              <button className="btn btn-primary classroom-submit-btn" type="submit">
                <LogIn size={18} /> Join Classroom
              </button>
            </form>
          </div>
        )}

        {classrooms.length > 0 && mode !== 'create' && !joined && (
          <div className="classroom-list-section">
            <h3>Your Classrooms</h3>
            <div className="classroom-list">
              {classrooms.map((c) => (
                <div className="classroom-list-item" key={c.id}>
                  <div className="classroom-list-info">
                    <span className="classroom-list-name">{c.name}</span>
                    <span className="classroom-list-code">Code: {c.id}</span>
                  </div>
                  <button className="btn btn-secondary classroom-list-copy" onClick={() => { navigator.clipboard.writeText(c.id); }}>
                    <Copy size={14} /> Copy Code
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
