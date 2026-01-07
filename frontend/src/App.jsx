import React, { useState } from 'react';
import ChatPopup from './ChatPopup';
import AdminDashboard from './AdminDashboard';

function App() {
  const [view, setView] = useState('user'); // 'user' or 'admin'

  return (
    <div className="min-h-screen">
      {/* Navigation Bar */}
      <nav style={{ 
        background: '#1e40af', 
        padding: '10px 20px', 
        color: 'white', 
        display: 'flex', 
        gap: '20px',
        position: 'relative',
        zIndex: 1000 
      }}>
        <button 
          onClick={() => setView('user')} 
          style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontWeight: view === 'user' ? 'bold' : 'normal', borderBottom: view === 'user' ? '2px solid white' : 'none' }}
        >
          Portal Home
        </button>
        <button 
          onClick={() => setView('admin')} 
          style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontWeight: view === 'admin' ? 'bold' : 'normal', borderBottom: view === 'admin' ? '2px solid white' : 'none' }}
        >
          Admin Dashboard
        </button>
      </nav>

      {/* Main Content Area */}
      <main>
        {view === 'user' ? (
          <div style={{ padding: '40px' }}>
            <h1 style={{ color: '#0f172a', fontSize: '2rem', fontWeight: 'bold' }}>Internal Portal</h1>
            <p style={{ color: '#475569', marginTop: '10px' }}>The query assistant is available in the bottom right corner.</p>
          </div>
        ) : (
          <AdminDashboard />
        )}
      </main>

      {/* ✅ THE FIX: ChatPopup is OUTSIDE the ternary. 
        It stays mounted even when you switch to Admin, 
        preserving your chat history! 
      */}
      <ChatPopup />
    </div>
  );
}

export default App;