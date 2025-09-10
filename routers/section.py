from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from models import Section, User
from schemas.sections import CreateSections, UpdateSections
from db import database
from functions.section import create_section, update_section, delete_section
from routers.auth import get_current_user

section_router = APIRouter(tags=["Sections"])


@section_router.get("/get_sections")
def get_sections(
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(Section).options(joinedload(Section.lessons)).all()
    elif current_user.role == "teacher":
        # Faqat o‘ziga tegishli course sectionlarini qaytaradi
        return db.query(Section).join(Section.course).filter(
            Section.course.has(created_by=current_user.id)
        ).options(joinedload(Section.lessons)).all()
    else:
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo‘q.")



@section_router.post("/create_section")
def create_section_view(
    form: CreateSections,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return create_section(form, db, current_user)


@section_router.put("/update_section/{ident}")
def update_section_view(
    ident: int,
    form: UpdateSections,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return update_section(ident, form, db, current_user)


@section_router.delete("/delete_section/{ident}")
def delete_section_view(
    ident: int,
    db: Session = Depends(database),
    current_user: User = Depends(get_current_user)
):
    return delete_section(ident, db, current_user)
