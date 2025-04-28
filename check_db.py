from app.database import SessionLocal
from app.models import Project

db = SessionLocal()
projects = db.query(Project).all()

for p in projects:
    print(p.user_id, p.title, p.description, p.link)
