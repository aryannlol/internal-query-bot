import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';
import { FileText, RefreshCw, Search, Loader2, AlertCircle } from 'lucide-react';
import './AdminPanel.css';

const AdminPanel = () => {
  const [docs, setDocs] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [content, setContent] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);

  useEffect(() => {
    fetchDocs();
  }, []);

  const fetchDocs = async () => {
    try {
      const res = await fetch('http://localhost:8000/list-docs');
      const data = await res.json();
      setDocs(data.files || []);
    } catch (err) {
      console.error("Failed to load file list");
    }
  };



  
  const handleFileClick = async (filename) => {
    setIsLoading(true);
    setSelectedDoc(filename);
    try {
      // ✅ Matches your @app.get("/get-doc/{filename}")
      const res = await fetch(`http://localhost:8000/get-doc/${filename}`);
      const data = await res.json();
      setContent(data.content || "");
      setSearchTerm(""); 
    } catch (err) {
      setContent("Error: Could not retrieve file content.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      await fetch('http://localhost:8000/rebuild-index', { method: 'POST' });
      alert("AI Brain Synced Successfully!");
      fetchDocs();
    } catch (e) {
      alert("Sync Failed. Is the backend running?");
    } finally {
      setIsSyncing(false);
    }
  };

  const getHighlightedContent = () => {
    if (!searchTerm) return content;
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return content.replace(regex, '<mark>$1</mark>'); 
  };

  return (
    <div className="admin-layout">
      {/* Sidebar */}
      <aside className="admin-sidebar">
        <div className="sidebar-header">
          <h2>Admin Console</h2>
          <button 
            className={`sync-btn ${isSyncing ? 'spinning' : ''}`} 
            onClick={handleSync}
            disabled={isSyncing}
          >
            <RefreshCw size={16} />
            {isSyncing ? 'Syncing...' : 'Sync AI Brain'}
          </button>
        </div>
        
        <div className="file-list">
          {docs.map(file => (
            <div 
              key={file} 
              className={`file-item ${selectedDoc === file ? 'active' : ''}`}
              onClick={() => handleFileClick(file)}
            >
              <FileText size={18} />
              <span>{file}</span>
            </div>
          ))}
        </div>
      </aside>

      {/* Main Content Viewer */}
      <main className="admin-main">
        {selectedDoc ? (
          <>
            <div className="toolbar">
              <div className="search-wrapper">
                <Search size={18} className="search-icon" />
                <input 
                  type="text" 
                  placeholder={`Search in ${selectedDoc}...`} 
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <span className="file-label">Viewing: <strong>{selectedDoc}</strong></span>
            </div>

            <div className="content-area">
              {isLoading ? (
                <div className="status-msg"><Loader2 className="animate-spin" /> Loading...</div>
              ) : (
                <div className="markdown-body">
                  <ReactMarkdown rehypePlugins={[rehypeRaw]}>
                    {getHighlightedContent()}
                  </ReactMarkdown>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="empty-state">
            <AlertCircle size={48} />
            <p>Select a policy document from the sidebar to begin.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default AdminPanel;