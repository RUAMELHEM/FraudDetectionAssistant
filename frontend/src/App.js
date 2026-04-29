import { useState } from 'react';
import LandingPage from './LandingPage';
import Dashboard   from './Dashboard';

export default function App() {
  const [page, setPage] = useState('landing');
  const [lang, setLang] = useState('en');

  if (page === 'dashboard')
    return <Dashboard lang={lang} setLang={setLang} onBack={() => setPage('landing')} />;

  return <LandingPage lang={lang} setLang={setLang} onStartFree={() => setPage('dashboard')} />;
}
