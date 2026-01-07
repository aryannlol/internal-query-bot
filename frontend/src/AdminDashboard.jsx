import React, { useState, useEffect, useCallback } from 'react';
import { Upload, Trash2, FileText, Eye, X, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [docs, setDocs] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedContent, setSelectedContent] = useState(null);
  const [viewingFileName, setViewingFileName] = useState("");
  const [isLoadingContent, setIsLoadingContent] = useState(false);

  // --- Resizing Logic ---
  const [previewWidth, setPreviewWidth] = useState(500); // Initial width in pixels
  const [isResizing, setIsResizing] = useState(false);

  const startResizing = useCallback(() => {
    setIsResizing(true);
  }, []);

  const stopResizing = useCallback(() => {
    setIsResizing(false);
  }, []);

  const resize = useCallback((e) => {
    if (isResizing) {
      const newWidth = window.innerWidth - e.clientX;
      if (newWidth > 300 && newWidth < 900) { // Limits: min 300px, max 900px
        setPreviewWidth(newWidth);
      }
    }
  }, [isResizing]);

  useEffect(() => {
    window.addEventListener('mousemove', resize);
    window.addEventListener('mouseup', stopResizing);
    return () => {
      window.removeEventListener('mousemove', resize);
      window.removeEventListener('mouseup', stopResizing);
    };
  }, [resize, stopResizing]);
  // ----------------------

  const fetchDocs = async () => {
    try {
      const res = await fetch('http://localhost:8000/list-docs');
      const data = await res.json();
      setDocs(data.files || data);
    } catch (e) { console.error("Failed to fetch"); }
  };

  useEffect(() => { fetchDocs(); }, []);


  const handleDelete = async (filename) => {
  const ok = window.confirm(`Delete ${filename}? This will remove it from index too.`);
  if (!ok) return;

  try {
    const res = await fetch(
      `http://localhost:8000/admin/documents/${encodeURIComponent(filename)}`,
      { method: "DELETE" }
    );

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Delete failed");
    }

    // ✅ Optimistic UI update
    setDocs((prev) => prev.filter((f) => f !== filename));

    // If currently previewing the deleted file → close preview
    if (viewingFileName === filename) {
      setViewingFileName("");
      setSelectedContent(null);
    }
  } catch (e) {
    alert(e.message);
  }
};
  const handleUpload = async (e) => {
  const files = Array.from(e.target.files);
  if (!files.length) return;

  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  setIsUploading(true);

  try {
    const res = await fetch(
      "http://localhost:8000/admin/upload-incremental",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Upload failed");
    }

    // ✅ Refresh doc list (or optimistic merge)
    await fetchDocs();

    alert(data.message);
  } catch (e) {
    alert(e.message);
  } finally {
    setIsUploading(false);
    e.target.value = ""; // reset input
  }
};



  const handleView = async (filename) => {
    setIsLoadingContent(true);
    setViewingFileName(filename);
    try {
      const res = await fetch(`http://localhost:8000/get-doc/${filename}`);
      const data = await res.json();
      setSelectedContent(data.content);
    } catch (e) { alert("Error loading"); }
    finally { setIsLoadingContent(false); }
  };

  return (
    <div className={`admin-wrapper ${isResizing ? 'resizing' : ''}`}>
      {/* Left Side */}
      <div className="admin-panel" style={{ flex: 1 }}>
        <div className="admin-header">
          <h2>Knowledge Base Management</h2>
        </div>
        
        <div className="upload-section">
          <label className={`upload-label ${isUploading ? "disabled" : ""}`}>
            <div className="file-icon-bg"><Upload size={24} /></div>
            <span>{isUploading ? 'Processing...' : 'Upload Office Docs (PDF/TXT/MD)'}</span>
            <input type="file" multiple hidden accept='.md' onChange={handleUpload}/>
          </label>
        </div>
        <div className="doc-list">
          <div className="table-wrapper">
          <table>
            <thead>
              <tr><th>File Name</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {docs.map((file) => (
                <tr key={file} className={viewingFileName === file ? 'selected-row' : ''}>
                  <td><div className="file-cell"><div className="file-icon-bg"><FileText size={16}/></div>{file}</div></td>
                  <td>
                    <div className="action-group">
                      <button onClick={() => handleView(file)} className="view-btn"><Eye size={18}/></button>
                      <button className="delete-btn" onClick={()=>handleDelete(file)}><Trash2 size={18}/></button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        </div>
        
      </div>

      {/* The Cursor/Resizer Bar */}
      {viewingFileName && (
        <div className="resizer" onMouseDown={startResizing} />
      )}

      {/* Right Side: Resizable Preview */}
      {viewingFileName && (
        <div className="side-preview" style={{ width: `${previewWidth}px`, flex: 'none' }}>
<div className="preview-header">
  <div className="file-cell">
    <div className="file-icon-bg"><FileText size={18} /></div>
    <h3>{viewingFileName}</h3> {/* The CSS above targets this h3 */}
  </div>
  <button className="close-btn" onClick={() => setViewingFileName("")}>
    <X size={20} />
  </button>
</div>
          <div className="preview-content">
            {isLoadingContent ? <Loader2 className="spinner" /> : (
              <div className="markdown-render">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{selectedContent}</ReactMarkdown>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;