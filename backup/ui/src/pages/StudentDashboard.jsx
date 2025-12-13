import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { queryAPI } from '../utils/api';
import { 
  Send, 
  LogOut, 
  BookOpen, 
  Loader, 
  User,
  Bot,
  AlertCircle,
  FileText
} from 'lucide-react';
import './StudentDashboard.css';

const StudentDashboard = () => {
  const { user, logout } = useAuth();
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Hello! I\'m your Campus Policy Assistant. Ask me anything about attendance, exams, placements, or any campus policies.',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      const response = await queryAPI.askQuestion(inputValue);
      const { answer, sources } = response.data;

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: answer,
        sources: sources || [],
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: 'Sorry, I encountered an error processing your question. Please try again.',
        error: true,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    'What is the minimum attendance requirement?',
    'What are the eligibility criteria for placements?',
    'Tell me about the exam policies',
    'What are the library rules?',
  ];

  const handleSuggestionClick = (question) => {
    setInputValue(question);
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <BookOpen size={24} />
            <div>
              <h1 className="header-title">CampusOps AI</h1>
              <p className="header-subtitle">Student Portal</p>
            </div>
          </div>
          <div className="header-right">
            <div className="user-info">
              <User size={18} />
              <span>{user?.username}</span>
            </div>
            <button onClick={logout} className="btn btn-outline">
              <LogOut size={18} />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="chat-container">
          <div className="messages-area">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.type} fade-in`}
              >
                <div className="message-avatar">
                  {message.type === 'user' ? (
                    <User size={20} />
                  ) : (
                    <Bot size={20} />
                  )}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">
                      {message.type === 'user' ? 'You' : 'Campus Assistant'}
                    </span>
                    <span className="message-time">
                      {message.timestamp.toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </span>
                  </div>
                  <div className={`message-text ${message.error ? 'error' : ''}`}>
                    {message.error && <AlertCircle size={16} />}
                    {message.text}
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <div className="sources-header">
                        <FileText size={14} />
                        <span>Sources ({message.sources.length})</span>
                      </div>
                      <div className="sources-list">
                        {message.sources.map((source, idx) => (
                          <div key={idx} className="source-item">
                            <span className="source-number">{idx + 1}</span>
                            <span className="source-text">{source}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message bot fade-in">
                <div className="message-avatar">
                  <Bot size={20} />
                </div>
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

          {/* Suggested Questions */}
          {messages.length === 1 && (
            <div className="suggestions fade-in">
              <p className="suggestions-title">Try asking:</p>
              <div className="suggestions-grid">
                {suggestedQuestions.map((question, idx) => (
                  <button
                    key={idx}
                    className="suggestion-chip"
                    onClick={() => handleSuggestionClick(question)}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="input-area">
            <form onSubmit={handleSubmit} className="input-form">
              <input
                type="text"
                className="input message-input"
                placeholder="Ask me about campus policies..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                disabled={loading}
              />
              <button
                type="submit"
                className="btn btn-primary send-button"
                disabled={!inputValue.trim() || loading}
              >
                {loading ? (
                  <Loader size={20} className="spin" />
                ) : (
                  <Send size={20} />
                )}
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
};

export default StudentDashboard;

