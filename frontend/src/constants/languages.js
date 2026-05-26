export const LANGUAGES = [
  { name: 'Python',    extensions: ['.py'] },
  { name: 'JavaScript',extensions: ['.js'] },
  { name: 'TypeScript',extensions: ['.ts'] },
  { name: 'C++',       extensions: ['.cpp', '.hpp', '.h'] },
  { name: 'Java',      extensions: ['.java'] },
  { name: 'Go',        extensions: ['.go'] },
  { name: 'Rust',      extensions: ['.rs'] },
  { name: 'C',         extensions: ['.c', '.h'] },
  { name: 'Dart',      extensions: ['.dart'] },
  { name: 'Ruby',      extensions: ['.rb'] },
  { name: 'PHP',       extensions: ['.php'] },
  { name: 'Swift',     extensions: ['.swift'] },
  { name: 'Kotlin',    extensions: ['.kt', '.kts'] },
  { name: 'C#',        extensions: ['.cs'] },
];

export function extToLanguage(filename) {
  const ext = '.' + filename.split('.').pop().toLowerCase();
  for (const lang of LANGUAGES) {
    if (lang.extensions.includes(ext)) return lang.name;
  }
  return null;
}

export function acceptExtensions() {
  return LANGUAGES.flatMap(l => l.extensions).join(',');
}
