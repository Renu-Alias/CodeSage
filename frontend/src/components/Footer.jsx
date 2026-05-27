import React from 'react';

export default function Footer({ setCurrentPage }) {
  return (
    <footer className="site-footer">
      <div className="container footer-container">
        <div className="footer-brand">
          <div className="logo-area" onClick={() => { setCurrentPage('home'); window.scrollTo(0, 0); }}>
            <div className="logo-icon">
              <svg width="20" height="20" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 2L36 11V29L20 38L4 29V11L20 2Z" stroke="#5D59D6" strokeWidth="3" strokeLinejoin="round"/>
                <path d="M15 16L11 20L15 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M25 16L29 20L25 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <span className="logo-text">Code<span className="logo-highlight">Sage</span></span>
          </div>
          <p className="copyright-text">© 2026 CodeSage AI. Empowering the next generation of engineers.</p>
        </div>
        
        <div className="footer-links">
          <a href="#terms" onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}>Terms of Service</a>
          <a href="#privacy" onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}>Privacy Policy</a>
          <a href="#cookie" onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}>Cookie Policy</a>
          <a href="#docs" onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}>Documentation</a>
          <a href="#support" onClick={(e) => { e.preventDefault(); setCurrentPage('home'); }}>Support</a>
        </div>
      </div>
    </footer>
  );
}
