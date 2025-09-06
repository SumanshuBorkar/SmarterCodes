import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [indexing, setIndexing] = useState(false);

  useEffect(() => {
    if (!url) return;
    const timer = setTimeout(() => {
      handleIndex();
    }, 1000);
    return () => clearTimeout(timer);
  }, [url]);

  const handleIndex = useCallback(async () => {
    if (!url) return;
    setIndexing(true);
    setError('');
    setSuccess('');

    try {
      const res = await axios.post('http://localhost:8000/index', { 
        url, 
        query: 'placeholder'
      });
      setSuccess(res.data.message || 'URL indexed successfully!');
    } catch (err) {
      console.error(err);
      setError('Failed to index URL. Please try again later.');
    } finally {
      setIndexing(false);
    }
  }, [url]);

  const handleSearch = async () => {
    if (!url || !query) {
      setError('Please enter both URL and query.');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');
    setResults([]);

    try {
      const res = await axios.post('http://localhost:8000/search', { url, query });
      const searchData = res.data;

      const matches = searchData.results.map((result) => ({
        text: result.content,
        score: Math.max(0, 1 - result.score / 2), 
        tag: `chunk-${result.chunk_id}`,
        html: result.content.substring(0, 100) + '...',
        path: url,
        chunk_id: result.chunk_id,
        original_score: result.score,
        has_code: result.has_code,
        language: result.language,
        token_count: result.token_count,
        character_count: result.character_count
      }));

      if (matches.length > 0) {
        setResults(matches);
      } else {
        setError('No relevant results found.');
      }
    } catch (err) {
      console.error(err);
      setError('Failed to fetch results. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      setSuccess('Copied to clipboard!');
      setTimeout(() => setSuccess(''), 2000);
    } catch {
      setError('Failed to copy content.');
    }
  };

  const getFullUrl = (path) => {
    try {
      const base = new URL(url);
      return new URL(path, base).href;
    } catch {
      return url;
    }
  };

  const formatCode = (text, language) => (
    <SyntaxHighlighter
      language={language || 'text'}
      style={atomDark}
      showLineNumbers
      wrapLines
      className="code-block"
    >
      {text}
    </SyntaxHighlighter>
  );

  return (
    <div className="App">
      <h1>Website Content Search</h1>
       <h3>Search through website content with precision</h3>
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter website URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={indexing}
          className='url-input'
        />
       <div className='SearchDiv'>
       <input
          type="text"
          placeholder="Enter search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className='url-input'
        />
        <button className='search-btn' onClick={handleSearch} disabled={loading || !url || !query}>
          {loading ? 'Searching...' : 'Search'}
        </button>
       </div>
      </div>

      {/* ✅ Inline feedback */}
      {indexing && <p className="info">Indexing website...</p>}
      {error && <p className="error">{error}</p>}
      {success && <p className="success">{success}</p>}

      {Array.isArray(results) && results.length > 0 && (
        <div className="results">
          <h2>Search Results</h2>
          {results.map((match, idx) => (
            <div className="result-card" key={idx}>
              <p>
                <strong>Relevance:</strong>
                <span style={{ color: 'green' }}>
                  {(match.score * 100).toFixed(1)} %
                </span>
                <span style={{ color: '#666', fontSize: '12px', marginLeft: '10px' }}>
                  (Distance: {match.original_score.toFixed(4)})
                </span>
              </p>

              <p>
                <strong>Chunk ID:</strong> <code>{match.chunk_id}</code>
                <span style={{ marginLeft: '15px' }}>
                  <strong>Size:</strong> {match.token_count} tokens, {match.character_count} chars
                </span>
              </p>

              {match.has_code ? (
                <div>
                  <p><strong>Code Content ({match.language || 'unknown'}):</strong></p>
                  {formatCode(match.text, match.language)}
                </div>
              ) : (
                <div>
                  <p><strong>Text Content:</strong></p>
                  <div className="text-content">{match.text}</div>
                </div>
              )}

              <p>
                <strong>Source URL:</strong>{' '}
                <a href={getFullUrl(match.path)} target="_blank" rel="noopener noreferrer">
                  {match.path}
                </a>
              </p>

              <button onClick={() => handleCopy(match.text)}>Copy Content</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
