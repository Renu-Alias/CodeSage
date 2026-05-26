import React, { useState, useEffect, useRef } from 'react';
import { Upload, Play, Copy, Check, Terminal, AlertCircle, Sparkles, FileText, ChevronRight } from 'lucide-react';
import { LANGUAGES, extToLanguage, acceptExtensions } from '../constants/languages';

const DEFAULT_SNIPPETS = {
  Python: `def calculate_average(numbers):
    total = sum(numbers)
    # Bug: division without zero check
    return total / len(numbers)`,
  JavaScript: `function calculateAverage(numbers) {
  let total = 0;
  for (let i = 0; i <= numbers.length; i++) {
    total += numbers[i];
  }
  return total / numbers.length;
}`,
  TypeScript: `function calculateAverage(numbers: number[]): number {
  let total = 0;
  for (let i = 0; i <= numbers.length; i++) {
    total += numbers[i];
  }
  return total / numbers.length;
}`,
  'C++': `#include <iostream>
using namespace std;

int main() {
  int numbers[5] = {1, 2, 3, 4, 5};
  int total = 0;
  for (int i = 0; i <= 5; i++) {
    total += numbers[i];
  }
  cout << total / 5;
  return 0;
}`,
  Java: `public class Main {
  public static void main(String[] args) {
    int[] numbers = {1, 2, 3, 4, 5};
    int total = 0;
    for (int i = 0; i <= numbers.length; i++) {
      total += numbers[i];
    }
    System.out.println(total / numbers.length);
  }
}`,
  Go: `package main

import "fmt"

func main() {
  numbers := []int{1, 2, 3, 4, 5}
  total := 0
  for i := 0; i <= len(numbers); i++ {
    total += numbers[i]
  }
  fmt.Println(total / len(numbers))
}`,
  Rust: `fn main() {
  let numbers = vec![1, 2, 3, 4, 5];
  let mut total = 0;
  for i in 0..=numbers.len() {
    total += numbers[i];
  }
  println!("{}", total / numbers.len());
}`,
  C: `#include <stdio.h>

int main() {
  int numbers[] = {1, 2, 3, 4, 5};
  int total = 0;
  for (int i = 0; i <= 5; i++) {
    total += numbers[i];
  }
  printf("%d", total / 5);
  return 0;
}`,
  Dart: `void main() {
  List<int> numbers = [1, 2, 3, 4, 5];
  int total = 0;
  for (int i = 0; i <= numbers.length; i++) {
    total += numbers[i];
  }
  print(total / numbers.length);
}`,
  Ruby: `def calculate_average(numbers)
  total = numbers.sum
  total / numbers.length
end

puts calculate_average([1, 2, 3, 4, 5])`,
  PHP: `<?php
function calculateAverage($numbers) {
  $total = array_sum($numbers);
  return $total / count($numbers);
}

echo calculateAverage([1, 2, 3, 4, 5]);
?>`,
  Swift: `func calculateAverage(numbers: [Int]) -> Int {
  let total = numbers.reduce(0, +)
  return total / numbers.count
}

print(calculateAverage(numbers: [1, 2, 3, 4, 5]))`,
  Kotlin: `fun main() {
  val numbers = listOf(1, 2, 3, 4, 5)
  var total = 0
  for (i in 0..numbers.size) {
    total += numbers[i]
  }
  println(total / numbers.size)
}`,
  'C#': `using System;

class Program {
  static void Main() {
    int[] numbers = {1, 2, 3, 4, 5};
    int total = 0;
    for (int i = 0; i <= numbers.Length; i++) {
      total += numbers[i];
    }
    Console.WriteLine(total / numbers.Length);
  }
}`,
  SQL: `SELECT AVG(price) AS average_price
FROM products
WHERE category_id = 1;`,
  HTML: `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My Page</title>
</head>
<body>
  <h1>Hello World</h1>
  <img src="image.jpg" alt="photo">
  <p>This is a paragraph</p>
</body>
</html>`,
  CSS: `.container {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: lightblue;
  padding: 20px;
  margin: 0 auto;
}`,
};

const DEFAULT_FILENAMES = {
  Python: 'calculate_average.py',
  JavaScript: 'calculate_average.js',
  TypeScript: 'calculate_average.ts',
  'C++': 'main.cpp',
  Java: 'Main.java',
  Go: 'main.go',
  Rust: 'main.rs',
  C: 'main.c',
  Dart: 'main.dart',
  Ruby: 'main.rb',
  PHP: 'index.php',
  Swift: 'main.swift',
  Kotlin: 'main.kt',
  'C#': 'Program.cs',
  SQL: 'query.sql',
  HTML: 'index.html',
  CSS: 'styles.css',
};

export default function Analyze({ sampleCode, setSampleCode }) {
  const getInitialSnippet = () => {
    if (sampleCode?.code) return sampleCode.code;
    const lang = sampleCode?.language || 'Python';
    return DEFAULT_SNIPPETS[lang] || DEFAULT_SNIPPETS.Python;
  };

  const getInitialFilename = () => {
    if (sampleCode?.filename) return sampleCode.filename;
    const lang = sampleCode?.language || 'Python';
    return DEFAULT_FILENAMES[lang] || DEFAULT_FILENAMES.Python;
  };

  const [code, setCode] = useState(getInitialSnippet());
  const [language, setLanguage] = useState(sampleCode?.language || "Python");
  const [filename, setFilename] = useState(getInitialFilename());
  const [mode, setMode] = useState("Beginner");
  
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("errors");
  const [copied, setCopied] = useState(false);
  const [saved, setSaved] = useState(true);

  const [errors, setErrors] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [explanation, setExplanation] = useState("### Ready to analyze\n\nPaste your code and click **Analyze** to get started.");
  const [fixedCode, setFixedCode] = useState("");

  // Sync if sampleCode changes from homepage click
  useEffect(() => {
    if (sampleCode) {
      setCode(sampleCode.code);
      setLanguage(sampleCode.language);
      setFilename(sampleCode.filename);
      // Run analysis on sample load immediately
      triggerAnalysis(sampleCode.code, sampleCode.language, mode);
    }
  }, [sampleCode]);

  // Recalculate line numbers
  const linesCount = code.split("\n").length;
  const lineNumbers = Array.from({ length: Math.max(linesCount, 1) }, (_, i) => i + 1);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFilename(file.name);
      // Detect language based on extension
      const detected = extToLanguage(file.name);
      if (detected) setLanguage(detected);

      const reader = new FileReader();
      reader.onload = (event) => {
        setCode(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleCopy = () => {
    const copyContent = activeTab === 'fixed' ? fixedCode : JSON.stringify({ errors, suggestions }, null, 2);
    navigator.clipboard.writeText(copyContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const triggerAnalysis = async (currentCode, currentLang, currentMode) => {
    setLoading(true);
    setSaved(false);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: currentCode,
          language: currentLang,
          mode: currentMode,
          filename: filename
        })
      });

      if (response.ok) {
        const data = await response.json();
        const analysis = data.analysis;
        setErrors(analysis.errors);
        setSuggestions(analysis.suggestions);
        setExplanation(analysis.explanation);
        setFixedCode(analysis.fixed_code);
        setSaved(true);
      } else if (response.status === 500) {
        const errData = await response.json();
        setErrors([{ line: 1, type: "ServerError", message: errData.detail || "Backend server error" }]);
        setSuggestions([]);
        setExplanation("### Server Error\n\nThe backend encountered an error processing your code. Make sure the backend server is running on port 8000.");
        setFixedCode("");
      } else {
        throw new Error("Backend response error");
      }
    } catch (err) {
      setErrors([{ line: 1, type: "ConnectionError", message: "Cannot reach the backend server. Make sure the Python backend is running on port 8000." }]);
      setSuggestions([]);
      setExplanation("### Backend Offline\n\nStart the backend with:\n```bash\ncd backend\npython -m app.main\n```");
      setFixedCode("");
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeClick = () => {
    triggerAnalysis(code, language, mode);
  };

  // Generate beautiful line-by-line comparison diff in the fixed code tab
  const renderFixedDiff = () => {
    const originalLines = code.split('\n');
    const correctedLines = fixedCode.split('\n');

    return (
      <div className="diff-view font-mono">
        {correctedLines.map((line, idx) => {
          const isAdded = !originalLines.includes(line);
          const isRemoved = originalLines.length > idx && !correctedLines.includes(originalLines[idx]);
          
          return (
            <div key={idx} className={`diff-line-row ${isAdded ? 'diff-added' : ''}`}>
              <span className="diff-marker">{isAdded ? '+' : ' '}</span>
              <span className="diff-code-text">{line}</span>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="analyze-page animate-fade container">
      <div className="analyze-grid">
        
        {/* LEFT COLUMN: CODE EDITOR */}
        <div className="editor-card card">
          <div className="editor-card-header">
            <div className="header-left">
              <span className="terminal-title">
                <Terminal size={16} /> Your code
              </span>
            </div>
            
            <div className="header-right">
              {/* Language Selector */}
              <select 
                className="select-dropdown" 
                value={language} 
                onChange={(e) => {
                  const newLang = e.target.value;
                  setLanguage(newLang);
                  setCode(DEFAULT_SNIPPETS[newLang] || DEFAULT_SNIPPETS.Python);
                  setFilename(DEFAULT_FILENAMES[newLang] || DEFAULT_FILENAMES.Python);
                  setErrors([]);
                  setSuggestions([]);
                  setExplanation(`### Ready to analyze\nPaste your ${newLang} code and click Analyze to get started.`);
                  setFixedCode('');
                }}
              >
                {LANGUAGES.map(lang => (
                  <option key={lang.name} value={lang.name}>{lang.name}</option>
                ))}
              </select>

              {/* Upload File button */}
              <label className="btn btn-secondary upload-btn-label">
                <Upload size={14} /> Upload file
                <input type="file" onChange={handleFileUpload} accept={acceptExtensions()} style={{ display: 'none' }} />
              </label>
            </div>
          </div>

          {/* Interactive Code Editor Container */}
          <div className="editor-body-container">
            <div className="line-numbers-sidebar">
              {lineNumbers.map(num => (
                <div key={num} className="line-number-cell">{num}</div>
              ))}
            </div>
            <textarea
              className="code-textarea font-mono"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck="false"
              placeholder="Paste or write your code here..."
            />
          </div>

          {/* Editor Footer Controls */}
          <div className="editor-footer">
            <div className="explain-level-toggle">
              <span className="explain-level-label">Explain as:</span>
              <div className="toggle-btn-group">
                <button 
                  className={`toggle-btn ${mode === 'Beginner' ? 'active' : ''}`}
                  onClick={() => { setMode('Beginner'); triggerAnalysis(code, language, 'Beginner'); }}
                >
                  Beginner
                </button>
                <button 
                  className={`toggle-btn ${mode === 'Intermediate' ? 'active' : ''}`}
                  onClick={() => { setMode('Intermediate'); triggerAnalysis(code, language, 'Intermediate'); }}
                >
                  Intermediate
                </button>
              </div>
            </div>

            <button 
              className={`btn btn-primary analyze-btn ${loading ? 'loading' : ''}`}
              onClick={handleAnalyzeClick}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner" /> Analyzing...
                </>
              ) : (
                <>
                  <Play size={16} fill="white" /> Analyze
                </>
              )}
            </button>
          </div>
        </div>

        {/* RIGHT COLUMN: ANALYSIS REPORT PANEL */}
        <div className="report-card card">
          {/* Tabs Menu Header */}
          <div className="report-tabs-header">
            <button 
              className={`report-tab-btn ${activeTab === 'errors' ? 'active' : ''}`}
              onClick={() => setActiveTab('errors')}
            >
              <span className="tab-bullet err-bullet" /> Errors
              {errors.length > 0 && <span className="tab-badge err-badge">{errors.length}</span>}
            </button>
            <button 
              className={`report-tab-btn ${activeTab === 'suggestions' ? 'active' : ''}`}
              onClick={() => setActiveTab('suggestions')}
            >
              <span className="tab-bullet sug-bullet" /> Suggestions
              {suggestions.length > 0 && <span className="tab-badge sug-badge">{suggestions.length}</span>}
            </button>
            <button 
              className={`report-tab-btn ${activeTab === 'explanation' ? 'active' : ''}`}
              onClick={() => setActiveTab('explanation')}
            >
              <span className="tab-bullet exp-bullet" /> Explanation
            </button>
            <button 
              className={`report-tab-btn ${activeTab === 'fixed' ? 'active' : ''}`}
              onClick={() => setActiveTab('fixed')}
            >
              <span className="tab-bullet fixed-bullet" /> Fixed code
            </button>
          </div>

          {/* Active Tab Panel Content */}
          <div className="report-panel-body">
            
            {/* 1. ERRORS PANEL */}
            {activeTab === 'errors' && (
              <div className="feedback-list animate-fade">
                {errors.length === 0 ? (
                  <div className="empty-panel-state">
                    <div className="empty-icon-check">✓</div>
                    <h3>No critical issues found</h3>
                    <p>Your code structures seem robust. CodeSage didn't find any syntax crashes or logic locks.</p>
                  </div>
                ) : (
                  errors.map((err, idx) => (
                    <div key={idx} className="feedback-card feedback-err">
                      <div className="card-side-indicator indicator-err" />
                      <div className="feedback-card-content">
                        <div className="feedback-meta">
                          <span className="meta-line">Line {err.line}</span>
                          <span className="meta-separator">•</span>
                          <span className="meta-type">{err.type}</span>
                        </div>
                        <p className="feedback-desc">{err.message}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* 2. SUGGESTIONS PANEL */}
            {activeTab === 'suggestions' && (
              <div className="feedback-list animate-fade">
                {suggestions.length === 0 ? (
                  <div className="empty-panel-state">
                    <Sparkles size={36} color="var(--text-light)" />
                    <h3>Up to standard</h3>
                    <p>We don't have any immediate style or clean-code recommendations for this snippet.</p>
                  </div>
                ) : (
                  suggestions.map((sug, idx) => (
                    <div key={idx} className="feedback-card feedback-sug">
                      <div className="card-side-indicator indicator-sug" />
                      <div className="feedback-card-content">
                        <div className="feedback-meta">
                          <span className="meta-line">Line {sug.line}</span>
                          <span className="meta-separator">•</span>
                          <span className="meta-type">{sug.title}</span>
                        </div>
                        <p className="feedback-desc">{sug.message}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* 3. EXPLANATION PANEL */}
            {activeTab === 'explanation' && (
              <div className="markdown-explanation animate-fade">
                {explanation.split('\n\n').map((paragraph, idx) => {
                  if (paragraph.startsWith('###')) {
                    return <h3 key={idx} className="md-header">{paragraph.replace('###', '').trim()}</h3>;
                  }
                  if (paragraph.startsWith('-') || paragraph.startsWith('*')) {
                    return (
                      <ul key={idx} className="md-list">
                        {paragraph.split('\n').map((item, idy) => (
                          <li key={idy}>{item.replace(/^[-*]\s+/, '')}</li>
                        ))}
                      </ul>
                    );
                  }
                  return <p key={idx} className="md-p">{paragraph}</p>;
                })}
              </div>
            )}

            {/* 4. FIXED CODE PANEL */}
            {activeTab === 'fixed' && (
              <div className="fixed-code-panel animate-fade">
                {renderFixedDiff()}
              </div>
            )}

          </div>

          {/* Report Panel Footer Actions */}
          <div className="report-footer">
            <button className="btn btn-secondary icon-btn-text" onClick={handleCopy}>
              {copied ? (
                <>
                  <Check size={14} color="var(--exp-color)" /> Copied
                </>
              ) : (
                <>
                  <Copy size={14} /> Copy
                </>
              )}
            </button>

            {saved && (
              <span className="saved-history-indicator animate-fade">
                <Check size={14} className="check-history-icon" /> Saved to your history
              </span>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
