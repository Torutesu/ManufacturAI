import numpy as np
import random  # MVPでは簡易実装のためrandomを使用

def detect_defects(image):
    """
    MVPでは簡易的な欠陥検出モデル
    実際の製品では機械学習モデルを使用する
    """
    # 欠陥タイプのリスト
    defect_types = ['scratch', 'dent', 'crack', 'stain', 'discoloration']
    
    # ランダムに欠陥を検出するシミュレーション
    defect_count = random.randint(0, 3)  # 0〜3個の欠陥
    
    defects = []
    for _ in range(defect_count):
        defect_type = random.choice(defect_types)
        
        defect = {
            'type': defect_type,
            'x': random.uniform(0.1, 0.9),  # 画像上のx座標 (0-1の範囲)
            'y': random.uniform(0.1, 0.9),  # 画像上のy座標 (0-1の範囲)
            'severity': random.uniform(0.1, 0.9),  # 重要度 (0-1の範囲)
            'description': f"{defect_type.capitalize()} detected"
        }
        
        defects.append(defect)
    
    return defects

def forecast_inventory_demand(historical_data):
    """
    過去の在庫データに基づいて需要を予測
    MVPでは簡易的なトレンドベースの予測
    """
    # 実際の製品では、時系列予測モデル（ARIMA、Prophet、LSTMなど）を使用
    
    # サンプル予測（過去データの平均 + トレンド + ランダム成分）
    if not historical_data:
        return []
    
    avg_demand = np.mean([item['demand'] for item in historical_data])
    trend = 0.05  # 上昇トレンドを仮定
    
    forecast = []
    last_date = max([item['date'] for item in historical_data])
    
    for i in range(1, 13):  # 12ヶ月の予測
        predicted_demand = avg_demand * (1 + trend * i) + random.uniform(-0.1, 0.1) * avg_demand
        forecast.append({
            'date': f"{last_date[:-2]}{int(last_date[-2:]) + i:02d}",  # 簡易的な日付増分
            'predicted_demand': max(0, predicted_demand)
        })
    
    return forecast

def optimize_nesting(materials, parts):
    """
    部品配置の最適化を行うネスティングアルゴリズム
    MVPでは簡易的な実装
    """
    # 実際の製品では、遺伝的アルゴリズムや強化学習ベースの最適化を実装
    
    # 簡易的なパッキングシミュレーション
    material_area = materials['width'] * materials['height']
    total_parts_area = sum([part['width'] * part['height'] for part in parts])
    
    if total_parts_area > material_area:
        return {
            'status': 'error',
            'message': 'Total parts area exceeds material area',
            'utilization': 0,
            'nesting_plan': []
        }
    
    # ランダム配置（実際のプロダクトでは効率的なアルゴリズムを実装）
    current_x, current_y = 0, 0
    max_height_in_row = 0
    nesting_plan = []
    
    for part in parts:
        # 行の終わりに達した場合、新しい行に移動
        if current_x + part['width'] > materials['width']:
            current_x = 0
            current_y += max_height_in_row
            max_height_in_row = 0
        
        # この部品が材料に収まらない場合
        if current_y + part['height'] > materials['height']:
            continue
        
        nesting_plan.append({
            'part_id': part['id'],
            'x': current_x,
            'y': current_y,
            'rotation': 0
        })
        
        current_x += part['width']
        max_height_in_row = max(max_height_in_row, part['height'])
    
    # 利用率を計算
    utilized_parts = len(nesting_plan)
    utilization = sum([parts[i]['width'] * parts[i]['height'] for i in range(utilized_parts)]) / material_area
    
    return {
        'status': 'success',
        'utilization': utilization,
        'nesting_plan': nesting_plan,
        'parts_placed': utilized_parts,
        'total_parts': len(parts)
    }
