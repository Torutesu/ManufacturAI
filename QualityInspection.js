import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './QualityInspection.css';

// コンポーネントのインポート
import ImageUploader from '../components/ImageUploader';
import DefectViewer from '../components/DefectViewer';
import InspectionHistory from '../components/InspectionHistory';

const API_URL = 'http://localhost:5000/api';

function QualityInspection() {
  const [loading, setLoading] = useState(false);
  const [inspectionResult, setInspectionResult] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // 検査履歴を取得
    fetchInspectionHistory();
  }, []);

  const fetchInspectionHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/quality/reports`);
      setHistory(response.data);
    } catch (error) {
      console.error('Failed to fetch inspection history:', error);
    }
  };

  const handleImageUpload = async (file) => {
    setLoading(true);
    setInspectionResult(null);

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await axios.post(`${API_URL}/quality/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setInspectionResult(response.data);
      // 履歴を更新
      fetchInspectionHistory();
    } catch (error) {
      console.error('Error analyzing image:', error);
      alert('画像分析中にエラーが発生しました。もう一度お試しください。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="quality-inspection">
      <h1>品質検査 (QualityAI)</h1>
      
      <div className="inspection-container">
        <div className="upload-section">
          <h2>製品画像をアップロード</h2>
          <ImageUploader onUpload={handleImageUpload} disabled={loading} />
          
          {loading && <div className="loading">分析中...</div>}
        </div>
        
        {inspectionResult && (
          <div className="result-section">
            <h2>検査結果</h2>
            <div className={`result-badge ${inspectionResult.result}`}>
              {inspectionResult.result === 'pass' ? '合格' : '不合格'}
            </div>
            
            <div className="result-details">
              <p><strong>製品ID:</strong> {inspectionResult.product_id}</p>
              <p><strong>信頼度:</strong> {(inspectionResult.confidence * 100).toFixed(1)}%</p>
              <p><strong>検出された欠陥:</strong> {inspectionResult.defects.length}</p>
            </div>
            
            {inspectionResult.defects.length > 0 && (
              <DefectViewer defects={inspectionResult.defects} />
            )}
          </div>
        )}
      </div>
      
      <div className="history-section">
        <h2>検査履歴</h2>
        <InspectionHistory history={history} />
      </div>
    </div>
  );
}

export default QualityInspection;
