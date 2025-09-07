from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from functions.user import add_user, update_user, delete_user, add_admin, update_own, delete_own
from models.user import User
from routers.auth import get_current_user
from schemas.users import CreateUser, UpdateUser
from db import database


user_router = APIRouter(tags=["User"])


@user_router.get('/get_my_user')
def get_my_user(
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi"
        )
    return user


# Admin barcha foydalanuvchilarni olish
@user_router.get('/get_all_users')
def get_all_users(
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_user)
):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ruxsat yo'q"
        )
    return db.query(User).all()


@user_router.post('/create_user')
def create_user(form: CreateUser, db: Session = Depends(database)):
    return add_user(form, db)


@user_router.post('/create_admin')
def create_admin(form: CreateUser, db: Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_user)):
    return add_admin(form, db, current_user)


@user_router.put('/put_user')
def update_users(ident:int, form : UpdateUser,db:Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_user)):
    return update_user(ident, form, db, current_user)


@user_router.put('/put_own')
def update_profil(form : UpdateUser,db:Session = Depends(database),
               current_user: CreateUser = Depends(get_current_user)):
    return update_own(form, db, current_user)


@user_router.delete('/delete_user')
def delete_users(ident: int,db:Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_user)):
    return delete_user(ident,db, current_user)


@user_router.delete('/delete_own')
def delete_profil(db:Session = Depends(database),
                 current_user: CreateUser = Depends(get_current_user)):
    return delete_own(db, current_user)