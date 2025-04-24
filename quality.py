from . import db
from datetime import datetime

class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(db.String(20), nullable=False)  # pass, fail, warning
    confidence = db.Column(db.Float)
    image_path = db.Column(db.String(255))
    defects = db.relationship('Defect', backref='inspection', lazy=True)

class Defect(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location_x = db.Column(db.Float)
    location_y = db.Column(db.Float)
    severity = db.Column(db.Float)
    description = db.Column(db.String(255))
