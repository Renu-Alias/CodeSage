import { useState } from 'react';
import { Plus, LogIn, Users, Copy, Check, DoorOpen, Calendar, FileText, AlertCircle, ArrowLeft } from 'lucide-react';

function SkeletonBlock({ lines = 3 }) {
  return (
    <div className="skeleton-block">
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="skeleton-line" style={{ width: `${70 + Math.random() * 30}%` }} />
      ))}
    </div>
  );
}

export default function Classroom({ setCurrentPage }) {
  const [mode, setMode] = useState(null);
  const [className, setClassName] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [copied, setCopied] = useState(false);
  const [classrooms, setClassrooms] = useState([]);
  const [selectedClassroom, setSelectedClassroom] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [detailData, setDetailData] = useState(null);

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
    setClassrooms([...classrooms, {
      id: code,
      name: className,
      created: new Date().toISOString(),
      role: 'teacher',
      memberCount: 1,
    }]);
    setClassName('');
    setMode(null);
  };

  const handleJoin = (e) => {
    e.preventDefault();
    if (!joinCode.trim()) return;
    const code = joinCode.toUpperCase();
    const exists = classrooms.some(c => c.id === code);
    if (!exists) {
      setClassrooms([...classrooms, {
        id: code,
        name: `Classroom ${code}`,
        created: new Date().toISOString(),
        role: 'student',
        memberCount: 0,
      }]);
    }
    setJoinCode('');
    setMode(null);
  };

  const handleCopy = (code) => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleCardClick = (c) => {
    setSelectedClassroom(c);
    setLoadingDetail(true);
    setDetailData(null);

    setTimeout(() => {
      setDetailData({
        actions: [
          { id: 1, desc: 'Analyzed bubble_sort.py — 3 bugs found', date: '2026-06-08', type: 'analysis' },
          { id: 2, desc: 'Completed exercise "Recursion Basics"', date: '2026-06-07', type: 'exercise' },
          { id: 3, desc: 'Submitted merge_sort.py for review', date: '2026-06-06', type: 'submission' },
          { id: 4, desc: 'Scored 85% on Arrays quiz', date: '2026-06-05', type: 'quiz' },
        ],
        tasks: [
          { id: 1, title: 'Fix off-by-one in binary search', due: '2026-06-15', priority: 'high', status: 'pending' },
          { id: 2, title: 'Implement quicksort (divide & conquer)', due: '2026-06-20', priority: 'medium', status: 'pending' },
          { id: 3, title: 'Read chapter on dynamic programming', due: '2026-06-25', priority: 'low', status: 'pending' },
        ],
        dues: [
          { id: 1, title: 'Project 1: Sorting Visualizer', due: '2026-06-30', submissions: 12 },
          { id: 2, title: 'Quiz 2: Data Structures', due: '2026-06-18', submissions: 8 },
        ],
      });
      setLoadingDetail(false);
    }, 1200);
  };

  if (selectedClassroom && !loadingDetail && detailData) {
    return (
      <div className="classroom-page">
        <div className="classroom-container">
          <button className="classroom-back-btn" onClick={() => { setSelectedClassroom(null); setDetailData(null); }}>
            <ArrowLeft size={16} /> Back to Classrooms
          </button>

          <div className="classroom-detail-header">
            <div className="classroom-detail-avatar">
              <Users size={28} />
            </div>
            <div>
              <h2 className="classroom-detail-name">{selectedClassroom.name}</h2>
              <p className="classroom-detail-meta">
                Code: <strong>{selectedClassroom.id}</strong> · {selectedClassroom.role === 'teacher' ? 'Teacher' : 'Student'} · {selectedClassroom.memberCount} member{selectedClassroom.memberCount !== 1 ? 's' : ''}
              </p>
            </div>
          </div>

          <div className="classroom-detail-grid">
            <div className="classroom-detail-section">
              <h3><Calendar size={16} /> Recent Actions</h3>
              <div className="classroom-action-list">
                {detailData.actions.map(a => (
                  <div key={a.id} className="classroom-action-item">
                    <span className={`classroom-action-type classroom-action-type--${a.type}`} />
                    <div className="classroom-action-info">
                      <span className="classroom-action-desc">{a.desc}</span>
                      <span className="classroom-action-date">{a.date}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="classroom-detail-section">
              <h3><FileText size={16} /> Tasks Assigned</h3>
              <div className="classroom-tasks-list">
                {detailData.tasks.map(t => (
                  <div key={t.id} className={`classroom-task-item classroom-task--${t.priority}`}>
                    <div className="classroom-task-info">
                      <span className="classroom-task-title">{t.title}</span>
                      <span className="classroom-task-due">Due: {t.due}</span>
                    </div>
                    <span className={`classroom-task-badge classroom-task-badge--${t.status}`}>{t.status}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="classroom-detail-section classroom-detail-section--full">
              <h3><AlertCircle size={16} /> Upcoming Dues</h3>
              <div className="classroom-dues-list">
                {detailData.dues.map(d => (
                  <div key={d.id} className="classroom-due-item">
                    <div className="classroom-due-info">
                      <span className="classroom-due-title">{d.title}</span>
                      <span className="classroom-due-date">Due: {d.due}</span>
                    </div>
                    <span className="classroom-due-submissions">{d.submissions} submissions</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (selectedClassroom && loadingDetail) {
    return (
      <div className="classroom-page">
        <div className="classroom-container">
          <button className="classroom-back-btn" onClick={() => { setSelectedClassroom(null); setDetailData(null); setLoadingDetail(false); }}>
            <ArrowLeft size={16} /> Back to Classrooms
          </button>

          <div className="classroom-detail-header">
            <div className="classroom-detail-avatar skeleton-pulse" />
            <div style={{ flex: 1 }}>
              <div className="skeleton-line" style={{ width: '40%', height: '24px', marginBottom: '8px' }} />
              <div className="skeleton-line" style={{ width: '60%', height: '14px' }} />
            </div>
          </div>

          <div className="classroom-detail-grid">
            {[1, 2, 3].map(i => (
              <div key={i} className="classroom-detail-section">
                <div className="skeleton-line" style={{ width: '50%', height: '18px', marginBottom: '16px' }} />
                <SkeletonBlock lines={4} />
              </div>
            ))}
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

        <div className="classroom-action-bar">
          <button className="btn btn-primary" onClick={() => setMode(mode === 'create' ? null : 'create')}>
            <Plus size={18} /> Create Classroom
          </button>
          <button className="btn btn-secondary" onClick={() => setMode(mode === 'join' ? null : 'join')}>
            <LogIn size={18} /> Join Classroom
          </button>
        </div>

        {mode === 'create' && (
          <div className="classroom-card card">
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

        <div className="classroom-list-section">
          <h3>Your Classrooms</h3>
          {classrooms.length === 0 ? (
            <div className="classroom-empty">
              <Users size={48} />
              <p>No classrooms yet. Create one or join with a code.</p>
            </div>
          ) : (
            <div className="classroom-cards-grid">
              {classrooms.map((c) => (
                <div key={c.id} className="classroom-card-item card" onClick={() => handleCardClick(c)}>
                  <div className="classroom-card-header">
                    <div className="classroom-card-avatar">
                      <Users size={24} />
                    </div>
                    <div className="classroom-card-role">{c.role === 'teacher' ? 'Teacher' : 'Student'}</div>
                  </div>
                  <h4 className="classroom-card-name">{c.name}</h4>
                  <p className="classroom-card-code">Code: {c.id}</p>
                  <p className="classroom-card-meta">{c.memberCount} member{c.memberCount !== 1 ? 's' : ''}</p>
                  <div className="classroom-card-actions">
                    <button className="btn btn-secondary classroom-card-copy"
                      onClick={(e) => { e.stopPropagation(); handleCopy(c.id); }}>
                      {copied ? <Check size={14} /> : <Copy size={14} />}
                      {copied ? 'Copied' : 'Copy Code'}
                    </button>
                    <span className="classroom-card-click">Click to view details →</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
