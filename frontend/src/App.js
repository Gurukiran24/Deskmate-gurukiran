import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [userName, setUserName] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;
    
    setLoading(true);
    const userMsg = message;
    setMessage('');
    
    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, user_name: userName })
      });
      const data = await response.json();
      
      setChatHistory(prev => [...prev, {
        user: userMsg,
        response: data.response,
        trace: data.execution_trace,
        tool: data.tool_used
      }]);
    } catch (err) {
      setChatHistory(prev => [...prev, {
        user: userMsg,
        response: 'Error: Could not connect to server',
        trace: [],
        tool: null
      }]);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>IT Helpdesk Chat</h1>
      <input 
        type="text" 
        placeholder="Your name" 
        value={userName} 
        onChange={e => setUserName(e.target.value)} 
      />
      <div className="chat-area">
        {chatHistory.map((chat, i) => (
          <div key={i} className="chat-entry">
            <strong>You:</strong> {chat.user}
            <br/>
            <strong>Bot:</strong> {chat.response}
            {chat.tool && <><br/><em>Tool used: {chat.tool}</em></>}
            <div className="trace">
              <details>
                <summary>Execution Trace</summary>
                <ul>{chat.trace.map((t, j) => <li key={j}>{t}</li>)}</ul>
              </details>
            </div>
          </div>
        ))}
      </div>
      <input 
        type="text" 
        placeholder="Type your message..." 
        value={message} 
        onChange={e => setMessage(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && sendMessage()}
      />
      <button onClick={sendMessage} disabled={loading}>Send</button>
    </div>
  );
}

export default App;