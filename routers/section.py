from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from models import Section
from schemas.sections import CreateSections, UpdateSections
from db import database
from functions.section import create_section,  update_section, delete_section
from routers.auth import get_current_user
from schemas.users import CreateUser

section_router = APIRouter(tags=["Sections"])

@section_router.get("/get_sections")
def get_sections(db: Session = Depends(database)):
    sections = db.query(Section).options(joinedload(Section.lessons)).all()
    return sections

@section_router.post('/create_section')
def create_section_view(  form: CreateSections, db: Session = Depends(database),
 current_user: CreateUser = Depends(get_current_user)
):
    return create_section(form, db, current_user)


@section_router.put('/update_section/{ident}')
def update_section_view(
    ident: int,
    form: UpdateSections,
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_user)
):
    return update_section(ident, form, db, current_user)

@section_router.delete('/delete_section/{ident}')
def delete_section_view(
    ident: int,
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_user)
):
    return delete_section(ident, db, current_user)
