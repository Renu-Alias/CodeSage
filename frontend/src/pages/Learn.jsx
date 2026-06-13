import React, { useState, useEffect, useRef } from 'react';
import { BookOpen, Compass, Award, Star, CheckCircle, XCircle, ArrowRight, RefreshCw, Lightbulb, Flame, Zap, Trophy, Code, Hash, Terminal, Braces, Globe, Database, FileJson, FileType, Cpu } from 'lucide-react';
import { EXERCISES, LANGUAGE_WEAKNESS_MAP } from '../constants/exercises';

const LANG_ICONS = {
  Python: <Terminal size={18} />,
  JavaScript: <FileJson size={18} />,
  TypeScript: <FileType size={18} />,
  'C++': <Code size={18} />,
  Java: <Cpu size={18} />,
  Go: <Terminal size={18} />,
  Rust: <Braces size={18} />,
  C: <Code size={18} />,
  Dart: <Hash size={18} />,
  Ruby: <GemIcon />,
  PHP: <Code size={18} />,
  Swift: <Braces size={18} />,
  Kotlin: <Terminal size={18} />,
  'C#': <Hash size={18} />,
  SQL: <Database size={18} />,
  HTML: <Globe size={18} />,
  CSS: <FileType size={18} />,
};

function GemIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 3h12l4 6-10 12L2 9Z" />
    </svg>
  );
}

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function pickUnseen(allQuestions, seenSet) {
  const unseen = allQuestions
    .map((q, i) => ({ q, i }))
    .filter(({ i }) => !seenSet.has(i));
  if (unseen.length >= 2) {
    const picked = shuffle(unseen).slice(0, allQuestions.length);
    return picked.map(({ q }) => q);
  }
  return shuffle(allQuestions);
}

export default function Learn({ setCurrentPage }) {
  const [selectedLang, setSelectedLang] = useState('Python');
  const [currentQ, setCurrentQ] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [shuffled, setShuffled] = useState(() => shuffle(EXERCISES.Python));
  const [xp, setXp] = useState(() => Math.floor(Math.random() * 200 + 200));
  const [streak, setStreak] = useState(() => Math.floor(Math.random() * 10 + 1));
  const [solved, setSolved] = useState(() => Math.floor(Math.random() * 30 + 20));
  const [seenIndices, setSeenIndices] = useState(() => ({}));
  const pillsRef = useRef(null);
  const isPerfectRef = useRef(false);
  const currentIndicesRef = useRef(null);

  const exercises = shuffled;

  const allQuestions = EXERCISES[selectedLang] || EXERCISES.Python;

  useEffect(() => {
    currentIndicesRef.current = exercises.map((q) => allQuestions.indexOf(q));
  }, [exercises, allQuestions]);

  const initLang = (lang, fresh) => {
    const pool = fresh
      ? pickUnseen(allQuestions, seenIndices[lang] || new Set())
      : shuffle(allQuestions);
    setShuffled(pool);
    setCurrentQ(0);
    setSelectedAnswer(null);
    setScore(0);
    setAnswered(0);
    setShowResult(false);
  };

  useEffect(() => {
    initLang(selectedLang, false);
  }, [selectedLang]);

  useEffect(() => {
    initLang(selectedLang, false);
  }, []);

  const handleAnswer = (idx) => {
    if (selectedAnswer !== null) return;
    setSelectedAnswer(idx);
    setAnswered(answered + 1);
    if (idx === exercises[currentQ].correct) {
      setScore(score + 1);
      setXp(xp + 10);
    }
  };

  const handleNext = () => {
    if (currentQ + 1 < exercises.length) {
      setCurrentQ(currentQ + 1);
      setSelectedAnswer(null);
    } else {
      isPerfectRef.current = score === exercises.length;
      setShowResult(true);
      setSolved(solved + score);
    }
  };

  const handleRestart = () => {
    const pool = score === exercises.length
      ? pickUnseen(allQuestions, seenIndices[selectedLang] || new Set())
      : shuffle(allQuestions);
    const seen = { ...seenIndices };
    if (score === exercises.length) {
      const idxSet = new Set(seen[selectedLang] || []);
      currentIndicesRef.current?.forEach((i) => idxSet.add(i));
      seen[selectedLang] = idxSet;
    }
    setSeenIndices(seen);
    setShuffled(pool);
    setCurrentQ(0);
    setSelectedAnswer(null);
    setScore(0);
    setAnswered(0);
    setShowResult(false);
  };

  const handleLangChange = (lang) => {
    setSelectedLang(lang);
    const pool = shuffle(EXERCISES[lang] || EXERCISES.Python);
    setShuffled(pool);
    setCurrentQ(0);
    setSelectedAnswer(null);
    setScore(0);
    setAnswered(0);
    setShowResult(false);
  };

  const weaknesses = LANGUAGE_WEAKNESS_MAP[selectedLang] || [];
  const allLangs = Object.keys(EXERCISES);
  const progressPct = exercises.length > 0 ? (answered / exercises.length) * 100 : 0;

  return (
    <div className="learn-page animate-fade container">
      {/* HERO */}
      <section className="learn-hero text-center">
        <div className="practice-hero-gradient" />
        <h1 className="hero-title gradient-text">Practice Exercises</h1>
        <p className="hero-subtitle">Master coding concepts through interactive quizzes and challenges.</p>

        {/* STATS ROW */}
        <div className="practice-stats-row">
          <div className="practice-stat-card">
            <div className="practice-stat-icon streak"><Flame size={20} /></div>
            <div className="practice-stat-info">
              <span className="practice-stat-value">{streak} Day Streak</span>
              <span className="practice-stat-label">Keep going!</span>
            </div>
          </div>
          <div className="practice-stat-card">
            <div className="practice-stat-icon xp"><Zap size={20} /></div>
            <div className="practice-stat-info">
              <span className="practice-stat-value">{xp} XP</span>
              <span className="practice-stat-label">Total earned</span>
            </div>
          </div>
          <div className="practice-stat-card">
            <div className="practice-stat-icon solved"><CheckCircle size={20} /></div>
            <div className="practice-stat-info">
              <span className="practice-stat-value">{solved} Solved</span>
              <span className="practice-stat-label">Questions</span>
            </div>
          </div>
        </div>

        {/* LANGUAGE PILLS — scrollable */}
        <div className="practice-lang-pills-wrapper">
          <div className="practice-lang-pills" ref={pillsRef}>
            {allLangs.slice(0, 14).map(lang => (
              <button
                key={lang}
                className={`practice-lang-pill${selectedLang === lang ? ' active' : ''}`}
                onClick={() => handleLangChange(lang)}
              >
                <span className="practice-lang-icon">{LANG_ICONS[lang] || <Code size={18} />}</span>
                <span className="practice-lang-name">{lang}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* CATEGORY CARDS */}
      <section className="practice-categories">
        {weaknesses.slice(0, 3).map((w, i) => {
          const count = Math.floor(Math.random() * 15 + 10);
          const pct = Math.min(100, Math.floor(Math.random() * 60 + 30));
          const colors = ['#6366F1', '#8B5CF6', '#F59E0B'];
          return (
            <div key={i} className="practice-category-card" style={{ '--accent': colors[i] }}>
              <div className="practice-category-top">
                <span className="practice-category-name">{w}</span>
                <span className="practice-category-count">{count} issues</span>
              </div>
              <div className="practice-category-bar-bg">
                <div className="practice-category-bar-fill" style={{ width: `${pct}%`, background: colors[i] }} />
              </div>
              <span className="practice-category-pct">{pct}%</span>
            </div>
          );
        })}
      </section>

      {/* QUIZ CARD */}
      <section className="practice-quiz-section">
        {showResult ? (
          <div className="practice-quiz-card">
            <div className="practice-result">
              <div className={`practice-result-icon ${score === exercises.length ? 'perfect' : 'good'}`}>
                {score === exercises.length ? <Trophy size={56} /> : <Star size={56} />}
              </div>
              <h3 className="practice-result-title">
                {score === exercises.length ? 'Perfect score!' : 'Practice makes perfect!'}
              </h3>
              <p className="practice-result-desc">
                You got <strong>{score}</strong> out of <strong>{exercises.length}</strong> correct in {selectedLang}.
              </p>
              <div className="practice-result-xp">+{score * 10} XP earned</div>
              <button className="btn btn-primary practice-restart-btn" onClick={handleRestart}>
                <RefreshCw size={16} /> {score === exercises.length ? 'Take another test' : 'Try again'}
              </button>
            </div>
          </div>
        ) : (
          <>
            {/* PROGRESS BAR */}
            <div className="practice-progress-bar-container">
              <div className="practice-progress-label-row">
                <span className="practice-progress-label">Progress</span>
                <span className="practice-progress-pct">{Math.round(progressPct)}%</span>
              </div>
              <div className="practice-progress-bg">
                <div className="practice-progress-fill" style={{ width: `${progressPct}%` }} />
              </div>
            </div>

            {/* STEP INDICATOR */}
            <div className="practice-step-dots">
              {exercises.map((_, i) => (
                <span key={i} className={`practice-step-dot${i === currentQ ? ' active' : ''}${i < currentQ ? ' done' : ''}`} />
              ))}
            </div>

            <div className="practice-quiz-card">
              <div className="practice-quiz-header">
                <span className="practice-quiz-counter">Question {currentQ + 1} of {exercises.length}</span>
                <span className="practice-quiz-score"><Star size={14} /> {score}/{answered}</span>
              </div>

              <div className="practice-question">
                <p>{exercises[currentQ].question}</p>
              </div>

              <div className="practice-options">
                {exercises[currentQ].options.map((opt, idx) => {
                  let cls = 'practice-option';
                  if (selectedAnswer !== null) {
                    if (idx === exercises[currentQ].correct) cls += ' correct';
                    else if (idx === selectedAnswer) cls += ' wrong';
                  }
                  return (
                    <div key={idx} className={cls} onClick={() => handleAnswer(idx)}>
                      <span className="practice-option-letter">{String.fromCharCode(65 + idx)}</span>
                      <span className="practice-option-text">{opt}</span>
                      {selectedAnswer !== null && idx === exercises[currentQ].correct && <CheckCircle size={20} className="practice-option-check" />}
                      {selectedAnswer !== null && idx === selectedAnswer && idx !== exercises[currentQ].correct && <XCircle size={20} className="practice-option-x" />}
                    </div>
                  );
                })}
              </div>

              {selectedAnswer !== null && (
                <div className="practice-explanation">
                  <div className="practice-explanation-icon">
                    {selectedAnswer === exercises[currentQ].correct ? <CheckCircle size={20} /> : <XCircle size={20} />}
                  </div>
                  <div className="practice-explanation-content">
                    <span className="practice-explanation-label">
                      {selectedAnswer === exercises[currentQ].correct ? 'Correct!' : 'Not quite'}
                    </span>
                    <p className="practice-explanation-text">{exercises[currentQ].explanation}</p>
                  </div>
                </div>
              )}

              {selectedAnswer !== null && (
                <button className="btn btn-primary practice-next-btn" onClick={handleNext}>
                  {currentQ + 1 < exercises.length ? 'Next question' : 'See results'} <ArrowRight size={16} />
                </button>
              )}
            </div>
          </>
        )}
      </section>
    </div>
  );
}
