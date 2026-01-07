import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send, ShieldCheck, FileText, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown'; // ✅ Import Markdown library
import './ChatPopup.css';

const ChatPopup = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! I'm your Internal Assistant. How can I help you today?", sender: 'bot' }
  ]);
  
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

const handleSend = async (e) => {
  e.preventDefault();
  if (!input.trim() || isLoading) return;

  const userQuery = input;
  // 1. Prepare history BEFORE updating state (to include previous turns)
  const history = messages.map(msg => ({
    role: msg.sender === 'user' ? 'user' : 'assistant',
    content: msg.text
  }));

  setMessages(prev => [...prev, { text: userQuery, sender: 'user' }]);
  setInput('');
  setIsLoading(true);

  try {
    const response = await fetch('http://localhost:8000/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // 2. Send both the current question AND the history
      body: JSON.stringify({ 
        question: userQuery,
        history: history 
      }),
    });

    if (!response.ok) throw new Error('Network response was not ok');
    
    const data = await response.json();
    
    setMessages(prev => [...prev, { 
      text: data.answer, 
      sender: 'bot',
      sources: data.sources,
      confidence: data.confidence 
    }]);
  } catch (error) {
    setMessages(prev => [...prev, { 
      text: "**Connection Error**: I can't reach the server.", 
      sender: 'bot',
      isError: true 
    }]);
  } finally {
    setIsLoading(false);
  }
};

  return (
    <div className="chat-widget">
      {isOpen && (
        <div className="chat-window">
          {/* Header */}
          <div className="chat-header">
            <div className="header-info">
              <ShieldCheck size={20} />
              <span>Internal Query Bot</span>
            </div>
            <X className="close-btn" onClick={() => setIsOpen(false)} />
          </div>

          {/* Messages */}
          <div className="message-container">
            {messages.map((msg, i) => (
              <div key={i} className={`message-row ${msg.sender}`}>
                <div className={`bubble ${msg.sender} ${msg.isError ? 'error' : ''}`}>
                  {/* ✅ Wrap text in ReactMarkdown to render **bold** and lists */}
                  <div className="markdown-content">
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </div>
                  
                  {msg.sources?.length > 0 && (
                    <div className="source-tag">
                      <FileText size={12} />
                      Sources: {msg.sources.join(', ')}
                    </div>
                  )}
                  
                  {msg.confidence && (
                    <div className="confidence-meter">
                      Confidence: {msg.confidence}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message-row bot">
                <div className="bubble bot loading">
                  <Loader2 className="spinner" size={18} />
                  Thinking...
                </div>
              </div>
            )}
            <div ref={scrollRef} />
          </div>

          {/* Input */}
          <form className="input-area" onSubmit={handleSend}>
            <input 
              type="text"
              placeholder="Ask about office policy..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button type="submit" disabled={!input.trim() || isLoading}>
              <Send size={20} />
            </button>
          </form>
        </div>
      )}

      {/* Floating Toggle Button */}
      <button className={`chat-toggle ${isOpen ? 'active' : ''}`} onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? <X size={28} /> : <MessageCircle size={28} />}
      </button>
    </div>
  );
};

export default ChatPopup;