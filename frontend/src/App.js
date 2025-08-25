import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Main App Component
function App() {
  const [currentView, setCurrentView] = useState('home');
  const [assessments, setAssessments] = useState([]);
  const [selectedAssessment, setSelectedAssessment] = useState(null);

  useEffect(() => {
    fetchAssessments();
  }, []);

  const fetchAssessments = async () => {
    try {
      const response = await axios.get(`${API}/assessments`);
      setAssessments(response.data);
    } catch (error) {
      console.error('Error fetching assessments:', error);
    }
  };

  const handleDeleteAssessment = async (assessmentId, assessmentName) => {
    if (window.confirm(`Are you sure you want to delete "${assessmentName}"? This action cannot be undone.`)) {
      try {
        await axios.delete(`${API}/assessments/${assessmentId}`);
        fetchAssessments(); // Refresh the assessment list
        
        // If we're currently viewing the deleted assessment, go back to home
        if (selectedAssessment && selectedAssessment.id === assessmentId) {
          setSelectedAssessment(null);
          setCurrentView('home');
        }
      } catch (error) {
        console.error('Error deleting assessment:', error);
        alert('Failed to delete assessment. Please try again.');
      }
    }
  };

  const renderView = () => {
    switch (currentView) {
      case 'create':
        return <CreateAssessment onBack={() => setCurrentView('home')} onCreated={fetchAssessments} />;
      case 'assessment':
        return <AssessmentDetail assessment={selectedAssessment} onBack={() => setCurrentView('home')} />;
      default:
        return (
          <Home 
            assessments={assessments}
            onCreateNew={() => setCurrentView('create')}
            onViewAssessment={(assessment) => {
              setSelectedAssessment(assessment);
              setCurrentView('assessment');
            }}
            onDeleteAssessment={handleDeleteAssessment}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {renderView()}
    </div>
  );
}

// Home Component - Assessment Dashboard
const Home = ({ assessments, onCreateNew, onViewAssessment, onDeleteAssessment }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'analyzing': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getScoreColor = (percentage) => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Azure Well-Architected Review</h1>
        <p className="text-lg text-gray-600">Analyze your Azure architecture against the 5 pillars of excellence</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-blue-600">{assessments.length}</div>
          <div className="text-sm text-gray-600">Total Reviews</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-green-600">{assessments.filter(a => a.status === 'completed').length}</div>
          <div className="text-sm text-gray-600">Completed</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-yellow-600">{assessments.filter(a => a.status === 'analyzing').length}</div>
          <div className="text-sm text-gray-600">In Progress</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-gray-600">
            {assessments.length > 0 ? 
              Math.round(assessments.filter(a => a.overall_percentage).reduce((sum, a) => sum + a.overall_percentage, 0) / 
              assessments.filter(a => a.overall_percentage).length) + '%' : 'N/A'}
          </div>
          <div className="text-sm text-gray-600">Avg Score</div>
        </div>
      </div>

      {/* Create New Button */}
      <div className="mb-6">
        <button
          onClick={onCreateNew}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 flex items-center space-x-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <span>New Well-Architected Review</span>
        </button>
      </div>

      {/* Assessments List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900">Recent Reviews</h2>
        </div>

        {assessments.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <svg className="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p>No reviews yet. Create your first Azure Well-Architected Review.</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {assessments.map((assessment) => (
              <div key={assessment.id} className="p-6 hover:bg-gray-50 transition duration-150">
                <div className="flex items-center justify-between">
                  <div className="flex-1 cursor-pointer" onClick={() => onViewAssessment(assessment)}>
                    <div className="flex items-center space-x-3">
                      <h3 className="text-lg font-medium text-gray-900">{assessment.name}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(assessment.status)}`}>
                        {assessment.status.charAt(0).toUpperCase() + assessment.status.slice(1)}
                      </span>
                    </div>
                    {assessment.description && (
                      <p className="mt-1 text-sm text-gray-600">{assessment.description}</p>
                    )}
                    <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                      <span>📄 {assessment.document_count} documents</span>
                      <span>📅 {new Date(assessment.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    {assessment.status === 'analyzing' && (
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full transition-all duration-500" 
                            style={{ width: `${assessment.progress}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-blue-600">{assessment.progress}%</span>
                      </div>
                    )}
                    {assessment.overall_percentage && (
                      <div className="text-right">
                        <div className={`text-2xl font-bold ${getScoreColor(assessment.overall_percentage)}`}>
                          {assessment.overall_percentage}%
                        </div>
                        <div className="text-xs text-gray-500">Overall Score</div>
                      </div>
                    )}
                    
                    {/* Delete Button */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation(); // Prevent triggering the row click
                        onDeleteAssessment(assessment.id, assessment.name);
                      }}
                      className="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-full transition duration-150"
                      title="Delete Assessment"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} 
                              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1-1H8a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                    
                    {/* View Arrow */}
                    <div className="cursor-pointer" onClick={() => onViewAssessment(assessment)}>
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

// Create Assessment Component
const CreateAssessment = ({ onBack, onCreated }) => {
  const [formData, setFormData] = useState({ name: '', description: '' });
  const [isCreating, setIsCreating] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsCreating(true);

    try {
      const response = await axios.post(`${API}/assessments`, formData);
      onCreated();
      onBack();
    } catch (error) {
      console.error('Error creating assessment:', error);
    } finally {
      setIsCreating(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <button onClick={onBack} className="mb-6 text-blue-600 hover:text-blue-700 flex items-center space-x-2">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        <span>Back to Dashboard</span>
      </button>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Create New Assessment</h1>
        <p className="text-gray-600 mb-8">Start a new Azure Well-Architected Framework review for your architecture</p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
              Assessment Name *
            </label>
            <input
              type="text"
              id="name"
              required
              value={formData.name}
              onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., E-commerce Platform Review"
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description (Optional)
            </label>
            <textarea
              id="description"
              rows={4}
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Brief description of your architecture and business requirements..."
            />
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="text-sm font-medium text-blue-900 mb-2">What's Next?</h3>
            <p className="text-sm text-blue-700">
              After creating the assessment, you'll be able to upload architecture documents, diagrams, and other relevant files. 
              Our AI agents will analyze your architecture against all 5 pillars of the Well-Architected Framework.
            </p>
          </div>

          <div className="flex justify-end space-x-4 pt-6">
            <button
              type="button"
              onClick={onBack}
              className="px-6 py-3 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition duration-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isCreating}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition duration-200"
            >
              {isCreating ? 'Creating...' : 'Create Assessment'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Assessment Detail Component
const AssessmentDetail = ({ assessment, onBack }) => {
  const [currentTab, setCurrentTab] = useState('upload');
  const [assessmentData, setAssessmentData] = useState(assessment);
  const [files, setFiles] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [scorecard, setScorecard] = useState(null);

  useEffect(() => {
    fetchAssessmentDetails();
    if (assessment.status === 'completed') {
      fetchScorecard();
    }
  }, []);

  const fetchAssessmentDetails = async () => {
    try {
      const response = await axios.get(`${API}/assessments/${assessment.id}`);
      setAssessmentData(response.data);
    } catch (error) {
      console.error('Error fetching assessment details:', error);
    }
  };

  const fetchScorecard = async () => {
    try {
      const response = await axios.get(`${API}/assessments/${assessment.id}/scorecard`);
      setScorecard(response.data);
    } catch (error) {
      console.error('Error fetching scorecard:', error);
    }
  };

  const handleFileUpload = async (e) => {
    const selectedFiles = Array.from(e.target.files);
    setIsUploading(true);

    // Check if this is the first upload (no existing documents)
    const isFirstUpload = !assessmentData.documents || assessmentData.documents.length === 0;

    try {
      for (const file of selectedFiles) {
        const formData = new FormData();
        formData.append('file', file);
        await axios.post(`${API}/assessments/${assessment.id}/documents`, formData);
      }
      
      // Refresh assessment data
      await fetchAssessmentDetails();
      
      // Only auto-switch to artifacts tab on first upload, not subsequent uploads
      if (isFirstUpload) {
        setTimeout(() => {
          setCurrentTab('artifacts');
        }, 500);
      }
    } catch (error) {
      console.error('Error uploading files:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleStartAnalysis = async () => {
    try {
      await axios.post(`${API}/assessments/${assessment.id}/analyze`);
      fetchAssessmentDetails();
      setCurrentTab('progress');
    } catch (error) {
      console.error('Error starting analysis:', error);
    }
  };

  useEffect(() => {
    let interval;
    if (assessmentData?.status === 'analyzing') {
      interval = setInterval(() => {
        fetchAssessmentDetails();
      }, 2000);
    }
    
    if (assessmentData?.status === 'completed' && !scorecard) {
      fetchScorecard();
      setCurrentTab('results');
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [assessmentData?.status]);

  return (
    <div className="container mx-auto px-4 py-8">
      <button onClick={onBack} className="mb-6 text-blue-600 hover:text-blue-700 flex items-center space-x-2">
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        <span>Back to Dashboard</span>
      </button>

      <div className="bg-white rounded-lg shadow-lg">
        {/* Header */}
        <div className="px-8 py-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{assessmentData?.name}</h1>
              {assessmentData?.description && (
                <p className="mt-1 text-gray-600">{assessmentData.description}</p>
              )}
            </div>
            <div className="text-right">
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                assessmentData?.status === 'completed' ? 'bg-green-100 text-green-800' :
                assessmentData?.status === 'analyzing' ? 'bg-blue-100 text-blue-800' :
                'bg-yellow-100 text-yellow-800'
              }`}>
                {assessmentData?.status?.charAt(0).toUpperCase() + assessmentData?.status?.slice(1)}
              </span>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="px-8 py-4 border-b border-gray-200">
          <nav className="flex space-x-8">
            {['upload', 'artifacts', 'progress', 'results'].map((tab) => (
              <button
                key={tab}
                onClick={() => setCurrentTab(tab)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  currentTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab === 'upload' ? '📄 Upload Documents' :
                 tab === 'artifacts' ? '🔍 Uploaded Artifact Findings' :
                 tab === 'progress' ? '⚡ Analysis Progress' : 
                 '📊 Results & Scorecard'}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-8">
          {currentTab === 'upload' && (
            <UploadTab 
              assessment={assessmentData}
              onFileUpload={handleFileUpload}
              onStartAnalysis={handleStartAnalysis}
              isUploading={isUploading}
            />
          )}
          {currentTab === 'artifacts' && (
            <ArtifactFindingsTab assessment={assessmentData} />
          )}
          {currentTab === 'progress' && (
            <ProgressTab assessment={assessmentData} />
          )}
          {currentTab === 'results' && (
            <ResultsTab scorecard={scorecard} />
          )}
        </div>
      </div>
    </div>
  );
};

// Upload Tab Component
const UploadTab = ({ assessment, onFileUpload, onStartAnalysis, isUploading }) => {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Architecture Documents, Images & CSV Files</h2>
        <p className="text-gray-600 mb-6">
          Upload your architecture diagrams, documentation, and CSV support case files. Our AI agents will analyze these against the 5 pillars.
        </p>

        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <div className="mt-4">
            <label htmlFor="file-upload" className="cursor-pointer">
              <span className="mt-2 block text-sm font-medium text-gray-900">
                {isUploading ? 'Uploading...' : 'Drop files here or click to upload'}
              </span>
              <input
                id="file-upload"
                name="file-upload"
                type="file"
                multiple
                accept=".pdf,.doc,.docx,.txt,.md,.png,.jpg,.jpeg,.svg,.csv"
                className="sr-only"
                onChange={onFileUpload}
                disabled={isUploading}
              />
            </label>
            <p className="mt-2 text-xs text-gray-500">
              📄 Documents: PDF, DOC, TXT | 🖼️ Images: PNG, JPG, SVG | 📊 CSV: Support Case Data
            </p>
          </div>
        </div>
      </div>

      {/* Uploaded Files */}
      {assessment?.documents?.length > 0 && (
        <div>
          <h3 className="text-lg font-medium text-gray-900 mb-4">Uploaded Documents ({assessment.documents.length})</h3>
          <div className="space-y-2">
            {assessment.documents.map((doc, index) => {
              const isImage = doc.content_type?.startsWith('image/') || doc.filename?.match(/\.(png|jpg|jpeg|gif|svg)$/i);
              const isCSV = doc.content_type === 'text/csv' || doc.filename?.toLowerCase().endsWith('.csv');
              const isText = doc.content_type === 'text/plain' || doc.filename?.match(/\.(txt|md)$/i);
              
              return (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    {isImage ? (
                      <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    ) : isCSV ? (
                      <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    )}
                    <span className="text-sm text-gray-900">{doc.filename}</span>
                    {isImage && (
                      <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">🖼️ Architecture Diagram</span>
                    )}
                    {isCSV && (
                      <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">📊 Case Analysis Data</span>
                    )}
                    {isText && (
                      <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">📄 Architecture Doc</span>
                    )}
                  </div>
                  <span className="text-xs text-gray-500">{doc.content_type}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Start Analysis Button */}
      {assessment?.documents?.length > 0 && assessment?.status === 'pending' && (
        <div className="flex justify-end">
          <button
            onClick={onStartAnalysis}
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 flex items-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <span>Start Enhanced Well-Architected Analysis</span>
          </button>
        </div>
      )}
    </div>
  );
};

// Progress Tab Component
const ProgressTab = ({ assessment }) => {
  const pillars = [
    { name: 'Reliability', icon: '🛡️', description: 'Resiliency, availability, recovery' },
    { name: 'Security', icon: '🔒', description: 'Data protection, threat detection' },
    { name: 'Cost Optimization', icon: '💰', description: 'Cost modeling, budgets, reduce waste' },
    { name: 'Operational Excellence', icon: '⚙️', description: 'Monitoring, DevOps practices' },
    { name: 'Performance Efficiency', icon: '⚡', description: 'Scalability, load testing' }
  ];

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Analysis Progress</h2>
        <p className="text-gray-600 mb-6">
          Our specialized AI agents are analyzing your architecture against each pillar of the Well-Architected Framework.
        </p>
      </div>

      {/* Overall Progress */}
      <div className="bg-gray-50 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-gray-900">Overall Progress</h3>
          <span className="text-2xl font-bold text-blue-600">{assessment?.progress || 0}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div 
            className="bg-blue-600 h-3 rounded-full transition-all duration-1000" 
            style={{ width: `${assessment?.progress || 0}%` }}
          ></div>
        </div>
      </div>

      {/* Pillar Progress */}
      <div>
        <h3 className="text-lg font-medium text-gray-900 mb-6">Pillar Analysis Status</h3>
        <div className="space-y-4">
          {pillars.map((pillar, index) => {
            // Fix: When progress is 100% OR status is completed, all pillars should be completed
            const isCompleted = assessment?.progress >= (index + 1) * 20 || 
                               assessment?.progress === 100 || 
                               assessment?.status === 'completed';
            const isAnalyzing = assessment?.progress > index * 20 && 
                               assessment?.progress < (index + 1) * 20 && 
                               assessment?.progress < 100 && 
                               assessment?.status !== 'completed';
            
            return (
              <div key={pillar.name} className={`border rounded-lg p-4 ${
                isCompleted ? 'border-green-200 bg-green-50' :
                isAnalyzing ? 'border-blue-200 bg-blue-50' :
                'border-gray-200 bg-white'
              }`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{pillar.icon}</span>
                    <div>
                      <h4 className="font-medium text-gray-900">{pillar.name}</h4>
                      <p className="text-sm text-gray-600">{pillar.description}</p>
                    </div>
                  </div>
                  <div>
                    {isCompleted ? (
                      <span className="flex items-center text-green-600">
                        <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        Complete
                      </span>
                    ) : isAnalyzing ? (
                      <span className="flex items-center text-blue-600">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                        Analyzing
                      </span>
                    ) : (
                      <span className="text-gray-400">Waiting</span>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {assessment?.status === 'completed' && (
        <div className="text-center">
          <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-lg">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            Analysis Complete! Check the Results tab for your scorecard.
          </div>
        </div>
      )}
    </div>
  );
};

// Results Tab Component
const ResultsTab = ({ scorecard }) => {
  if (!scorecard) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500">No results available yet. Complete the analysis first.</div>
      </div>
    );
  }

  const getScoreColor = (percentage) => {
    if (percentage >= 80) return 'text-green-600 bg-green-100';
    if (percentage >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getPriorityColor = (priority) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-8">
      {/* Overall Score */}
      <div className="text-center">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Well-Architected Scorecard</h2>
        <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full text-4xl font-bold ${getScoreColor(scorecard.overall_percentage)}`}>
          {scorecard.overall_percentage}%
        </div>
        <p className="mt-2 text-gray-600">Overall Architecture Score</p>
      </div>

      {/* Pillar Scores */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Pillar Breakdown</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {scorecard.pillar_scores && Array.isArray(scorecard.pillar_scores) && scorecard.pillar_scores.map((pillar) => (
            <div key={pillar.pillar_name} className="bg-white border border-gray-200 rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h4 className="font-medium text-gray-900">{pillar.pillar_name}</h4>
                <span className={`px-2 py-1 rounded text-sm font-medium ${getScoreColor(pillar.percentage)}`}>
                  {pillar.percentage}%
                </span>
              </div>
              
              <div className="space-y-2">
                {pillar.sub_categories && typeof pillar.sub_categories === 'object' && 
                 Object.entries(pillar.sub_categories).map(([category, scores]) => (
                  <div key={category} className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">{category}</span>
                    <span className="font-medium">{scores?.percentage || 0}%</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-6">Recommendations</h3>
        <div className="space-y-4">
          {scorecard.recommendations && Array.isArray(scorecard.recommendations) && scorecard.recommendations.map((rec, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-6">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <div className="flex items-center space-x-3 mb-2">
                    <h4 className="font-medium text-gray-900">{rec.title || 'Untitled Recommendation'}</h4>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(rec.priority || 'Medium')}`}>
                      {rec.priority || 'Medium'} Priority
                    </span>
                  </div>
                  <p className="text-sm text-gray-500">{rec.pillar || 'General'} • {rec.category || 'General'}</p>
                </div>
              </div>
              
              <p className="text-gray-700 mb-4">{rec.description || 'No description available'}</p>
              
              {rec.details && (
                <div className="mb-4 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
                  <span className="font-medium text-blue-900">Details:</span>
                  <p className="text-blue-800 mt-1 text-sm">{rec.details}</p>
                </div>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <span className="font-medium text-gray-900">Impact:</span>
                  <p className="text-gray-600 mt-1">{rec.impact || 'Not specified'}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-900">Effort:</span>
                  <p className="text-gray-600 mt-1">{rec.effort || 'Not specified'}</p>
                </div>
                <div>
                  <span className="font-medium text-gray-900">Azure Service:</span>
                  <div className="mt-1">
                    {rec.reference_url ? (
                      <a 
                        href={rec.reference_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-700 hover:underline font-medium"
                      >
                        {rec.azure_service || 'Azure Service'} →
                      </a>
                    ) : (
                      <span className="text-blue-600 font-medium">{rec.azure_service || 'Azure Service'}</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
          {(!scorecard.recommendations || !Array.isArray(scorecard.recommendations) || scorecard.recommendations.length === 0) && (
            <div className="text-center py-8 text-gray-500">
              No recommendations available yet.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Artifact Findings Tab Component
const ArtifactFindingsTab = ({ assessment }) => {
  const [artifactData, setArtifactData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('Assessment changed, processing artifact data:', assessment);
    processArtifactData();
  }, [assessment, assessment?.documents]);

  const processArtifactData = () => {
    if (!assessment || !assessment.documents) {
      console.log('No assessment or documents found');
      setArtifactData(null);
      setLoading(false);
      return;
    }

    const documents = assessment.documents || [];
    console.log('Processing documents:', documents);
    
    // Enhanced file type detection with mutually exclusive categories
    const csvDocuments = documents.filter(doc => {
      const filename = doc.filename?.toLowerCase() || '';
      const contentType = doc.content_type?.toLowerCase() || '';
      
      return (
        contentType === 'text/csv' || 
        contentType.includes('csv') ||
        filename.endsWith('.csv') ||
        (contentType === 'application/octet-stream' && filename.endsWith('.csv'))
      );
    });
    
    const imageDocuments = documents.filter(doc => {
      const filename = doc.filename?.toLowerCase() || '';
      const contentType = doc.content_type?.toLowerCase() || '';
      
      // Exclude files already categorized as CSV
      if (csvDocuments.includes(doc)) return false;
      
      return (
        contentType.startsWith('image/') ||
        filename.endsWith('.png') ||
        filename.endsWith('.jpg') ||
        filename.endsWith('.jpeg') ||
        filename.endsWith('.gif') ||
        filename.endsWith('.bmp') ||
        filename.endsWith('.svg') ||
        (contentType === 'application/octet-stream' && 
         (filename.endsWith('.png') || filename.endsWith('.jpg') || filename.endsWith('.jpeg')))
      );
    });
    
    const textDocuments = documents.filter(doc => {
      const filename = doc.filename?.toLowerCase() || '';
      const contentType = doc.content_type?.toLowerCase() || '';
      
      // Exclude files already categorized as CSV or images
      if (csvDocuments.includes(doc) || imageDocuments.includes(doc)) return false;
      
      return (
        contentType === 'text/plain' || 
        contentType.includes('text') ||
        filename.endsWith('.txt') || 
        filename.endsWith('.md') ||
        filename.endsWith('.doc') ||
        filename.endsWith('.docx') ||
        (contentType === 'application/octet-stream' && (filename.endsWith('.txt') || filename.endsWith('.md')))
      );
    });
    
    const otherDocuments = documents.filter(doc => 
      !textDocuments.includes(doc) && 
      !imageDocuments.includes(doc) && 
      !csvDocuments.includes(doc)
    );

    console.log('Categorized documents:', {
      total: documents.length,
      text: textDocuments.length,
      images: imageDocuments.length,
      csv: csvDocuments.length,
      other: otherDocuments.length
    });

    setArtifactData({
      totalDocuments: documents.length,
      textDocuments,
      imageDocuments,
      csvDocuments,
      otherDocuments,
      uploadTimestamp: assessment.created_at,
      lastModified: assessment.updated_at
    });
    
    setLoading(false);
  };

  const formatFileSize = (base64String) => {
    if (!base64String) return 'Unknown';
    const bytes = (base64String.length * 3) / 4;
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
  };

  const getDocumentIcon = (contentType, filename) => {
    const fname = filename?.toLowerCase() || '';
    const ctype = contentType?.toLowerCase() || '';
    
    // Images
    if (ctype.startsWith('image/') || fname.match(/\.(png|jpg|jpeg|gif|bmp|svg)$/)) return '🖼️';
    
    // CSV files
    if (ctype === 'text/csv' || ctype.includes('csv') || fname.endsWith('.csv')) return '📊';
    
    // Text files
    if (ctype === 'text/plain' || fname.endsWith('.txt') || fname.endsWith('.md')) return '📄';
    
    // Office documents
    if (fname.endsWith('.pdf')) return '📕';
    if (fname.endsWith('.doc') || fname.endsWith('.docx')) return '📘';
    
    return '📎';
  };

  const renderDocumentAnalysis = (doc) => {
    const icon = getDocumentIcon(doc.content_type, doc.filename);
    const size = formatFileSize(doc.file_base64);
    const filename = doc.filename?.toLowerCase() || '';
    const contentType = doc.content_type?.toLowerCase() || '';
    
    // Determine file type for correct context display
    const isCSV = contentType === 'text/csv' || contentType.includes('csv') || filename.endsWith('.csv');
    const isImage = contentType.startsWith('image/') || filename.match(/\.(png|jpg|jpeg|gif|bmp|svg)$/);
    const isText = !isCSV && !isImage && (contentType === 'text/plain' || contentType.includes('text') || filename.match(/\.(txt|md)$/));
    
    return (
      <div key={doc.document_id} className="border border-gray-200 rounded-lg p-4 bg-white">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{icon}</span>
            <div>
              <h4 className="font-medium text-gray-900">{doc.filename || 'Unnamed Document'}</h4>
              <p className="text-sm text-gray-500">{doc.content_type} • {size}</p>
            </div>
          </div>
          <div className="text-xs text-gray-400">
            Uploaded: {new Date(doc.upload_timestamp || Date.now()).toLocaleDateString()}
          </div>
        </div>
        
        {/* Document Content Preview Based on File Type */}
        {isImage && (
          <div className="mt-3">
            <p className="text-sm font-medium text-gray-700 mb-2">🔍 Image Analysis Context:</p>
            <div className="bg-blue-50 p-3 rounded border-l-4 border-blue-400">
              <p className="text-sm text-blue-800">
                This architecture diagram will be analyzed to identify Azure services, components, and architectural patterns. 
                The AI system will extract service relationships, data flows, and architectural decisions to enhance the Well-Architected review.
              </p>
              {assessment?.llm_mode === 'real' && (
                <div className="mt-2 p-2 bg-blue-100 rounded border border-blue-300">
                  <p className="text-xs font-medium text-blue-900">🤖 Real AI Analysis:</p>
                  <p className="text-xs text-blue-800 mt-1">
                    This image will be processed by advanced AI vision models to extract architectural components, 
                    identify Azure services, and provide specific insights for each Well-Architected pillar assessment.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
        
        {isCSV && (
          <div className="mt-3">
            <p className="text-sm font-medium text-gray-700 mb-2">📊 CSV Case Analysis Context:</p>
            <div className="bg-green-50 p-3 rounded border-l-4 border-green-400">
              <p className="text-sm text-green-800">
                This CSV file contains support case data that will be analyzed for patterns, trends, and Well-Architected Framework violations. 
                The reactive case analyzer will identify common issues and provide targeted recommendations based on historical incidents.
              </p>
            </div>
            
            {/* Display actual AI insights for CSV files */}
            {assessment?.llm_mode === 'real' && doc.ai_insights && (
              <div className="mt-2 p-3 bg-green-100 rounded border border-green-300">
                <p className="text-xs font-medium text-green-900">🤖 Real AI Case Analysis:</p>
                <div className="text-xs text-green-800 mt-2 space-y-1">
                  {doc.ai_insights.patterns && (
                    <div>
                      <span className="font-semibold">Common Patterns:</span> {doc.ai_insights.patterns}
                    </div>
                  )}
                  {doc.ai_insights.services && (
                    <div>
                      <span className="font-semibold">Problem Services:</span> {doc.ai_insights.services}
                    </div>
                  )}
                  {doc.ai_insights.violations && (
                    <div>
                      <span className="font-semibold">WA Framework Violations:</span> {doc.ai_insights.violations}
                    </div>
                  )}
                  {doc.ai_insights.risks && (
                    <div>
                      <span className="font-semibold">Risk Indicators:</span> {doc.ai_insights.risks}
                    </div>
                  )}
                  {doc.ai_insights.analysis && !doc.ai_insights.patterns && (
                    <div>{doc.ai_insights.analysis}</div>
                  )}
                </div>
              </div>
            )}
            
            {assessment?.llm_mode === 'real' && !doc.ai_insights && (
              <div className="mt-2 p-2 bg-yellow-100 rounded border border-yellow-300">
                <p className="text-xs text-yellow-800">
                  ⚠️ AI analysis not available - upload in Real LLM mode to get instant insights
                </p>
              </div>
            )}
          </div>
        )}
        
        {isText && (
          <div className="mt-3">
            <p className="text-sm font-medium text-gray-700 mb-2">📄 Architecture Document Context:</p>
            <div className="bg-purple-50 p-3 rounded border-l-4 border-purple-400">
              <p className="text-sm text-purple-800">
                This architecture document provides detailed context about your system design, components, and configurations. 
                The AI agents will analyze this content to understand your architecture and provide specific, contextual recommendations for each Well-Architected pillar.
              </p>
            </div>
            
            {/* Display actual AI insights for architecture documents */}
            {assessment?.llm_mode === 'real' && doc.ai_insights && (
              <div className="mt-2 p-3 bg-purple-100 rounded border border-purple-300">
                <p className="text-xs font-medium text-purple-900">🤖 Real AI Architecture Analysis:</p>
                <div className="text-xs text-purple-800 mt-2 space-y-1">
                  {doc.ai_insights.patterns && (
                    <div>
                      <span className="font-semibold">Architecture Patterns:</span> {doc.ai_insights.patterns}
                    </div>
                  )}
                  {doc.ai_insights.concerns && (
                    <div>
                      <span className="font-semibold">WA Framework Concerns:</span> {doc.ai_insights.concerns}
                    </div>
                  )}
                  {doc.ai_insights.components && (
                    <div>
                      <span className="font-semibold">Key Components:</span> {doc.ai_insights.components}
                    </div>
                  )}
                  {doc.ai_insights.recommendations && (
                    <div>
                      <span className="font-semibold">Recommendations:</span> {doc.ai_insights.recommendations}
                    </div>
                  )}
                  {doc.ai_insights.analysis && !doc.ai_insights.patterns && (
                    <div>{doc.ai_insights.analysis}</div>
                  )}
                </div>
              </div>
            )}
            
            {assessment?.llm_mode === 'real' && !doc.ai_insights && (
              <div className="mt-2 p-2 bg-yellow-100 rounded border border-yellow-300">
                <p className="text-xs text-yellow-800">
                  ⚠️ AI analysis not available - upload in Real LLM mode to get instant insights
                </p>
              </div>
            )}
            
            {/* Show a preview of text content */}
            {doc.file_base64 && (
              <div className="mt-3">
                <p className="text-xs font-medium text-gray-600 mb-1">Content Preview:</p>
                <div className="bg-gray-50 p-2 rounded text-xs text-gray-700 max-h-20 overflow-hidden">
                  {(() => {
                    try {
                      const decoded = atob(doc.file_base64);
                      return decoded.substring(0, 200) + (decoded.length > 200 ? '...' : '');
                    } catch (e) {
                      return 'Preview not available';
                    }
                  })()}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500">Loading artifact findings...</div>
      </div>
    );
  }

  if (!artifactData || artifactData.totalDocuments === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📂</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Artifacts Uploaded</h3>
        <p className="text-gray-500">Upload documents, images, or CSV files to see their analysis context here.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Summary Header */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">🔍 Uploaded Artifact Findings</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-blue-600">{artifactData.totalDocuments}</div>
            <div className="text-sm text-gray-600">Total Documents</div>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-green-600">{artifactData.textDocuments.length}</div>
            <div className="text-sm text-gray-600">Architecture Docs</div>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-purple-600">{artifactData.imageDocuments.length}</div>
            <div className="text-sm text-gray-600">Architecture Diagrams</div>
          </div>
          <div className="bg-white rounded-lg p-4 text-center">
            <div className="text-2xl font-bold text-orange-600">{artifactData.csvDocuments.length}</div>
            <div className="text-sm text-gray-600">Case Analysis CSVs</div>
          </div>
        </div>
      </div>

      {/* AI Context Information */}
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
        <div className="flex items-start">
          <div className="text-yellow-400 mr-3">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </div>
          <div>
            <h3 className="text-sm font-medium text-yellow-800">AI Analysis Context</h3>
            <p className="text-sm text-yellow-700 mt-1">
              These uploaded artifacts provide comprehensive context for the AI-powered Well-Architected review. 
              Architecture documents inform textual analysis, diagrams enable visual component recognition, 
              and CSV files provide historical case patterns for reactive analysis recommendations.
            </p>
          </div>
        </div>
      </div>

      {/* Document Categories */}
      {artifactData.textDocuments.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📄 Architecture Documents ({artifactData.textDocuments.length})</h3>
          <div className="space-y-4">
            {artifactData.textDocuments.map((doc, index) => (
              <div key={`text-${index}-${doc.document_id || doc.filename}`}>
                {renderDocumentAnalysis(doc)}
              </div>
            ))}
          </div>
        </div>
      )}

      {artifactData.imageDocuments.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">🖼️ Architecture Diagrams ({artifactData.imageDocuments.length})</h3>
          <div className="space-y-4">
            {artifactData.imageDocuments.map((doc, index) => (
              <div key={`image-${index}-${doc.document_id || doc.filename}`}>
                {renderDocumentAnalysis(doc)}
              </div>
            ))}
          </div>
        </div>
      )}

      {artifactData.csvDocuments.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 Case Analysis Data ({artifactData.csvDocuments.length})</h3>
          <div className="space-y-4">
            {artifactData.csvDocuments.map((doc, index) => (
              <div key={`csv-${index}-${doc.document_id || doc.filename}`}>
                {renderDocumentAnalysis(doc)}
              </div>
            ))}
          </div>
        </div>
      )}

      {artifactData.otherDocuments.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">📎 Other Documents ({artifactData.otherDocuments.length})</h3>
          <div className="space-y-4">
            {artifactData.otherDocuments.map((doc, index) => (
              <div key={`other-${index}-${doc.document_id || doc.filename}`}>
                {renderDocumentAnalysis(doc)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Analysis Insights Footer */}
      <div className="bg-gray-50 rounded-lg p-6 mt-8">
        <h4 className="font-medium text-gray-900 mb-3">🤖 How These Artifacts Enhance AI Analysis:</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="bg-white rounded p-3">
            <div className="font-medium text-blue-600 mb-2">📄 Document Analysis</div>
            <p className="text-gray-600">Text documents provide detailed architecture context, enabling AI agents to understand your specific implementation and generate targeted recommendations.</p>
          </div>
          <div className="bg-white rounded p-3">
            <div className="font-medium text-purple-600 mb-2">🖼️ Visual Recognition</div>
            <p className="text-gray-600">Architecture diagrams are analyzed to identify services, connections, and patterns, extracting structured data for comprehensive pillar assessment.</p>
          </div>
          <div className="bg-white rounded p-3">
            <div className="font-medium text-orange-600 mb-2">📊 Reactive Analysis</div>
            <p className="text-gray-600">CSV case data reveals historical patterns and common issues, enabling proactive recommendations based on real-world operational experience.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;