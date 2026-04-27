import React, { useState, useEffect } from 'react';
import { Search, Activity, LogOut } from 'lucide-react';
import NewsGrid from './components/NewsGrid';
import { Login, Register } from './components/Auth';
import './index.css';

import IntelligenceDigest from './components/IntelligenceDigest';

const API_BASE = 'http://localhost:8000';
const CATEGORIES = ['All', 'Finance', 'Tech', 'Science', 'Politics', 'Sports', 'Health'];

const App: React.FC = () => {
  // Auth State
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<any>(null);
  const [authView, setAuthView] = useState<'login' | 'register'>('login');

  // Dashboard State
  const [nodes, setNodes] = useState<any[]>([]);
  const [selectedNode, setSelectedNode] = useState<any | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(false);

  // Helper to fetch with auth
  const fetchWithAuth = async (endpoint: string, options: RequestInit = {}) => {
    const headers = new Headers(options.headers || {});
    if (token) headers.set('Authorization', `Bearer ${token}`);
    
    const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
    if (response.status === 401) {
      handleLogout();
      throw new Error('Unauthorized');
    }
    return response;
  };

  useEffect(() => {
    if (token) {
      fetchNodes('All');
      // Optionally fetch user profile if needed
      fetchWithAuth('/auth/me/')
        .then(res => res.json())
        .then(data => { if (data.status === 'success') setUser(data.user); })
        .catch(console.error);
    }
  }, [token]);

  const handleAuthSuccess = (newToken: string, newUser: any) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    setUser(newUser);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    setNodes([]);
  };

  const fetchNodes = async (category: string) => {
    setLoading(true);
    try {
      const res = await fetchWithAuth(`/?category=${category}`);
      const data = await res.json();
      setNodes(data.nodes || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return fetchNodes(selectedCategory);
    
    setLoading(true);
    try {
      const res = await fetchWithAuth(`/search/?q=${encodeURIComponent(searchQuery)}`);
      const data = await res.json();
      setNodes(data.nodes || []);
      setSelectedCategory('All');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryClick = (cat: string) => {
    setSelectedCategory(cat);
    fetchNodes(cat);
  };

  const handleSummarize = async (id: number) => {
    try {
      const res = await fetchWithAuth(`/summarize/${id}/`, { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        setNodes(prev => prev.map(n => n.id === id ? { ...n, ...data.node } : n));
        setSelectedNode((prev: any) => prev && prev.id === id ? { ...prev, ...data.node } : prev);
      }
    } catch (err) {
      console.error('Summarize failed', err);
    }
  };

  // Auth Routing
  if (!token) {
    return authView === 'login' 
      ? <Login onAuthSuccess={handleAuthSuccess} toggleView={() => setAuthView('register')} />
      : <Register onAuthSuccess={handleAuthSuccess} toggleView={() => setAuthView('login')} />;
  }

  return (
    <div className="container">
      {/* Enterprise Full-Screen Digest */}
      {selectedNode && (
        <IntelligenceDigest 
          node={selectedNode} 
          onClose={() => setSelectedNode(null)} 
          onSummarize={() => handleSummarize(selectedNode.id)}
        />
      )}

      <header className="header">
        <div>
          <h1 className="header-title">AI News Analyst</h1>
          {user && <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>Welcome, {user.first_name || user.email}</p>}
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button className="glass-button" onClick={handleLogout} style={{ padding: '0.5rem 1rem' }} title="Sign Out">
            <LogOut size={18} />
          </button>
        </div>
      </header>

      <form className="search-container" onSubmit={handleSearch} style={{ position: 'relative', width: '100%', marginBottom: '1.5rem' }}>
        <div style={{ position: 'relative', width: '100%' }}>
          <Search className="search-icon" size={20} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input 
            type="text" 
            className="glass-input search-input" 
            placeholder="Search global news or knowledge base..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ width: '100%', paddingLeft: '3rem' }}
          />
        </div>
      </form>

      <div className="categories-container" style={{ display: 'flex', gap: '1rem', marginBottom: '3rem', overflowX: 'auto', paddingBottom: '0.5rem' }}>
        {CATEGORIES.map(cat => (
          <button
            key={cat}
            className={`glass-button category-btn ${selectedCategory === cat ? 'active' : ''}`}
            onClick={() => handleCategoryClick(cat)}
            style={{ 
              padding: '0.5rem 1.25rem', 
              borderRadius: '20px', 
              fontSize: '0.9rem',
              whiteSpace: 'nowrap',
              background: selectedCategory === cat ? 'var(--accent-primary)' : 'var(--card-bg)',
              border: selectedCategory === cat ? '1px solid var(--accent-primary)' : '1px solid var(--card-border)',
              color: selectedCategory === cat ? 'white' : 'var(--text-secondary)'
            }}
          >
            {cat}
          </button>
        ))}
      </div>

      <main>
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '4rem', color: 'var(--accent-primary)' }}>
            <Activity size={32} className="spinner" />
          </div>
        ) : (
          <section style={{ marginBottom: '4rem' }}>
            <h2 style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-primary)' }}></span>
              Latest Intelligence
            </h2>
            <div style={{ 
              padding: '2rem', 
              borderRadius: '24px', 
              background: 'var(--card-bg)',
              border: '1px solid var(--card-border)',
              boxShadow: '0 10px 25px -5px rgba(0,0,0,0.05)',
              position: 'relative'
            }}>
              <div style={{ position: 'absolute', top: 0, left: 0, width: '4px', height: '100%', background: 'var(--accent-primary)', borderTopLeftRadius: '24px', borderBottomLeftRadius: '24px' }}></div>
              <NewsGrid nodes={nodes} onSummarize={handleSummarize} onNodeClick={setSelectedNode} emptyMessage="No intelligence found for your query." />
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default App;
