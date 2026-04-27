import React, { useState } from 'react';

interface AuthProps {
  onAuthSuccess: (token: string, user: any) => void;
  toggleView: () => void;
}

export const Login: React.FC<AuthProps> = ({ onAuthSuccess, toggleView }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      
      if (data.status === 'success') {
        onAuthSuccess(data.token, data.user);
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      setError('System connection failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ position: 'relative', minHeight: '100vh', backgroundColor: 'var(--bg-color)' }}>
      <div style={{ position: 'absolute', top: '2rem', left: '2rem', fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
        AI News Analyst
      </div>
      <div style={{ maxWidth: '400px', margin: '0 auto', paddingTop: '15vh', animation: 'fadeIn 0.5s ease-out' }}>
        <div className="glass-panel" style={{ padding: '2.5rem' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem', fontWeight: 700, textAlign: 'center' }}>Welcome Back</h2>
          <p style={{ color: 'var(--text-muted)', textAlign: 'center', marginBottom: '2rem' }}>Authenticate to access the intelligence dashboard.</p>
          
          {error && <div style={{ background: '#fee2e2', color: '#dc2626', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>{error}</div>}
          
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: '0.25rem', color: 'var(--text-secondary)' }}>Email Address</label>
              <input type="email" required className="glass-input" value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: '0.25rem', color: 'var(--text-secondary)' }}>Password</label>
              <input type="password" required className="glass-input" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
            <button type="submit" disabled={loading} className="glass-button primary" style={{ marginTop: '1rem', padding: '1rem' }}>
              {loading ? 'Authenticating...' : 'Sign In'}
            </button>
          </form>
          
          <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Don't have an access node? <button onClick={toggleView} style={{ background: 'none', border: 'none', color: 'var(--accent-primary)', fontWeight: 600, cursor: 'pointer' }}>Register</button>
          </p>
        </div>
      </div>
    </div>
  );
};

export const Register: React.FC<AuthProps> = ({ onAuthSuccess, toggleView }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://localhost:8000/auth/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, first_name: firstName })
      });
      const data = await res.json();
      
      if (data.status === 'success') {
        onAuthSuccess(data.token, data.user);
      } else {
        setError(data.message || 'Registration failed');
      }
    } catch (err) {
      setError('System connection failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ position: 'relative', minHeight: '100vh', backgroundColor: 'var(--bg-color)' }}>
      <div style={{ position: 'absolute', top: '2rem', left: '2rem', fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
        AI News Analyst
      </div>
      <div style={{ maxWidth: '400px', margin: '0 auto', paddingTop: '15vh', animation: 'fadeIn 0.5s ease-out' }}>
        <div className="glass-panel" style={{ padding: '2.5rem' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '0.5rem', fontWeight: 700, textAlign: 'center' }}>Request Access</h2>
          <p style={{ color: 'var(--text-muted)', textAlign: 'center', marginBottom: '2rem' }}>Create a new intelligence clearance profile.</p>
          
          {error && <div style={{ background: '#fee2e2', color: '#dc2626', padding: '0.75rem', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.9rem', textAlign: 'center' }}>{error}</div>}
          
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: '0.25rem', color: 'var(--text-secondary)' }}>First Name</label>
              <input type="text" className="glass-input" value={firstName} onChange={e => setFirstName(e.target.value)} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: '0.25rem', color: 'var(--text-secondary)' }}>Email Address</label>
              <input type="email" required className="glass-input" value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 500, marginBottom: '0.25rem', color: 'var(--text-secondary)' }}>Password</label>
              <input type="password" required className="glass-input" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
            <button type="submit" disabled={loading} className="glass-button primary" style={{ marginTop: '1rem', padding: '1rem' }}>
              {loading ? 'Processing...' : 'Register'}
            </button>
          </form>
          
          <p style={{ textAlign: 'center', marginTop: '1.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
            Already have clearance? <button onClick={toggleView} style={{ background: 'none', border: 'none', color: 'var(--accent-primary)', fontWeight: 600, cursor: 'pointer' }}>Sign In</button>
          </p>
        </div>
      </div>
    </div>
  );
};
