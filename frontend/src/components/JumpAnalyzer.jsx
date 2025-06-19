import { useState } from 'react';
import api from '../api';
import '../styles/JumpAnalyzer.css';

function JumpAnalyzer() {
  const [file, setFile] = useState(null);
  const [processedVideo, setProcessedVideo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentAngles, setCurrentAngles] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('original_video', file);

    try {
      const response = await api.post('/api/jump-videos/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setProcessedVideo(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVideoTimeUpdate = (e) => {
    const video = e.target;
    const currentTime = video.currentTime;
    // You'll need to implement a way to get the angles for the current frame
    // This might require additional backend endpoints or processing
  };

  return (
    <div className="jump-analyzer">
      <h2>Jump Analyzer</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Upload & Analyze'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {processedVideo && (
        <div className="results">
          <h3>Analysis Results</h3>
          <div className="angles">
            <div className="angle-group">
              <h4>Left Side</h4>
              <p>Knee: {processedVideo.left_knee_angle?.toFixed(1) || '0.0'}</p>
              <p>Hip: {processedVideo.left_hip_angle?.toFixed(1) || '0.0'}</p>
              <p>Ankle: {processedVideo.left_ankle_angle?.toFixed(1) || '0.0'}</p>
              <p>Shoulder: {processedVideo.left_shoulder_angle?.toFixed(1) || '0.0'}</p>
            </div>
            <div className="angle-group">
              <h4>Right Side</h4>
              <p>Knee: {processedVideo.right_knee_angle?.toFixed(1) || '0.0'}</p>
              <p>Hip: {processedVideo.right_hip_angle?.toFixed(1) || '0.0'}</p>
              <p>Ankle: {processedVideo.right_ankle_angle?.toFixed(1) || '0.0'}</p>
              <p>Shoulder: {processedVideo.right_shoulder_angle?.toFixed(1) || '0.0'}</p>
            </div>
          </div>
          <video 
            controls 
            width="640"
            onTimeUpdate={handleVideoTimeUpdate}
          >
            <source src={processedVideo.processed_video} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default JumpAnalyzer;