from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import database
from functions.live_sessions import create_live_session, get_student_live_sessions, get_all_live_sessions, \
    delete_live_session, update_live_session
from schemas.live_sessions import CreateLiveSession
from routers.auth import get_current_user
from models import User

live_router = APIRouter(tags=["LiveSession"])

@live_router.get("/live/my")
def route_student_live(db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    return get_student_live_sessions(db, current_user)

@live_router.get("/live/all")
def route_all_live(db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    return get_all_live_sessions(db, current_user)

@live_router.post("/live/create")
def route_create_live(form: CreateLiveSession, db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    return create_live_session(form, db, current_user)

@live_router.put("/update_live_session/{ident}")
def route_update_live_session(
    ident: int,
    form: CreateLiveSession,
    db: Session = Depends(database),
    current_user = Depends(get_current_user)
):
    return update_live_session(ident, form, db, current_user)

@live_router.delete("/delete_live_session/{session_id}")
def route_delete_live(session_id: int, db: Session = Depends(database), current_user: User = Depends(get_current_user)):
    return delete_live_session(session_id, db, current_user)



