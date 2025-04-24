import React, { useState } from 'react';
import axios from 'axios';
import './MaterialNesting.css';

// コンポーネントのインポート
import MaterialForm from '../components/MaterialForm';
import PartsList from '../components/PartsList';
import NestingViewer from '../components/NestingViewer';

const API_URL = 'http://localhost:5000/api';

function MaterialNesting() {
  const [material, setMaterial] = useState({ width: 1220, height: 2440, thickness: 18, type: 'plywood' });
  const [parts, setParts] = useState([]);
  const [nestingResult, setNestingResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddPart = (part) => {
    setParts([...parts, { ...part, id: Date.now() }]);
  };

  const handleRemovePart = (partId) => {
    setParts(parts.filter(part => part.id !== partId));
  };

  const handleOptimizeNesting = async () => {
    if (parts.length === 0) {
      alert('部品が登録されていません。まず部品を追加してください。');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/material/nest`, {
        material,
        parts
      });

      setNestingResult(response.data);
    } catch (error) {
      console.error('Error optimizing nesting:', error);
      alert('ネスティング最適化中にエラーが発生しました。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="material-nesting">
      <h1>建材登録・ネスティング (MaterialAI)</h1>
      
      <div className="material-container">
        <div className="material-section">
          <h2>建材情報</h2>
          <MaterialForm material={material} setMaterial={setMaterial} />
        </div>
        
        <div className="parts-section">
          <h2>部品リスト</h2>
          <PartsList 
            parts={parts} 
            onAddPart={handleAddPart} 
            onRemovePart={handleRemovePart} 
          />
          
          <button 
            className="optimize-button" 
            onClick={handleOptimizeNesting}
            disabled={loading || parts.length === 0}
          >
            ネスティング最適化
          </button>
          
          {loading && <div className="loading">最適化中...</div>}
        </div>
      </div>
      
      {nestingResult && (
        <div className="result-section">
          <h2>ネスティング結果</h2>
          
          <div className="result-details">
            <p><strong>材料利用率:</strong> {(nestingResult.utilization * 100).toFixed(1)}%</p>
            <p><strong>配置された部品:</strong> {nestingResult.parts_placed} / {nestingResult.total_parts}</p>
          </div>
          
          <NestingViewer 
            material={material} 
            parts={parts} 
            nestingPlan={nestingResult.nesting_plan} 
          />
        </div>
      )}
    </div>
  );
}

export default MaterialNesting;
