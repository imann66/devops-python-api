from app.app import app, db
from app.models import Task

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")