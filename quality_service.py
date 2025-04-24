import os
import uuid
from datetime import datetime
from models import db
from models.quality import Inspection, Defect
from utils.image_processing import process_image
from utils.ai_helpers import detect_defects

class QualityService:
    def analyze_image(self, image_file):
        # 画像保存
        filename = f"{uuid.uuid4()}.jpg"
        upload_folder = "uploads/images/"
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        image_file.save(image_path)
        
        # 画像処理
        processed_image = process_image(image_path)
        
        # AI分析 (MVPでは簡易的な実装)
        defects = detect_defects(processed_image)
        
        # 結果をデータベースに保存
        inspection = Inspection(
            product_id=f"PROD-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            result="pass" if not defects else "fail",
            confidence=0.92,
            image_path=image_path
        )
        
        db.session.add(inspection)
        db.session.commit()
        
        # 検出された欠陥情報を保存
        for defect_data in defects:
            defect = Defect(
                inspection_id=inspection.id,
                type=defect_data['type'],
                location_x=defect_data['x'],
                location_y=defect_data['y'],
                severity=defect_data['severity'],
                description=defect_data['description']
            )
            db.session.add(defect)
        
        db.session.commit()
        
        return {
            'inspection_id': inspection.id,
            'product_id': inspection.product_id,
            'result': inspection.result,
            'confidence': inspection.confidence,
            'defects': [
                {
                    'type': d.type,
                    'location': {'x': d.location_x, 'y': d.location_y},
                    'severity': d.severity,
                    'description': d.description
                } for d in inspection.defects
            ]
        }
    
    def get_reports(self):
        inspections = Inspection.query.order_by(Inspection.timestamp.desc()).limit(50).all()
        return [
            {
                'inspection_id': inspection.id,
                'product_id': inspection.product_id,
                'timestamp': inspection.timestamp.isoformat(),
                'result': inspection.result,
                'defects_count': len(inspection.defects)
            } for inspection in inspections
        ]
