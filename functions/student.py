from models.user import User
from routers.auth import get_password_hash
from fastapi import HTTPException

def create_student(form, db, teacher):
    existing = db.query(User).filter(User.username == form.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username band!")

    new_user = User(
        name=form.name,
        username=form.username,
        password=get_password_hash(form.password),
        phone=form.phone,
        role="student",
        created_by=teacher.id  # teacher_id ni ko'rsatamiz
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_my_students(db, teacher_id):
    return db.query(User).filter(User.role == "student", User.created_by == teacher_id).all()
