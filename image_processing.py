import cv2
import numpy as np

def process_image(image_path):
    """
    画像前処理を行い、分析用の画像を返す
    """
    # 画像読み込み
    image = cv2.imread(image_path)
    
    # グレースケール変換
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # ノイズ除去
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # コントラスト強調
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    
    return enhanced
