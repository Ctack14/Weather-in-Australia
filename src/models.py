from db import db
from datetime import datetime



class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    graph_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Query(db.Model):
    __tablename__ = 'queries'

    id = db.Column(db.Integer, primary_key=True, index=True)
    location = db.Column(db.String, nullable=True)
    graph_type = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

