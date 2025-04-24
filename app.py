from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from models import db
from services.quality_service import QualityService
from services.inventory_service import InventoryService
from services.material_service import MaterialService
from services.production_service import ProductionService
import config

app = Flask(__name__)
CORS(app)

# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# サービスのインスタンス化
quality_service = QualityService()
inventory_service = InventoryService()
material_service = MaterialService()
production_service = ProductionService()

# APIエンドポイント - QualityAI
@app.route('/api/quality/analyze', methods=['POST'])
def analyze_quality():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    result = quality_service.analyze_image(image_file)
    return jsonify(result)

@app.route('/api/quality/reports', methods=['GET'])
def get_quality_reports():
    reports = quality_service.get_reports()
    return jsonify(reports)

# APIエンドポイント - InventoryAI
@app.route('/api/inventory/optimize', methods=['POST'])
def optimize_inventory():
    data = request.json
    result = inventory_service.optimize_inventory(data)
    return jsonify(result)

@app.route('/api/inventory/forecast', methods=['POST'])
def forecast_demand():
    data = request.json
    result = inventory_service.forecast_demand(data)
    return jsonify(result)

# APIエンドポイント - MaterialAI
@app.route('/api/material/register', methods=['POST'])
def register_material():
    data = request.json
    result = material_service.register_material(data)
    return jsonify(result)

@app.route('/api/material/nest', methods=['POST'])
def optimize_nesting():
    data = request.json
    result = material_service.optimize_nesting(data)
    return jsonify(result)

# APIエンドポイント - ProductionAI
@app.route('/api/production/plan', methods=['POST'])
def create_production_plan():
    data = request.json
    result = production_service.create_plan(data)
    return jsonify(result)

@app.route('/api/production/monitor', methods=['GET'])
def get_production_status():
    result = production_service.get_status()
    return jsonify(result)

# データベース初期化
@app.before_first_request
def initialize_database():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host='0.0.0.0', port=config.PORT)
