
import { useState, useRef, useEffect } from 'react';
import './App.css';

// API configuration 
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'; 

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isClearing, setIsClearing] = useState(false);
  const fileInputRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMessage, top_k: 3 })
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();
      
      // Add assistant message
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.answer,
        sources: data.sources 
      }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    
    // Add system message
    setMessages(prev => [...prev, { 
      role: 'system', 
      content: `Uploading ${file.name}...` 
    }]);

    try {
      // Validate file size (limit to 50MB)
      const maxSize = 50 * 1024 * 1024;
      if (file.size > maxSize) {
        throw new Error(`File too large. Max size: 50MB`);
      }

      // Validate file type
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/csv'];
      if (!allowedTypes.includes(file.type)) {
        throw new Error(`Unsupported file type: ${file.type}. Allowed: PDF, DOCX, CSV`);
      }

      const formData = new FormData();
      formData.append('file', file);

      console.log(`Uploading file to: ${API_URL}/upload`);

      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
        headers: {
          
        }
      });

      const responseText = await response.text();
      console.log('Upload response:', responseText);

      if (!response.ok) {
        try {
          const error = JSON.parse(responseText);
          throw new Error(error.detail || `HTTP ${response.status}: Upload failed`);
        } catch {
          throw new Error(`HTTP ${response.status}: ${responseText}`);
        }
      }

      const data = JSON.parse(responseText);
      
      // Update system message with success
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          role: 'system',
          content: `✓ ${file.name} uploaded successfully! (${data.chunks_processed} chunks processed)`
        };
        return newMessages;
      });
    } catch (error) {
      console.error('Upload error:', error);
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          role: 'system',
          content: `✗ Upload failed: ${error.message}`
        };
        return newMessages;
      });
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearDatabase = async () => {
  if (!window.confirm('Clear all uploaded documents? This cannot be undone.')) {
    return;
  }

  setIsClearing(true);
  
  try {
    const response = await fetch(`${API_URL}/clear`, {
      method: 'DELETE', 
    });

    if (!response.ok) {
      throw new Error('Failed to clear database');
    }

    // Clear messages and show success
    setMessages([{
      role: 'system',
      content: '✓ All documents cleared successfully. You can now upload new documents.'
    }]);
    
  } catch (error) {
    console.error('Clear error:', error);
    setMessages(prev => [...prev, {
      role: 'system',
      content: `✗ Failed to clear database: ${error.message}`
    }]);
  } finally {
    setIsClearing(false);
  }
};
  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="logo">
          <span className="logo-icon">🦊</span>
          <span className="logo-text">FileFox</span>
        </div>
        <button 
          className="clear-button"
          onClick={handleClearDatabase}
          disabled={isClearing}
          title="Clear all documents"
        >
          {isClearing ? '⏳' : '🗑️'} Clear All
        </button>
      </header>

      {/* Chat Container */}
      <main className="chat-container">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">🦊</div>
            <h1>Welcome to FileFox</h1>
            <p>Upload documents and ask questions about them</p>
            <div className="welcome-features">
              <div className="feature">
                <span>📄</span>
                <span>PDF, DOCX, CSV</span>
              </div>
              <div className="feature">
                <span>🔍</span>
                <span>Semantic Search</span>
              </div>
              <div className="feature">
                <span>🤖</span>
                <span>AI-Powered Answers</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                {msg.role === 'user' && <div className="avatar user-avatar">You</div>}
                {msg.role === 'assistant' && <div className="avatar bot-avatar">🦊</div>}
                {msg.role === 'system' && <div className="avatar system-avatar">📋</div>}
                
                <div className="message-content">
                  <div className="message-text">{msg.content}</div>
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="sources">
                      <div className="sources-title">Sources:</div>
                      {msg.sources.map((source, sidx) => (
                        <div key={sidx} className="source-item">
                          <span className="source-filename">{source.filename}</span>
                          <span className="source-score">({(source.score * 100).toFixed(0)}% match)</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="avatar bot-avatar">🦊</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      {/* Input Area */}
      <footer className="input-area">
        <div className="input-container">
          <button 
            className="upload-button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            title="Upload document"
          >
            📎
          </button>
          
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileUpload}
            accept=".pdf,.docx,.csv"
            style={{ display: 'none' }}
          />
          
          <textarea
            className="message-input"
            placeholder="Ask a question about your documents..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            rows={1}
          />
          
          <button 
            className="send-button"
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
          >
            ↑
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;
