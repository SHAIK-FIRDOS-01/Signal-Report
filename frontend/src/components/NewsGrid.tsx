import React from 'react';
import NewsCard from './NewsCard';

interface NewsGridProps {
  nodes: any[];
  onSummarize: (id: number) => Promise<void>;
  onNodeClick: (node: any) => void;
  emptyMessage?: string;
}

const NewsGrid: React.FC<NewsGridProps> = ({ nodes, onSummarize, onNodeClick, emptyMessage }) => {
  if (nodes.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }} className="glass-panel">
        <p style={{ fontSize: '1.0rem' }}>{emptyMessage || "No intelligence found for your query."}</p>
      </div>
    );
  }

  return (
    <div className="grid">
      {nodes.map((node, i) => (
        <div key={node.id} style={{ animationDelay: `${i * 0.05}s` }} className="animate-fade-in">
          <NewsCard 
            node={node} 
            onSummarize={() => onSummarize(node.id)} 
            onOpenDigest={() => onNodeClick(node)}
          />
        </div>
      ))}
    </div>
  );
};

export default NewsGrid;
