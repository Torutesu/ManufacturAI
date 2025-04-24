import React, { useRef, useEffect } from 'react';
import './NestingViewer.css';

function NestingViewer({ material, parts, nestingPlan }) {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    if (!canvasRef.current || !material || !parts || !nestingPlan) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // キャンバスサイズを設定
    const maxWidth = 800;
    const scale = maxWidth / material.width;
    canvas.width = material.width * scale;
    canvas.height = material.height * scale;
    
    // 背景をクリア
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 材料の枠を描画
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, canvas.width, canvas.height);
    
    // 部品を描画
    const colors = ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6', '#1abc9c'];
    
    nestingPlan.forEach((placement, index) => {
      const part = parts.find(p => p.id === placement.part_id);
      if (!part) return;
      
      const colorIndex = index % colors.length;
      ctx.fillStyle = colors[colorIndex];
      
      const x = placement.x * scale;
      const y = placement.y * scale;
      const width = part.width * scale;
      const height = part.height * scale;
      
      ctx.fillRect(x, y, width, height);
      ctx.strokeRect(x, y, width, height);
      
      // 部品ID/名前を表示
      ctx.fillStyle = '#fff';
      ctx.font = '12px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(part.name || `#${index + 1}`, x + width / 2, y + height / 2);
    });
    
  }, [material, parts, nestingPlan]);
  
  return (
    <div className="nesting-viewer">
      <canvas ref={canvasRef} className="nesting-canvas"></canvas>
      <div className="nesting-legend">
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#f0f0f0' }}></div>
          <span>未使用領域</span>
        </div>
        <div className="legend-item">
          <div className="legend-color" style={{ backgroundColor: '#3498db' }}></div>
          <span>配置済み部品</span>
        </div>
      </div>
    </div>
  );
}

export default NestingViewer;
