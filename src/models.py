from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """User model for auth. Password is stored as a hash."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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

def seed_users():
    """Create some default users for testing. Created once at startup"""
    if User.query.count() == 0:
        user1 = User(username="admin")
        user1.set_password("adminpass")
        db.session.add(user1)

        user2 = User(username="user")
        user2.set_password("userpass")
        db.session.add(user2)

        db.session.commit()