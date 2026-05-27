import React, { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Analyze from './pages/Analyze';
import Dashboard from './pages/Dashboard';
import Learn from './pages/Learn';
import Payment from './pages/Payment';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import AccountSettings from './pages/AccountSettings';
import OnboardingLearning from './pages/OnboardingLearning';
import OnboardingLevel from './pages/OnboardingLevel';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [sampleCode, setSampleCode] = useState(null);
  const [selectedPlan, setSelectedPlan] = useState(null);
  
  // Authentication & Onboarding states
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [onboardingData, setOnboardingData] = useState({
    learningLanguage: 'Python',
    skillLevel: 'Beginner'
  });

  // Protected routes: redirect to login if not authenticated
  const protectedRoutes = ['analyze', 'dashboard', 'learn', 'payment', 'account-settings'];
  const activePage = protectedRoutes.includes(currentPage) && !isLoggedIn ? 'login' : currentPage;

  const renderPage = () => {
    switch (activePage) {
      case 'home':
        return <Home
          setCurrentPage={setCurrentPage}
          setSampleCode={setSampleCode}
          setSelectedPlan={setSelectedPlan}
          isLoggedIn={isLoggedIn}
        />;
      case 'analyze':
        return <Analyze sampleCode={sampleCode} setSampleCode={setSampleCode} />;
      case 'dashboard':
        return <Dashboard setCurrentPage={setCurrentPage} setSampleCode={setSampleCode} />;
      case 'learn':
        return <Learn setCurrentPage={setCurrentPage} />;
      case 'payment':
        return <Payment selectedPlan={selectedPlan} setCurrentPage={setCurrentPage} />;
      case 'login':
        return <Login setCurrentPage={setCurrentPage} setIsLoggedIn={setIsLoggedIn} />;
      case 'signup':
        return <SignUp setCurrentPage={setCurrentPage} setIsLoggedIn={setIsLoggedIn} />;
      case 'onboarding-learning':
        return <OnboardingLearning setCurrentPage={setCurrentPage} setOnboardingData={setOnboardingData} />;
      case 'onboarding-level':
        return <OnboardingLevel setCurrentPage={setCurrentPage} setIsLoggedIn={setIsLoggedIn} onboardingData={onboardingData} setOnboardingData={setOnboardingData} />;
      case 'account-settings':
        return <AccountSettings setCurrentPage={setCurrentPage} />;
      default:
        return <Home setCurrentPage={setCurrentPage} setSampleCode={setSampleCode} setSelectedPlan={setSelectedPlan} isLoggedIn={isLoggedIn} />;
    }
  };

  // Do not render default Header/Footer on full-screen auth and onboarding pages
  const isFullScreenPage = ['login', 'signup', 'onboarding-learning', 'onboarding-level'].includes(activePage);

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
        currentPage={activePage}
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

