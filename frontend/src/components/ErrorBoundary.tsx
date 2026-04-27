import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  errorMsg: string;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    errorMsg: ''
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, errorMsg: error.message };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--bg-color)' }}>
          <div className="glass-panel" style={{ padding: '3rem', textAlign: 'center', maxWidth: '500px' }}>
            <AlertTriangle size={48} color="var(--error)" style={{ marginBottom: '1rem' }} />
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--text-primary)' }}>System Interruption</h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
              We encountered an unexpected error. The system architecture protected the core processes, but this view needs to be reloaded.
            </p>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '2rem', fontFamily: 'monospace' }}>
              {this.state.errorMsg}
            </p>
            <button 
              className="glass-button primary"
              onClick={() => window.location.reload()}
            >
              Reinitialize Session
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
