from fastapi import HTTPException
from models.user import User
from routers.auth import get_password_hash


def add_user(form, db):
    a = db.query(User).filter(User.username == form.username).first()
    if a:
        raise HTTPException(404,"Bunday user band")
    new_user = User(
        name=form.name.strip().capitalize(),
        username=form.username,
        password=get_password_hash(form.password),
        phone=form.phone,
        role = 'user'
    )
    db.add(new_user)
    db.commit()
    return {"massage" : " User royxatdan o'tdi !!!","user_id":new_user.id}


def add_admin(form, db, current_user):
    if current_user.role == 'admin':
        new_user = User(
            name=form.name.strip().capitalize(),
            username=form.username.strip(),
            password=get_password_hash(form.password),
            phone=form.phone.strip(),
            role='admin'
        )
        db.add(new_user)
        db.commit()
        return {"massage": " User royxatdan o'tdi !!!","user_id":new_user.id}
    else:
        return {"massage": "Sizga admin qoshishga ruxsat yo'q"}



def update_user(ident, form, db, current_user):
    if current_user.role == 'admin':
        user = db.query(User).filter(User.id == ident).first()
        if not user:
            raise HTTPException(404, "he building you entered does not exist!!!")

        db.query(User).filter(User.id == ident).update({
            User.name: form.name.strip().capitalize(),
            User.username: form.username.strip(),
            User.password: get_password_hash(form.password),
            User.phone: form.phone.strip()
        })
        db.commit()
        return {"Message": "Users restarted"}
    else:
        return {"massage": "Sizga admin qoshishga ruxsat yo'q"}



def update_own(form, db, current_user):
    db.query(User).filter(User.id == current_user.id).update({
        User.name: form.name.strip().capitalize(),
        User.username: form.username.strip(),
        User.password: get_password_hash(form.password),
        User.phone: form.phone.strip()
    })
    db.commit()
    return {"massage": "Profil tahrirlandi"}


def delete_user(ident, db, current_user):
    if current_user.role == 'admin':
        user = db.query(User).filter(User.id == ident).first()
        if not user:
            raise HTTPException(404, "The users was deleted from the database!!!")

        db.query(User).filter(User.id == ident).delete()
        db.commit()
        return {"Message": "The users was deleted from the database.!!!"}
    else:
        return {"massage": "Sizga admin qoshishga ruxsat yo'q"}



def delete_own(db, current_user):
    db.query(User).filter(User.id == current_user.id).delete()
    db.commit()
    return {"massage": "Profil ochirildi"}

