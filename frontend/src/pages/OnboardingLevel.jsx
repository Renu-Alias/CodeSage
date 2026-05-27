import React, { useState } from 'react';
import { ArrowRight, Sprout, Terminal, CheckCircle2 } from 'lucide-react';

export default function OnboardingLevel({ setCurrentPage, setIsLoggedIn, setOnboardingData, onboardingData }) {
  const [selectedLevel, setSelectedLevel] = useState(onboardingData?.skillLevel || 'Beginner');

  const handleFinish = () => {
    setOnboardingData(prev => ({ ...prev, skillLevel: selectedLevel }));
    setIsLoggedIn(true);
    setCurrentPage('dashboard');
    window.scrollTo(0, 0);
  };

  const handleSaveExit = () => {
    setOnboardingData(prev => ({ ...prev, skillLevel: selectedLevel }));
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
        {/* Progress indicators (two dots - Step 2 active) */}
        <div className="onboarding-dots-container">
          <span className="onboarding-dot" />
          <span className="onboarding-dot active" />
        </div>

        <div className="onboarding-title-area">
          <h2>How would you describe your level?</h2>
          <p>This sets how CodeSage explains errors to you. You can change this anytime.</p>
        </div>

        {/* Level Cards Grid */}
        <div className="level-grid">
          {/* Beginner Card */}
          <div
            className={`level-card ${selectedLevel === 'Beginner' ? 'active' : ''}`}
            onClick={() => setSelectedLevel('Beginner')}
          >
            <div className="level-card-icon">
              <Sprout size={24} />
            </div>
            {selectedLevel === 'Beginner' && (
              <CheckCircle2 className="level-card-check" size={20} />
            )}
            <h3 className="level-card-title">Beginner</h3>
            <p className="level-card-desc">
              I'm just starting out. Explain things simply with analogies.
            </p>
          </div>

          {/* Intermediate Card */}
          <div
            className={`level-card ${selectedLevel === 'Intermediate' ? 'active' : ''}`}
            onClick={() => setSelectedLevel('Intermediate')}
          >
            <div className="level-card-icon">
              <Terminal size={24} />
            </div>
            {selectedLevel === 'Intermediate' && (
              <CheckCircle2 className="level-card-check" size={20} />
            )}
            <h3 className="level-card-title">Intermediate</h3>
            <p className="level-card-desc">
              I know the basics. Give me technical details.
            </p>
          </div>
        </div>

        {/* Bottom Actions Area */}
        <div className="onboarding-actions" style={{ flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
          <button className="btn btn-primary onboarding-btn-next" onClick={handleFinish} style={{ width: 'auto', minWidth: '240px' }}>
            Get started <ArrowRight size={18} />
          </button>
          <span className="step-indicator-text">Step 2 of 2</span>
        </div>
      </main>

      {/* Onboarding Footer */}
      <footer className="onboarding-footer" style={{ marginTop: 'auto' }}>
        <div className="container onboarding-footer-container">
          <div className="onboarding-footer-left">
            CodeSage Academy
          </div>
          <div className="onboarding-footer-right">
            <a href="#terms" onClick={(e) => e.preventDefault()}>Terms</a>
            <a href="#privacy" onClick={(e) => e.preventDefault()}>Privacy</a>
            <a href="#support" onClick={(e) => e.preventDefault()}>Support</a>
            <span>© 2026 CodeSage Academy. All rights reserved.</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
