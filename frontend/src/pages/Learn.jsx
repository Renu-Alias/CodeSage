import React from 'react';
import { BookOpen, Compass, Award, Star } from 'lucide-react';

export default function Learn({ setCurrentPage }) {
  return (
    <div className="learn-page animate-fade container">
      {/* 1. HERO BLOCK */}
      <section className="learn-hero text-center">
        <h1 className="hero-title gradient-text">Master coding with AI by your side</h1>
        <p className="hero-subtitle">
          Accelerate your programming journey with intelligent code analysis, personalized tutoring, and real-time step-by-step logic explanations designed for the modern developer.
        </p>
        
        <div className="hero-actions">
          <button className="btn btn-primary" onClick={() => setCurrentPage('analyze')}>
            Start learning
          </button>
          <button className="btn btn-secondary" onClick={() => setCurrentPage('home')}>
            Watch demo
          </button>
        </div>
      </section>

      {/* 2. APP SCREENSHOT WRAPPER */}
      <section className="learn-app-preview">
        <div className="monitor-frame card">
          <div className="monitor-screen">
            {/* Visual presentation of code workspace */}
            <div className="workspace-header">
              <span className="dot dot-red" />
              <span className="dot dot-yellow" />
              <span className="dot dot-green" />
              <div className="workspace-title">CodeSage Workspace - Recursion Solver</div>
            </div>
            
            <div className="workspace-body font-mono">
              <div className="workspace-sidebar">
                <div className="sidebar-item active">fibonacci.py</div>
                <div className="sidebar-item">binary_search.cpp</div>
                <div className="sidebar-item">quicksort.js</div>
              </div>
              <div className="workspace-editor">
                <div className="code-line"><span className="keyword">def</span> <span className="func">fibonacci</span>(n):</div>
                <div className="code-line">    <span className="comment"># Tutoring Insight: Base cases check</span></div>
                <div className="code-line">    <span className="keyword">if</span> n &lt;= <span className="num">1</span>:</div>
                <div className="code-line">        <span className="keyword">return</span> n</div>
                <div className="code-line">    <span className="keyword">return</span> fibonacci(n-<span className="num">1</span>) + fibonacci(n-<span className="num">2</span>)</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. CORE TUTORING FEATURES ROW */}
      <section className="tutoring-features-grid">
        {/* Card 1: Instant Analysis */}
        <div className="tutoring-card card">
          <div className="icon-wrapper">
            <BookOpen size={20} color="var(--brand)" />
          </div>
          <h3>Instant analysis</h3>
          <p>Receive immediate feedback on your code syntax, logic, and efficiency with our AI engine.</p>
          
          <div className="embedded-preview-box code-embed font-mono">
            <div className="code-line"><span className="keyword">function</span> <span className="func">analyze</span>(code) &#123;</div>
            <div className="code-line">  <span className="keyword">const</span> result = AI.process(code);</div>
            <div className="code-line">  <span className="keyword">return</span> result.feedback;</div>
            <div className="code-line">&#125;</div>
          </div>
        </div>

        {/* Card 2: Guided Tutoring */}
        <div className="tutoring-card card">
          <div className="icon-wrapper">
            <Compass size={20} color="var(--brand)" />
          </div>
          <h3>Guided tutoring</h3>
          <p>Break down complex problems into step-by-step logic explanations that help you truly understand the "why".</p>
          
          <div className="embedded-preview-box list-embed">
            <div className="list-item-preview">
              <span className="badge badge-brand list-index">1.</span>
              <span>Identify the base case in recursion.</span>
            </div>
            <div className="list-item-preview">
              <span className="badge badge-brand list-index">2.</span>
              <span>Map the recursive step to subproblems.</span>
            </div>
          </div>
        </div>

        {/* Card 3: Progress Tracking */}
        <div className="tutoring-card card">
          <div className="icon-wrapper">
            <Award size={20} color="var(--brand)" />
          </div>
          <h3>Progress tracking</h3>
          <p>Visualize your growth with detailed skill maps and completion stats as you master new concepts.</p>
          
          <div className="embedded-preview-box progress-embed">
            <div className="progress-label-row">
              <span className="p-concept">Mastery Score</span>
              <span className="p-percent">75%</span>
            </div>
            <div className="progress-bar-bg">
              <div className="progress-bar-fill" style={{ width: '75%' }} />
            </div>
          </div>
        </div>
      </section>

      {/* 4. STUDENT QUOTE block */}
      <section className="quote-section text-center">
        <div className="quote-box card">
          <span className="large-quote-mark">“</span>
          <p className="quote-text">
            CodeSage didn't just give me the answers—it taught me how to think like a developer. The step-by-step logic explanations turned complex data structures into something I could finally grasp.
          </p>
          
          <div className="quote-author-profile">
            <div className="author-avatar">
              <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=100" alt="Alex Rivera Avatar" />
            </div>
            <h4 className="author-name">Alex Rivera</h4>
            <p className="author-role">Computer Science Sophomore</p>
          </div>
        </div>
      </section>

      {/* 5. FOOTER CALL-TO-ACTION TIER */}
      <section className="learn-cta text-center animate-fade">
        <div className="cta-banner-card card">
          <h2>Ready to accelerate your learning?</h2>
          <p>Join thousands of students using AI to master programming 3x faster. No credit card required to start.</p>
          <button className="btn btn-primary" onClick={() => setCurrentPage('analyze')}>
            Get started for free
          </button>
        </div>
      </section>
    </div>
  );
}
