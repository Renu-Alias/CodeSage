import React, { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Analyze from './pages/Analyze';
import Dashboard from './pages/Dashboard';
import Learn from './pages/Learn';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import OnboardingLearning from './pages/OnboardingLearning';
import OnboardingLevel from './pages/OnboardingLevel';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [sampleCode, setSampleCode] = useState(null);
  
  // Authentication & Onboarding states
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [onboardingData, setOnboardingData] = useState({
    learningLanguage: 'Python',
    skillLevel: 'Beginner'
  });

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <Home setCurrentPage={setCurrentPage} setSampleCode={setSampleCode} />;
      case 'analyze':
        return <Analyze sampleCode={sampleCode} setSampleCode={setSampleCode} />;
      case 'dashboard':
        return <Dashboard setCurrentPage={setCurrentPage} setSampleCode={setSampleCode} />;
      case 'learn':
        return <Learn setCurrentPage={setCurrentPage} />;
      case 'login':
        return (
          <Login 
            setCurrentPage={setCurrentPage} 
            setIsLoggedIn={setIsLoggedIn} 
            setUser={setUser} 
          />
        );
      case 'signup':
        return (
          <SignUp 
            setCurrentPage={setCurrentPage} 
            setUser={setUser} 
          />
        );
      case 'onboarding-learning':
        return (
          <OnboardingLearning 
            setCurrentPage={setCurrentPage} 
            setOnboardingData={setOnboardingData} 
            onboardingData={onboardingData} 
          />
        );
      case 'onboarding-level':
        return (
          <OnboardingLevel 
            setCurrentPage={setCurrentPage} 
            setIsLoggedIn={setIsLoggedIn} 
            setOnboardingData={setOnboardingData} 
            onboardingData={onboardingData} 
          />
        );
      default:
        return <Home setCurrentPage={setCurrentPage} setSampleCode={setSampleCode} />;
    }
  };

  // Do not render default Header/Footer on full-screen auth and onboarding pages
  const isFullScreenPage = ['login', 'signup', 'onboarding-learning', 'onboarding-level'].includes(currentPage);

  if (isFullScreenPage) {
    return (
      <div className="full-screen-container">
        {renderPage()}
      </div>
    );
  }

  return (
    <div className="app-container">
      <Header 
        currentPage={currentPage} 
        setCurrentPage={setCurrentPage} 
        isLoggedIn={isLoggedIn}
        setIsLoggedIn={setIsLoggedIn}
        user={user}
      />
      <main className="main-content">
        {renderPage()}
      </main>
      <Footer setCurrentPage={setCurrentPage} />
    </div>
  );
}

export default App;

