import React, { useState, useEffect } from 'react';
import { Search, Download, Flame, Rocket, Award, Bug, Play, HelpCircle, ChevronRight, User, Mail, Calendar } from 'lucide-react';
import { LANGUAGES } from '../constants/languages';

export default function Dashboard({ setCurrentPage, setSampleCode }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [langFilter, setLangFilter] = useState("All");
  const [loading, setLoading] = useState(true);

  // Dashboard Data State
  const [metrics, setMetrics] = useState({
    totalUploads: 47,
    errorsFound: 128,
    errorsThisWeek: 12,
    errorsThisWeekChange: "-8%",
    topLanguage: "Python"
  });

  const [uploads, setUploads] = useState([
    {
      id: "1",
      filename: "calculate_average.py",
      language: "Python",
      timestamp: "2 hours ago",
      errors_count: 2,
      code: "def calculate_average(numbers):\n    total = sum(numbers)\n    # Bug: division without zero check\n    return total / len(numbers)"
    },
    {
      id: "2",
      filename: "auth_handler.js",
      language: "JavaScript",
      timestamp: "5 hours ago",
      errors_count: 4,
      code: "function verifyUser(user) {\n  const token = user.token;\n  if(!token) return null\n  return jwt.decode(token)\n}"
    },
    {
      id: "3",
      filename: "data_processor.py",
      language: "Python",
      timestamp: "Yesterday",
      errors_count: 1,
      code: "def process_data(data):\n    # Potential TypeError\n    return [d * 2.5 for d in data]"
    },
    {
      id: "4",
      filename: "api_endpoints.py",
      language: "Python",
      timestamp: "2 days ago",
      errors_count: 7,
      code: "def get_items(req):\n    res = db.fetch_all()\n    return res"
    },
    {
      id: "5",
      filename: "utils_test.js",
      language: "JavaScript",
      timestamp: "3 days ago",
      errors_count: 2,
      code: "test('math', () => {\n  expect(sum(1, 2)).toBe(3)\n})"
    }
  ]);

  const [weaknessReport, setWeaknessReport] = useState([
    { topic: "Loop logic", count: 23, badge: "PRACTICE THIS" },
    { topic: "Null / zero handling", count: 14, badge: "PRACTICE THIS" },
    { topic: "Variable scoping", count: 8, badge: "PRACTICE THIS" }
  ]);

  const [badges, setBadges] = useState([
    { id: "first_upload", name: "First upload", icon: "rocket", unlocked: true },
    { id: "uploads_10", name: "10 uploads", icon: "award", unlocked: true },
    { id: "week_streak", name: "Week streak", icon: "flame", unlocked: true },
    { id: "bug_hunter", name: "Bug hunter", icon: "bug", unlocked: false }
  ]);

  const [errorsOverTime, setErrorsOverTime] = useState([
    { week: "Week 1", errors: 50 },
    { week: "Week 2", errors: 45 },
    { week: "Week 3", errors: 35 },
    { week: "Week 4", errors: 25 },
    { week: "Week 5", errors: 20 },
    { week: "Week 6", errors: 18 },
    { week: "Week 7", errors: 15 },
    { week: "Week 8", errors: 12 }
  ]);

  // Fetch data from FastAPI backend
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/dashboard`);
        if (res.ok) {
          const data = await res.json();
          setMetrics(data.metrics);
          setUploads(data.recentUploads);
          setWeaknessReport(data.weaknessReport);
          setBadges(data.badges);
          setErrorsOverTime(data.errorsOverTime);
        }
      } catch (err) {
        console.warn("FastAPI offline. Rendering pre-populated client dashboard data.", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleViewFeedback = (fileItem) => {
    setSampleCode({
      code: fileItem.code,
      language: fileItem.language,
      filename: fileItem.filename
    });
    setCurrentPage('analyze');
    window.scrollTo(0, 0);
  };

  const handleExport = () => {
    const dataStr = JSON.stringify({ metrics, uploads, weaknessReport, badges, errorsOverTime }, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'codesage-history.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Filter uploads based on search and language dropdown
  const filteredUploads = uploads.filter(file => {
    const matchesSearch = file.filename.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLang = langFilter === "All" || file.language === langFilter;
    return matchesSearch && matchesLang;
  });

  // Calculate coordinates for dynamic SVG Line Chart
  const chartWidth = 500;
  const chartHeight = 150;
  const paddingLeft = 40;
  const paddingRight = 20;
  const paddingTop = 20;
  const paddingBottom = 30;

  const chartUsableWidth = chartWidth - paddingLeft - paddingRight;
  const chartUsableHeight = chartHeight - paddingTop - paddingBottom;

  const maxVal = Math.max(...errorsOverTime.map(d => d.errors), 60);

  const points = errorsOverTime.map((d, index) => {
    const x = paddingLeft + (index / (errorsOverTime.length - 1)) * chartUsableWidth;
    const y = paddingTop + chartUsableHeight - (d.errors / maxVal) * chartUsableHeight;
    return { x, y, label: d.week, val: d.errors };
  });

  const pathD = points.reduce((path, p, i) => {
    return i === 0 ? `M ${p.x} ${p.y}` : `${path} L ${p.x} ${p.y}`;
  }, "");

  // Create area coordinates for fill under the line chart
  const areaD = points.length > 0 
    ? `${pathD} L ${points[points.length - 1].x} ${chartHeight - paddingBottom} L ${points[0].x} ${chartHeight - paddingBottom} Z`
    : "";

  return (
    <div className="dashboard-page animate-fade container">
      {/* 1. TOP HEADER WITH EXPORT OPTION */}
      <div className="dashboard-header-row">
        <h2>Your dashboard</h2>
        <button className="btn btn-secondary btn-export" onClick={handleExport}>
          <Download size={14} /> Export history
        </button>
      </div>

      {/* PROFILE / ACCOUNT SECTION */}
      <div className="profile-card card">
        <div className="profile-avatar-large">
          <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100" alt="Student" />
        </div>
        <div className="profile-info">
          <h3>Student Name</h3>
          <div className="profile-meta">
            <span><Mail size={14} /> student@example.com</span>
            <span><Calendar size={14} /> Member since March 2026</span>
            <span className="badge badge-brand">Free plan</span>
          </div>
        </div>
        <button className="btn btn-secondary" onClick={() => setCurrentPage('learn')}>
          Upgrade to Pro
        </button>
      </div>

      {/* 2. STATS ROW METRICS */}
      <div className="stats-row">
        {/* Total Uploads */}
        <div className="stat-card card">
          <span className="stat-label">Total uploads</span>
          <span className="stat-value">{metrics.totalUploads}</span>
        </div>
        
        {/* Errors Found */}
        <div className="stat-card card">
          <span className="stat-label">Errors found</span>
          <span className="stat-value">{metrics.errorsFound}</span>
        </div>

        {/* Errors this week */}
        <div className="stat-card card">
          <span className="stat-label">Errors this week</span>
          <div className="stat-trend-group">
            <span className="stat-value">{metrics.errorsThisWeek}</span>
            <span className="trend-badge trend-green">
              ↓ {metrics.errorsThisWeekChange}
            </span>
          </div>
        </div>

        {/* Top Language */}
        <div className="stat-card card">
          <span className="stat-label">Top language</span>
          <div className="top-lang-group">
            <span className="stat-value">{metrics.topLanguage}</span>
            <div className="lang-icon-badge">
              {metrics.topLanguage === 'Python' ? (
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M11.89 2C8.38 2 8.1 2.3 8.1 3.53v2.24H12c1.9 0 3.44 1.55 3.44 3.45v3.83h2.36c1.23 0 1.53-.28 1.53-1.8v-3.7C19.33 4 19.06 2 15.56 2h-3.67zM7.34 6.64C6.12 6.64 5.8 6.9 5.8 8.14v3.7c0 3.52.28 5.52 3.77 5.52h3.67v-2.24H9.3c-1.9 0-3.45-1.54-3.45-3.44V7.83h3.33V6.64H7.34z" fill="#5D59D6"/>
                </svg>
              ) : (
                <span className="js-logo font-mono">JS</span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* 3. MAIN GRID: RECENT UPLOADS vs SIDEBAR */}
      <div className="dashboard-grid">
        
        {/* LEFT COLUMN: RECENT UPLOADS & ERRORS CHART */}
        <div className="dashboard-left-panel">
          
          {/* Uploads List */}
          <div className="uploads-list-card card">
            <div className="card-header-actions">
              <h3>Recent uploads</h3>
              
              <div className="search-filter-row">
                <div className="search-input-wrapper">
                  <Search size={14} className="search-icon" />
                  <input
                    type="text"
                    placeholder="Search files..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>

                <select 
                  className="select-dropdown dropdown-sm"
                  value={langFilter}
                  onChange={(e) => setLangFilter(e.target.value)}
                >
                  <option value="All">All Languages</option>
                  {LANGUAGES.map(lang => (
                    <option key={lang.name} value={lang.name}>{lang.name}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Uploads List Items */}
            <div className="uploads-rows-container">
              {filteredUploads.length === 0 ? (
                <div className="empty-search-state">
                  <p>No uploaded files matched your filters.</p>
                </div>
              ) : (
                filteredUploads.map((file) => (
                  <div key={file.id} className="upload-item-row" onClick={() => handleViewFeedback(file)}>
                    <div className="item-left">
                      <div className="file-icon-box">🗎</div>
                      <div className="file-meta">
                        <span className="file-name">{file.filename}</span>
                        <div className="file-submeta">
                          <span className="badge badge-brand file-lang">{file.language}</span>
                          <span className="file-time">{file.timestamp}</span>
                        </div>
                      </div>
                    </div>

                    <div className="item-right">
                      <span className="badge file-error-badge">
                        {file.errors_count} {file.errors_count === 1 ? 'error' : 'errors'}
                      </span>
                      <button className="view-feedback-link">
                        View feedback <ChevronRight size={14} />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* SVG Line Graph: Errors over Time */}
          <div className="chart-card card">
            <h3>Errors over time</h3>
            
            <div className="svg-chart-container">
              <svg width="100%" height={chartHeight} viewBox={`0 0 ${chartWidth} ${chartHeight}`} className="svg-line-chart">
                <defs>
                  {/* Gradients */}
                  <linearGradient id="chart-fill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--brand)" stopOpacity="0.15" />
                    <stop offset="100%" stopColor="var(--brand)" stopOpacity="0.00" />
                  </linearGradient>
                </defs>
                
                {/* Horizontal Guide Lines */}
                {[0, 20, 40, 60].map((gridVal, i) => {
                  const y = paddingTop + chartUsableHeight - (gridVal / maxVal) * chartUsableHeight;
                  return (
                    <line 
                      key={i} 
                      x1={paddingLeft} 
                      y1={y} 
                      x2={chartWidth - paddingRight} 
                      y2={y} 
                      stroke="#EAEAEE" 
                      strokeWidth="1" 
                      strokeDasharray="4,4" 
                    />
                  );
                })}

                {/* Shaded Area Under Line */}
                <path d={areaD} fill="url(#chart-fill)" />

                {/* Line Path */}
                <path d={pathD} fill="none" stroke="var(--brand)" strokeWidth="3" strokeLinecap="round" />

                {/* Circles & Labels */}
                {points.map((p, idx) => (
                  <g key={idx}>
                    <circle cx={p.x} cy={p.y} r="4" fill="white" stroke="var(--brand)" strokeWidth="2.5" />
                    {/* X axis labels */}
                    <text 
                      x={p.x} 
                      y={chartHeight - 10} 
                      className="chart-axis-lbl" 
                      textAnchor="middle"
                    >
                      {p.label}
                    </text>
                  </g>
                ))}
              </svg>
            </div>
          </div>

        </div>

        {/* RIGHT COLUMN: SIDEBAR */}
        <div className="dashboard-right-panel">
          
          {/* Weakness Report */}
          <div className="weakness-card card">
            <div className="report-badge-meta">
              <span className="badge badge-brand">Weakness dashboard</span>
            </div>
            <h3>Your weakness report</h3>
            <p className="weakness-intro">Based on your last {metrics.totalUploads} uploads</p>
            
            <div className="weakness-list">
              {weaknessReport.map((w, idx) => (
                <div key={idx} className="weakness-item">
                  <div className="weakness-meta">
                    <span className="weakness-index">{idx + 1}. {w.topic}</span>
                    <span className="weakness-times">{w.count} times</span>
                  </div>
                  <a href="#analyze" className="practice-badge-link" onClick={() => setCurrentPage('analyze')}>
                    PRACTICE THIS
                  </a>
                </div>
              ))}
            </div>

            <button className="btn btn-primary w-full" onClick={() => setCurrentPage('learn')}>
              View recommended exercises
            </button>
          </div>

          {/* Badges Container */}
          <div className="badges-card card">
            <h3>Your badges</h3>
            
            <div className="badges-grid">
              {badges.map((badge) => {
                const getIcon = () => {
                  if (badge.icon === 'rocket') return <Rocket size={22} />;
                  if (badge.icon === 'award') return <Award size={22} />;
                  if (badge.icon === 'flame') return <Flame size={22} />;
                  return <Bug size={22} />;
                };

                return (
                  <div 
                    key={badge.id} 
                    className={`badge-circle-item ${badge.unlocked ? 'unlocked' : 'locked'}`}
                    title={badge.unlocked ? `Unlocked: ${badge.name}` : `Locked: ${badge.name}`}
                  >
                    <div className="badge-bubble">
                      {getIcon()}
                    </div>
                    <span className="badge-name">{badge.name}</span>
                  </div>
                );
              })}
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
