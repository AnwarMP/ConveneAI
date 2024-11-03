import React, { useEffect, useState } from 'react';
import '../styles/transcript.css';

const TranscriptViewer = () => {
  const [transcript, setTranscript] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTranscript = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://localhost:5000/transcript-gemini', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      if (data.status === 'success' && data.results?.enhanced_transcript) {
        setTranscript(data.results.enhanced_transcript);
      } else {
        throw new Error('Failed to fetch the transcript');
      }
    } catch (error) {
      console.error('Error fetching transcript:', error);
      setError('Failed to fetch the transcript. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTranscript();
  }, []);

  return (
    <div className="transcript-container">
      <div className="transcript-header">
        <h2>Meeting Transcript</h2>
        <button 
          className="transcript-toggle" 
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? "Collapse Transcript" : "Expand Transcript"}
        </button>
      </div>

      {isLoading ? (
        <div className="transcript-loading">
          <div className="loading-spinner"></div>
          <p>Loading transcript...</p>
        </div>
      ) : error ? (
        <div className="transcript-error">
          <p>{error}</p>
        </div>
      ) : (
        <div className={`transcript-content ${isExpanded ? 'expanded' : ''}`}>
          {isExpanded ? (
            <div className="transcript-text">
              {transcript.split('\n').map((line, i) => (
                <div key={i} className="transcript-line">
                  {line}
                </div>
              ))}
            </div>
          ) : (
            <div className="transcript-preview">
              Click "Expand Transcript" to view the enhanced meeting transcript
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TranscriptViewer;
