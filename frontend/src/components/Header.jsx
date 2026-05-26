import React from 'react';
import { Bell, Settings } from 'lucide-react';

export default function Header({ currentPage, setCurrentPage, isLoggedIn, setIsLoggedIn, user }) {
  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'analyze', label: 'Analyze' },
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'learn', label: 'Learn' },
    { id: 'pricing', label: 'Pricing' }
  ];

  const handleNavClick = (e, targetId) => {
    e.preventDefault();
    if (targetId === 'pricing') {
      // Scroll to pricing section on home page
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

  return (
    <header className="site-header">
      <div className="container header-container">
        {/* CodeSage Logo */}
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

        {/* Navigation Tabs */}
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

        {/* Right Action Icons / Profiles */}
        <div className="header-actions">
          {isLoggedIn ? (
            <>
              <span className="free-plan-badge">Free plan</span>
              <button className="icon-btn" title="Notifications">
                <Bell size={20} className="header-icon" />
                <span className="notification-dot" />
              </button>
              <button className="icon-btn" title="Settings">
                <Settings size={20} className="header-icon" />
              </button>
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
