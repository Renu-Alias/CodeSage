import React, { useState, useMemo } from 'react';
import { BookOpen, Compass, Award, Star, X, Play, CheckCircle, XCircle, ArrowRight, RefreshCw, Lightbulb } from 'lucide-react';
import { EXERCISES, LANGUAGE_WEAKNESS_MAP } from '../constants/exercises';
import { LANGUAGES } from '../constants/languages';

export default function Learn({ setCurrentPage }) {
  const [showDemo, setShowDemo] = useState(false);
  const [selectedLang, setSelectedLang] = useState('Python');
  const [currentQ, setCurrentQ] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(0);
  const [showResult, setShowResult] = useState(false);

  const exercises = EXERCISES[selectedLang] || EXERCISES.Python;

  const handleAnswer = (idx) => {
    if (selectedAnswer !== null) return;
    setSelectedAnswer(idx);
    setAnswered(answered + 1);
    if (idx === exercises[currentQ].correct) {
      setScore(score + 1);
    }
  };

  const handleNext = () => {
    if (currentQ + 1 < exercises.length) {
      setCurrentQ(currentQ + 1);
      setSelectedAnswer(null);
    } else {
      setShowResult(true);
    }
  };

  const handleRestart = () => {
    setCurrentQ(0);
    setSelectedAnswer(null);
    setScore(0);
    setAnswered(0);
    setShowResult(false);
  };

  const weaknesses = LANGUAGE_WEAKNESS_MAP[selectedLang] || [];
  const allLangs = Object.keys(EXERCISES);
  const weakAreas = [
    { topic: "Syntax correctness", count: Math.floor(Math.random() * 15 + 10) },
    { topic: weaknesses[0] || "Logic errors", count: Math.floor(Math.random() * 12 + 8) },
    { topic: weaknesses[1] || "Edge cases", count: Math.floor(Math.random() * 10 + 5) }
  ];

  const demoSteps = [
    { code: 'def calculate_average(numbers):', highlight: false },
    { code: '    total = sum(numbers)', highlight: false },
    { code: '    return total / len(numbers)', highlight: true, msg: 'Bugs found: division by zero if numbers is empty' },
  ];

  return (
    <div className="learn-page animate-fade container">
      {/* DEMO OVERLAY */}
      {showDemo && (
        <div className="demo-overlay" onClick={() => setShowDemo(false)}>
          <div className="demo-modal" onClick={e => e.stopPropagation()}>
            <button className="demo-close" onClick={() => setShowDemo(false)}><X size={20} /></button>
            <h2>CodeSage in Action</h2>
            <div className="demo-steps">
              <div className="demo-step">
                <div className="demo-step-num">1</div>
                <div><strong>Submit your code</strong><p>Paste any code snippet from any language.</p></div>
              </div>
              <div className="demo-step">
                <div className="demo-step-num">2</div>
                <div><strong>AI analyzes instantly</strong><p>Syntax errors, logical bugs, and runtime risks are detected in milliseconds.</p></div>
              </div>
              <div className="demo-step">
                <div className="demo-step-num">3</div>
                <div><strong>Get plain-English explanations</strong><p>Beginner-friendly breakdowns with analogies, auto-fixes, and line-by-line walkthroughs.</p></div>
              </div>
            </div>
            <div className="demo-code-preview">
              {demoSteps.map((s, i) => (
                <div key={i} className={`demo-code-line ${s.highlight ? 'demo-highlight' : ''}`}>
                  <code>{s.code}</code>
                  {s.highlight && <span className="demo-msg">{s.msg}</span>}
                </div>
              ))}
            </div>
            <button className="btn btn-primary" onClick={() => { setShowDemo(false); setCurrentPage('analyze'); }}>
              Try it now <ArrowRight size={16} />
            </button>
          </div>
        </div>
      )}

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
          <button className="btn btn-secondary" onClick={() => setShowDemo(true)}>
            <Play size={16} /> Watch demo
          </button>
        </div>
      </section>

      {/* 2. APP SCREENSHOT WRAPPER */}
      <section className="learn-app-preview">
        <div className="monitor-frame card">
          <div className="monitor-screen">
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

      {/* 4. EXERCISE SECTION */}
      <section className="exercise-section" id="exercises">
        <div className="exercise-header">
          <h2><Lightbulb size={22} /> Practice exercises</h2>
          <p>Test your knowledge with language-specific quizzes. Choose a language below.</p>
        </div>

        <div className="exercise-controls">
          <select
            className="select-dropdown exercise-lang-select"
            value={selectedLang}
            onChange={(e) => { setSelectedLang(e.target.value); handleRestart(); }}
          >
            {allLangs.map(lang => (
              <option key={lang} value={lang}>{lang}</option>
            ))}
          </select>
          <div className="exercise-weakness-hints">
            {weakAreas.map((w, i) => (
              <span key={i} className="badge badge-weakness">{w.topic}: {w.count} issues</span>
            ))}
          </div>
        </div>

        <div className="exercise-card card">
          {showResult ? (
            <div className="exercise-result">
              <div className="result-icon">{score === exercises.length ? <CheckCircle size={48} /> : <Star size={48} />}</div>
              <h3>{score === exercises.length ? 'Perfect score!' : 'Practice makes perfect!'}</h3>
              <p>You got <strong>{score}</strong> out of <strong>{exercises.length}</strong> correct in {selectedLang}.</p>
              <button className="btn btn-primary" onClick={handleRestart}>
                <RefreshCw size={16} /> Try again
              </button>
            </div>
          ) : (
            <>
              <div className="exercise-progress">
                <span>Question {currentQ + 1} of {exercises.length}</span>
                <span className="exercise-score">Score: {score}/{answered}</span>
              </div>
              <div className="exercise-question">
                <p>{exercises[currentQ].question}</p>
              </div>
              <div className="exercise-options">
                {exercises[currentQ].options.map((opt, idx) => {
                  let cls = 'exercise-option';
                  if (selectedAnswer !== null) {
                    if (idx === exercises[currentQ].correct) cls += ' correct';
                    else if (idx === selectedAnswer) cls += ' wrong';
                  }
                  return (
                    <div key={idx} className={cls} onClick={() => handleAnswer(idx)}>
                      <span className="option-letter">{String.fromCharCode(65 + idx)}</span>
                      <span className="option-text">{opt}</span>
                      {selectedAnswer !== null && idx === exercises[currentQ].correct && <CheckCircle size={18} className="option-icon correct-icon" />}
                      {selectedAnswer !== null && idx === selectedAnswer && idx !== exercises[currentQ].correct && <XCircle size={18} className="option-icon wrong-icon" />}
                    </div>
                  );
                })}
              </div>
              {selectedAnswer !== null && (
                <div className="exercise-explanation">
                  <Lightbulb size={16} />
                  <span>{exercises[currentQ].explanation}</span>
                </div>
              )}
              {selectedAnswer !== null && (
                <button className="btn btn-primary exercise-next" onClick={handleNext}>
                  {currentQ + 1 < exercises.length ? 'Next question' : 'See results'} <ArrowRight size={16} />
                </button>
              )}
            </>
          )}
        </div>
      </section>

      {/* 5. STUDENT QUOTE */}
      <section className="quote-section text-center">
        <div className="quote-box card">
          <span className="large-quote-mark">&ldquo;</span>
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

      {/* 6. CTA */}
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
