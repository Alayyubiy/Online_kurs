from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from db import database
from functions.progress import create_progress, update_progress, get_all_progress
from models import  Progress, User
from routers.auth import get_current_user
from schemas.progress import CreateProgress
from schemas.users import CreateUser

progress_router = APIRouter(tags=["Progress"])


@progress_router.get('/my_progress')
def get_my_progress(db: Session = Depends(database),
                    current_user: User = Depends(get_current_user)):
    return db.query(Progress).options(joinedload(Progress.lesson)).filter(Progress.user_id == current_user.id).all()

@progress_router.post("/create_progress")
def route_create_progress(form: CreateProgress, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    return create_progress(form, db, current_user)

@progress_router.put("/update_progress/{ident}")
def route_update_progress(ident: int, form: CreateProgress, db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    return update_progress(ident, form, db, current_user)

@progress_router.get("/get_all_progress")
def route_get_all_progress(db: Session = Depends(database), current_user: CreateUser = Depends(get_current_user)):
    return get_all_progress(db, current_user)