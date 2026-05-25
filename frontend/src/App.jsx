import React, { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Analyze from './pages/Analyze';
import Dashboard from './pages/Dashboard';
import Learn from './pages/Learn';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [sampleCode, setSampleCode] = useState(null);

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
      default:
        return <Home setCurrentPage={setCurrentPage} setSampleCode={setSampleCode} />;
    }
  };

  return (
    <div className="app-container">
      <Header currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main className="main-content">
        {renderPage()}
      </main>
      <Footer setCurrentPage={setCurrentPage} />
    </div>
  );
}

export default App;
