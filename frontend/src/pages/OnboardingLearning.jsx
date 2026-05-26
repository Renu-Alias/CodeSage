import React, { useState } from 'react';
import { ArrowRight, Coffee, Terminal, Code2, Rocket, Wrench, MoreHorizontal } from 'lucide-react';

export default function OnboardingLearning({ setCurrentPage, setOnboardingData, onboardingData }) {
  const [selectedLang, setSelectedLang] = useState(onboardingData?.learningLanguage || 'Python');

  const languages = [
    { id: 'Python', name: 'Python', icon: <Terminal size={22} /> },
    { id: 'JavaScript', name: 'JavaScript', icon: <span style={{ fontWeight: 800, fontSize: '13px' }}>JS</span> },
    { id: 'Java', name: 'Java', icon: <Coffee size={22} /> },
    { id: 'C++', name: 'C++', icon: <Code2 size={22} /> },
    { id: 'TypeScript', name: 'TypeScript', icon: <span style={{ fontWeight: 800, fontSize: '13px' }}>JS</span> },
    { id: 'Go', name: 'Go', icon: <Rocket size={22} /> },
    { id: 'Rust', name: 'Rust', icon: <Wrench size={22} /> },
    { id: 'Other', name: 'Other', icon: <MoreHorizontal size={22} /> },
  ];

  const handleNext = () => {
    setOnboardingData(prev => ({ ...prev, learningLanguage: selectedLang }));
    setCurrentPage('onboarding-level');
    window.scrollTo(0, 0);
  };

  const handleSaveExit = () => {
    setOnboardingData(prev => ({ ...prev, learningLanguage: selectedLang }));
    setCurrentPage('home');
    window.scrollTo(0, 0);
  };

  return (
    <div className="onboarding-screen">
      {/* Premium Onboarding Header */}
      <header className="onboarding-header">
        <div className="container onboarding-header-container">
          <div className="logo-area" onClick={handleSaveExit}>
            <div className="logo-icon">
              <svg width="32" height="32" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 2L36 11V29L20 38L4 29V11L20 2Z" stroke="#5D59D6" strokeWidth="3" strokeLinejoin="round"/>
                <path d="M15 16L11 20L15 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M25 16L29 20L25 24" stroke="#5D59D6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <span className="logo-text">Code<span className="logo-highlight">Sage</span></span>
          </div>

          <div className="onboarding-header-right">
            <a href="#support" className="onboarding-header-link" onClick={(e) => e.preventDefault()}>Support</a>
            <button className="save-exit-btn" onClick={handleSaveExit}>Save & Exit</button>
          </div>
        </div>
      </header>

      {/* Main Form Area */}
      <main className="onboarding-body container">
        {/* Progress indicators (two dots) */}
        <div className="onboarding-dots-container">
          <span className="onboarding-dot active" />
          <span className="onboarding-dot" />
        </div>

        <div className="onboarding-title-area">
          <h2>What are you learning?</h2>
          <p>We'll personalise your experience.</p>
        </div>

        {/* Options grid */}
        <div className="learning-grid">
          {languages.map((lang) => (
            <div
              key={lang.id}
              className={`learning-card ${selectedLang === lang.id ? 'active' : ''}`}
              onClick={() => setSelectedLang(lang.id)}
            >
              <div className="learning-card-icon">
                {lang.icon}
              </div>
              <span className="learning-card-name">{lang.name}</span>
            </div>
          ))}
        </div>

        {/* Bottom Actions Row */}
        <div className="onboarding-actions">
          <button className="btn btn-primary onboarding-btn-next" onClick={handleNext}>
            Next <ArrowRight size={18} />
          </button>
        </div>
      </main>

      {/* Real Onboarding Footer */}
      <footer className="onboarding-footer">
        <div className="container onboarding-footer-container">
          <div className="onboarding-footer-left">
            CodeSage Academy
          </div>
          <div className="onboarding-footer-right">
            <a href="#terms" onClick={(e) => e.preventDefault()}>Terms</a>
            <a href="#privacy" onClick={(e) => e.preventDefault()}>Privacy</a>
            <a href="#support" onClick={(e) => e.preventDefault()}>Support</a>
            <span>© 2024 CodeSage Academy. All rights reserved.</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
