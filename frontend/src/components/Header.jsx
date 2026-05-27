import { useState, useRef, useEffect } from 'react';
import { Bell, Settings, Gift, Megaphone, MessageSquare, Star, User, Palette, HelpCircle, LogOut } from 'lucide-react';

export default function Header({ currentPage, setCurrentPage, isLoggedIn, setIsLoggedIn, user }) {
  const [notifOpen, setNotifOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const notifRef = useRef(null);
  const settingsRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (notifRef.current && !notifRef.current.contains(e.target)) setNotifOpen(false);
      if (settingsRef.current && !settingsRef.current.contains(e.target)) setSettingsOpen(false);
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'analyze', label: 'Analyze' },
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'learn', label: 'Learn' },
    { id: 'pricing', label: 'Pricing' }
  ];

  const handleNavClick = (e, targetId) => {
    e.preventDefault();
    setNotifOpen(false);
    setSettingsOpen(false);
    if (targetId === 'pricing') {
      setCurrentPage('home');
      setTimeout(() => {
        const el = document.getElementById('pricing-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      setCurrentPage(targetId);
      window.scrollTo(0, 0);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentPage('home');
    window.scrollTo(0, 0);
  };

  const notifications = [
    { icon: <Gift size={16} />, title: "🎉 Special Offer!", desc: "Get 50% off on Pro plan — limited time only.", time: "2 hours ago" },
    { icon: <Megaphone size={16} />, title: "📢 New Feature", desc: "AI-powered code explanations are now live!", time: "1 day ago" },
    { icon: <Star size={16} />, title: "⭐ Milestone", desc: "You've analyzed 10 code snippets. Keep going!", time: "3 days ago" },
    { icon: <MessageSquare size={16} />, title: "💡 Tip", desc: "Try the Dashboard to track your progress.", time: "5 days ago" },
  ];

  const handleAppearance = () => {
    document.body.classList.toggle('dark-mode');
    setSettingsOpen(false);
  };

  const handleHelp = () => {
    setCurrentPage('home');
    setSettingsOpen(false);
    setTimeout(() => {
      const el = document.querySelector('.site-footer');
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  const settingsItems = [
    { icon: <User size={16} />, label: "Account Settings", onClick: () => setCurrentPage('dashboard') },
    { icon: <Palette size={16} />, label: "Appearance", onClick: handleAppearance },
    { icon: <HelpCircle size={16} />, label: "Help & Support", onClick: handleHelp },
    { icon: <LogOut size={16} />, label: "Log Out", onClick: handleLogout },
  ];

  return (
    <header className="site-header">
      <div className="container header-container">
        <a href="/" className="logo-area" onClick={(e) => handleNavClick(e, 'home')}>
          <div className="logo-icon">
            <svg width="32" height="32" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 2L36 11V29L20 38L4 29V11L20 2Z" stroke="#5D59D6" strokeWidth="3" strokeLinejoin="round"/>
              <path d="M15 16L11 20L15 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M25 16L29 20L25 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <span className="logo-text">
            Code<span className="logo-highlight">Sage</span>
          </span>
        </a>

        <nav className="header-nav">
          {navItems.map((item) => (
            <a
              key={item.id}
              href={`#${item.id}`}
              onClick={(e) => handleNavClick(e, item.id)}
              className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
            >
              {item.label}
              {currentPage === item.id && <span className="nav-underline" />}
            </a>
          ))}
        </nav>

        <div className="header-actions">
          {isLoggedIn ? (
            <>
              <span className="free-plan-badge">Free plan</span>

              <div className="dropdown-wrapper" ref={notifRef}>
                <button className="icon-btn" title="Notifications" onClick={() => { setNotifOpen(!notifOpen); setSettingsOpen(false); }}>
                  <Bell size={20} className="header-icon" />
                  <span className="notification-dot" />
                </button>
                {notifOpen && (
                  <div className="dropdown-menu dropdown-notif">
                    <div className="dropdown-header">Notifications</div>
                    <div className="dropdown-body">
                      {notifications.map((n, i) => (
                        <div className="dropdown-item" key={i}>
                          <div className="dropdown-item-icon">{n.icon}</div>
                          <div className="dropdown-item-content">
                            <div className="dropdown-item-title">{n.title}</div>
                            <div className="dropdown-item-desc">{n.desc}</div>
                            <div className="dropdown-item-time">{n.time}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="dropdown-footer" onClick={() => setNotifOpen(false)}>Mark all as read</div>
                  </div>
                )}
              </div>

              <div className="dropdown-wrapper" ref={settingsRef}>
                <button className="icon-btn" title="Settings" onClick={() => { setSettingsOpen(!settingsOpen); setNotifOpen(false); }}>
                  <Settings size={20} className="header-icon" />
                </button>
                {settingsOpen && (
                  <div className="dropdown-menu dropdown-settings">
                    <div className="dropdown-header">Settings</div>
                    <div className="dropdown-body">
                      {settingsItems.map((s, i) => (
                        <div className="dropdown-item dropdown-item-single" key={i} onClick={() => { s.onClick(); setSettingsOpen(false); }}>
                          <div className="dropdown-item-icon">{s.icon}</div>
                          <div className="dropdown-item-content">
                            <div className="dropdown-item-title">{s.label}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div 
                className="profile-avatar" 
                onClick={() => setCurrentPage('dashboard')} 
                style={{ cursor: 'pointer' }}
                title={user?.name || "Student Profile"}
              >
                <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100" alt="Student Profile" />
              </div>
              <button 
                className="btn btn-secondary btn-sign-in" 
                onClick={handleLogout}
                style={{ padding: '6px 12px', fontSize: '12px' }}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <button className="btn btn-secondary btn-sign-in" onClick={() => setCurrentPage('login')}>
                Sign In
              </button>
              <button className="btn btn-primary btn-sign-in" onClick={() => setCurrentPage('signup')}>
                Sign Up
              </button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
