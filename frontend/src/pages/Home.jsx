import React from 'react';
import { ArrowRight, Code2, AlertTriangle, Lightbulb, Compass, Award, Star } from 'lucide-react';
import { LANGUAGES } from '../constants/languages';

export default function Home({ setCurrentPage, setSampleCode, setSelectedPlan }) {
  const handleStartAnalysis = (codeType) => {
    if (codeType === 'demo') {
      setSampleCode({
        code: "def calculate_average(numbers):\n    total = sum(numbers)\n    # Bug: division without zero check\n    return total / len(numbers)",
        language: "Python",
        filename: "calculate_average.py"
      });
    } else if (codeType === 'loop') {
      setSampleCode({
        code: "def calculate_total(prices):\n    total = 0\n    for i in range(len(prices)):\n        tax = i * price # Error here\n        total += p\n    return total",
        language: "Python",
        filename: "calculate_total.py"
      });
    }
    setCurrentPage('analyze');
    window.scrollTo(0, 0);
  };

  return (
    <div className="home-page animate-fade">
      {/* 1. HERO SECTION */}
      <section className="hero-section text-center">
        <div className="container">
          <div className="hero-badge-wrapper">
            <span className="badge badge-brand hero-badge">AI-powered code tutor for students</span>
          </div>
          <h1 className="hero-title gradient-text">
            Debug smarter. Learn faster.<br />Code better.
          </h1>
          <p className="hero-subtitle">
            Upload any code snippet and CodeSage finds your bugs, explains them in plain English, and remembers your weak spots so you actually improve.
          </p>
          
          <div className="hero-actions">
            <button className="btn btn-primary" onClick={() => handleStartAnalysis('default')}>
              <Code2 size={18} /> Analyze my code
            </button>
            <button className="btn btn-secondary" onClick={() => handleStartAnalysis('demo')}>
              See a demo
            </button>
          </div>

          <div className="hero-languages">
            {LANGUAGES.slice(0, 7).map(lang => (
              <span key={lang.name} className="lang-tag">{lang.name.toUpperCase()}</span>
            ))}
            <span className="lang-tag">+ MORE</span>
          </div>
        </div>
      </section>

      {/* 2. HOW IT WORKS */}
      <section className="how-it-works-section">
        <div className="container">
          <div className="section-header text-center">
            <span className="section-subtitle">HOW IT WORKS</span>
            <h2 className="section-title">Three steps to better code</h2>
          </div>

          <div className="steps-grid">
            {/* Step 1 */}
            <div className="step-card card text-center">
              <div className="step-number">1</div>
              <h3 className="step-card-title">Paste or upload your code</h3>
              <p className="step-card-desc">
                Choose your programming language or let our AI auto-detect it for you instantly.
              </p>
            </div>
            {/* Step 2 */}
            <div className="step-card card text-center">
              <div className="step-number">2</div>
              <h3 className="step-card-title">Get Instant AI feedback</h3>
              <p className="step-card-desc">
                Identify bugs, performance bottlenecks, and get plain-English explanations for every fix.
              </p>
            </div>
            {/* Step 3 */}
            <div className="step-card card text-center">
              <div className="step-number">3</div>
              <h3 className="step-card-title">Track your progress</h3>
              <p className="step-card-desc">
                View your history and get weakness reports to see where you're improving over time.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. MORE THAN A DEBUGGER */}
      <section className="features-section">
        <div className="container">
          <div className="section-header text-center">
            <h2 className="section-title">More than a debugger</h2>
          </div>

          <div className="features-grid">
            <div className="feature-card card">
              <div className="feature-icon-wrapper err">
                <AlertTriangle size={20} className="feature-icon" />
              </div>
              <div className="feature-content">
                <h3>Error detection</h3>
                <p>Comprehensive line-by-line bug detection that catches logic errors standard linters miss.</p>
              </div>
            </div>

            <div className="feature-card card">
              <div className="feature-icon-wrapper fixed">
                <Compass size={20} className="feature-icon" />
              </div>
              <div className="feature-content">
                <h3>Beginner-friendly explanations</h3>
                <p>Toggle between beginner and intermediate modes to get explanations tailored to your skill level.</p>
              </div>
            </div>

            <div className="feature-card card">
              <div className="feature-icon-wrapper sug">
                <Lightbulb size={20} className="feature-icon" />
              </div>
              <div className="feature-content">
                <h3>Upload history</h3>
                <p>Every snippet you upload is saved securely, allowing you to revisit past challenges and solutions.</p>
              </div>
            </div>

            <div className="feature-card card">
              <div className="feature-icon-wrapper brand">
                <Award size={20} className="feature-icon" />
              </div>
              <div className="feature-content">
                <h3>Best practice suggestions</h3>
                <p>Don't just fix bugs—improve your draft with recommendations for cleaner, more efficient patterns.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. LEARNING PATH INTELLIGENCE (INTERACTIVE WRAPPER) */}
      <section className="learning-path-section">
        <div className="container">
          <div className="learning-path-card card">
            <div className="learning-path-info">
              <span className="badge badge-brand mb-12">Unique to CodeSage</span>
              <h2 className="section-title text-left">Learning Path Intelligence — your personal weakness report</h2>
              <p className="learning-path-desc">
                CodeSage tracks your errors across sessions. After a few uploads, it identifies your top recurring mistake patterns and recommends targeted exercises — turning every bug into a lesson.
              </p>
              <button className="btn btn-primary" onClick={() => setCurrentPage('dashboard')}>
                Advanced analytics engine
              </button>
            </div>
            
            {/* Interactive Code Editor Preview with active popover */}
            <div className="learning-path-preview" onClick={() => handleStartAnalysis('loop')} title="Click to debug this code in CodeSage!">
              <div className="preview-editor-header">
                <span className="dot dot-red" />
                <span className="dot dot-yellow" />
                <span className="dot dot-green" />
              </div>
              <div className="preview-editor-body">
                <div className="code-line"><span className="line-num">1</span><span className="keyword">def</span> <span className="func">calculate_total</span>(prices):</div>
                <div className="code-line"><span className="line-num">2</span>    total = <span className="num">0</span></div>
                <div className="code-line err-highlight"><span className="line-num">3</span>    <span className="keyword">for</span> i <span className="keyword">in</span> <span className="builtin">range</span>(<span className="builtin">len</span>(prices)):</div>
                <div className="code-line err-highlight-row"><span className="line-num">4</span>        tax = i * <span className="danger">price</span> <span className="comment"># Error here</span></div>
                <div className="code-line"><span className="line-num">5</span>        total += p</div>
                <div className="code-line"><span className="line-num">6</span>    <span className="keyword">return</span> total</div>
                
                {/* Insights Popover Box */}
                <div className="insights-popover animate-fade">
                  <div className="popover-title">💡 Insights</div>
                  <p className="popover-text">
                    You often confuse singular/plural variable names in loops. Recommended: naming convention module.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. TESTIMONIALS */}
      <section className="testimonials-section">
        <div className="container">
          <div className="section-header text-center">
            <h2 className="section-title">Loved by students worldwide</h2>
          </div>

          <div className="testimonials-grid">
            <div className="testimonial-card card">
              <div className="star-rating">
                {[...Array(5)].map((_, i) => <Star key={i} size={16} fill="#F59E0B" color="#F59E0B" />)}
              </div>
              <p className="testimonial-text">
                "CodeSage helped me pass my CS101 final. The plain-English explanations for my Python code were way better than any forum post."
              </p>
              <div className="testimonial-user">
                <div className="avatar">AJ</div>
                <div>
                  <h4 className="user-name">Alex Rivera</h4>
                  <p className="user-role">Sophomore, Stanford</p>
                </div>
              </div>
            </div>

            <div className="testimonial-card card">
              <div className="star-rating">
                {[...Array(5)].map((_, i) => <Star key={i} size={16} fill="#F59E0B" color="#F59E0B" />)}
              </div>
              <p className="testimonial-text">
                "The weakness report is a game-changer. I don't keep making the same memory management mistakes in C++ code now."
              </p>
              <div className="testimonial-user">
                <div className="avatar">SL</div>
                <div>
                  <h4 className="user-name">Sarah Lee</h4>
                  <p className="user-role">Self-Taught Developer</p>
                </div>
              </div>
            </div>

            <div className="testimonial-card card">
              <div className="star-rating">
                {[...Array(5)].map((_, i) => <Star key={i} size={16} fill="#F59E0B" color="#F59E0B" />)}
              </div>
              <p className="testimonial-text">
                "As a TA, I recommend this to all my students. It acts as a 24/7 tutor that guides them instead of just giving the answers."
              </p>
              <div className="testimonial-user">
                <div className="avatar">RM</div>
                <div>
                  <h4 className="user-name">Rishi Mittal</h4>
                  <p className="user-role">Graduate TA, MIT</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. PRICING SECTION */}
      <section className="pricing-section" id="pricing-section">
        <div className="container">
          <div className="section-header text-center">
            <h2 className="section-title">Ready to master your code?</h2>
          </div>

          <div className="pricing-grid">
            {/* Free */}
            <div className="pricing-card card">
              <h3 className="tier-name">Free</h3>
              <div className="price-tag">
                <span className="currency">₹</span>
                <span className="price-amount">0</span>
                <span className="period">/month</span>
              </div>
              <p className="tier-desc">Essential tutoring</p>
              
              <ul className="tier-features">
                <li>✓ 10 snippets per day</li>
                <li>✓ Standard bug detection</li>
                <li>✓ Weakness report dashboard</li>
                <li>✓ Targeted exercise sets</li>
                <li>✓ Community support</li>
                <li>✓ Basic explanations</li>
              </ul>
              
              <button className="btn btn-secondary pricing-btn" onClick={() => { setSelectedPlan('free'); setCurrentPage('payment'); }}>
                Get started
              </button>
            </div>

            {/* Pro */}
            <div className="pricing-card card pro-card">
              <div className="popular-badge">MOST POPULAR</div>
              <h3 className="tier-name">Pro</h3>
              <div className="price-tag">
                <span className="currency">₹</span>
                <span className="price-amount">299</span>
                <span className="period">/month</span>
              </div>
              <p className="tier-desc">Advanced analysis</p>
              
              <ul className="tier-features">
                <li>✓ Unlimited snippets</li>
                <li>✓ Deep logic analysis</li>
                <li>✓ Priority AI processing</li>
              </ul>
              
              <button className="btn btn-primary pricing-btn" onClick={() => { setSelectedPlan('pro'); setCurrentPage('payment'); }}>
                Start Pro trial
              </button>
            </div>

            {/* Classroom */}
            <div className="pricing-card card">
              <h3 className="tier-name">Classroom</h3>
              <div className="price-tag">
                <span className="currency">₹</span>
                <span className="price-amount">999</span>
                <span className="period">/month</span>
              </div>
              <p className="tier-desc">For teaching teams</p>
              
              <ul className="tier-features">
                <li>✓ Up to 50 student seats</li>
                <li>✓ Shared classroom history</li>
                <li>✓ Common error analytics</li>
                <li>✓ Admin controls</li>
                <li>✓ LMS integration</li>
              </ul>
              
              <button className="btn btn-secondary pricing-btn" onClick={() => { setSelectedPlan('classroom'); setCurrentPage('payment'); }}>
                Get started
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
