import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { adminAPI, healthAPI } from '../utils/api';
import {
  LogOut,
  ShieldCheck,
  Upload,
  FileText,
  Trash2,
  RefreshCw,
  BarChart3,
  CheckCircle,
  AlertCircle,
  Loader,
  User,
  Database,
  File,
} from 'lucide-react';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState({ total_chunks: 0, total_documents: 0 });
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [statsResponse, docsResponse] = await Promise.all([
        healthAPI.check(),
        adminAPI.listDocuments()
      ]);
      
      setStats({
        total_chunks: statsResponse.data.chunks_in_db || 0,
        total_documents: docsResponse.data.documents?.length || 0
      });
      setDocuments(docsResponse.data.documents || []);
    } catch (error) {
      console.error('Error fetching data:', error);
      setMessage({
        type: 'error',
        text: 'Failed to load data. Please refresh.',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      const validTypes = ['text/plain', 'application/pdf'];
      const validExtensions = ['.txt', '.pdf'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (validTypes.includes(file.type) || validExtensions.includes(fileExtension)) {
        setSelectedFile(file);
        setMessage(null);
      } else {
        setMessage({
          type: 'error',
          text: 'Please select a .txt or .pdf file',
        });
      }
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setMessage({
        type: 'error',
        text: 'Please select a file first',
      });
      return;
    }

    setUploadLoading(true);
    setMessage(null);

    try {
      const response = await adminAPI.ingestFile(selectedFile);
      setMessage({
        type: 'success',
        text: `Successfully uploaded! ${response.data.chunks_added} chunks added.`,
      });
      setSelectedFile(null);
      document.getElementById('file-input').value = '';
      
      // Refresh data
      await fetchData();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Failed to upload file',
      });
    } finally {
      setUploadLoading(false);
    }
  };

  const handleDeleteDocument = async (docId) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      await adminAPI.deleteDocument(docId);
      setMessage({
        type: 'success',
        text: 'Document deleted successfully',
      });
      await fetchData();
    } catch (error) {
      setMessage({
        type: 'error',
        text: 'Failed to delete document',
      });
    }
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <ShieldCheck size={28} />
            <div>
              <h1 className="header-title">CampusOps AI</h1>
              <p className="header-subtitle">Administrator Portal</p>
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
      <main className="admin-main">
        <div className="admin-container">
          
          {/* Stats Section */}
          <section className="stats-section">
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
                  <Database size={28} style={{ color: 'white' }} />
                </div>
                <div className="stat-content">
                  <p className="stat-label">Total Chunks</p>
                  <p className="stat-value">
                    {loading ? (
                      <Loader size={24} className="spin" />
                    ) : (
                      stats.total_chunks
                    )}
                  </p>
                </div>
                <button
                  className="stat-refresh"
                  onClick={fetchData}
                  disabled={loading}
                  title="Refresh"
                >
                  <RefreshCw size={16} className={loading ? 'spin' : ''} />
                </button>
              </div>

              <div className="stat-card">
                <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' }}>
                  <File size={28} style={{ color: 'white' }} />
                </div>
                <div className="stat-content">
                  <p className="stat-label">Documents</p>
                  <p className="stat-value">{stats.total_documents}</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' }}>
                  <CheckCircle size={28} style={{ color: 'white' }} />
                </div>
                <div className="stat-content">
                  <p className="stat-label">Status</p>
                  <p className="stat-value">
                    <span className="badge badge-success">Active</span>
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Upload Section */}
          <section className="upload-section">
            <h2 className="section-title">
              <Upload size={24} />
              Upload Documents
            </h2>
            <div className="upload-card">
              <div className="upload-area">
                <Upload size={48} className="upload-icon" />
                <h3 className="upload-title">Upload Policy Documents</h3>
                <p className="upload-description">
                  Upload TXT or PDF files containing campus policies
                </p>

                <div className="upload-actions">
                  <input
                    id="file-input"
                    type="file"
                    accept=".txt,.pdf"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                  />
                  <label htmlFor="file-input" className="btn btn-outline">
                    <FileText size={18} />
                    <span>Choose File</span>
                  </label>
                  {selectedFile && (
                    <button
                      onClick={handleFileUpload}
                      className="btn btn-primary"
                      disabled={uploadLoading}
                    >
                      {uploadLoading ? (
                        <>
                          <Loader size={18} className="spin" />
                          <span>Uploading...</span>
                        </>
                      ) : (
                        <>
                          <Upload size={18} />
                          <span>Upload File</span>
                        </>
                      )}
                    </button>
                  )}
                </div>

                {selectedFile && (
                  <div className="selected-file">
                    <FileText size={16} />
                    <span>{selectedFile.name}</span>
                    <span className="file-size">
                      ({(selectedFile.size / 1024).toFixed(2)} KB)
                    </span>
                  </div>
                )}

                {message && (
                  <div className={`upload-message ${message.type} fade-in`}>
                    {message.type === 'success' ? (
                      <CheckCircle size={18} />
                    ) : (
                      <AlertCircle size={18} />
                    )}
                    <span>{message.text}</span>
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Documents List */}
          <section className="documents-section">
            <h2 className="section-title">
              <FileText size={24} />
              Uploaded Documents ({documents.length})
            </h2>
            
            {documents.length === 0 ? (
              <div className="empty-state">
                <FileText size={64} />
                <h3>No Documents Yet</h3>
                <p>Upload your first policy document to get started</p>
              </div>
            ) : (
              <div className="documents-list">
                {documents.map((doc) => (
                  <div key={doc.id} className="document-card fade-in">
                    <div className="document-icon">
                      <FileText size={24} />
                    </div>
                    <div className="document-info">
                      <h3 className="document-name">{doc.name}</h3>
                      <div className="document-meta">
                        <span className="badge badge-primary">{doc.type}</span>
                        <span className="document-detail">
                          <strong>{doc.chunks}</strong> chunks
                        </span>
                        <span className="document-detail">
                          {new Date(doc.lastModified).toLocaleString()}
                        </span>
                      </div>
                    </div>
                    <div className="document-actions">
                      <button
                        className="btn-icon btn-icon-danger"
                        title="Delete document"
                        onClick={() => handleDeleteDocument(doc.id)}
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;
