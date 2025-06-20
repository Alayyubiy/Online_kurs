from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from schemas.enrollments import CreateEnrollments
from functions.enrollments import (
    enroll_user, get_all_enrollments,
    update_enrollment, delete_enrollment
)
from routers.auth import get_current_user
from models.user import User

enrollment_router = APIRouter(tags=["Enrollments"])


@enrollment_router.get("/enrollments")
def route_get_enrollments(db: Session = Depends(database),
                          current_user: User = Depends(get_current_user)):
    return get_all_enrollments(db, current_user)


@enrollment_router.post("/enroll_user")
def route_enroll_user(form: CreateEnrollments,
                      db: Session = Depends(database),
                      current_user: User = Depends(get_current_user)):
    return enroll_user(form, db, current_user)


@enrollment_router.put("/update_enrollment/{ident}")
def route_update_enrollment(ident: int,
                            form: CreateEnrollments,
                            db: Session = Depends(database),
                            current_user: User = Depends(get_current_user)):
    return update_enrollment(ident, form, db, current_user)


@enrollment_router.delete("/delete_enrollment/{ident}")
def route_delete_enrollment(ident: int,
                            db: Session = Depends(database),
                            current_user: User = Depends(get_current_user)):
    return delete_enrollment(ident, db, current_user)
