from fastapi import HTTPException
from models.course import Course


def create_courses(form, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="You do not have admin rights!")

    new_course = Course(
        name=form.name,
        description=form.description,

    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return {"message": "Course added to the database"}



def update_courses(ident, form, db, current_user):
    if current_user.role != 'admin':
        return {"message": "You do not have admin rights!"}

    course = db.query(Course).filter(Course.id == ident).first()
    if not course:
        raise HTTPException(status_code=404, detail="The Course you entered does not exist!")


    cleaned_data = {
        "name": form.name.strip().capitalize(),
        "description": form.description.strip(),

    }

    db.query(Course).filter(Course.id == ident).update(cleaned_data)
    db.commit()
    return {"message": "Course updated successfully!"}




def delete_courses(ident,db,current_user):
    if current_user.role == 'admin':
        courses = db.query(Course).filter(Course.id == ident).first()
        if not courses:
            raise HTTPException(404, "The Course was deleted from the database!!!")

        db.query(Course).filter(Course.id == ident).delete()
        db.commit()
        return {"Message": "The Course was deleted from the database."}
    else:
        return {"Message": "You do not have admin rights !!!"}
















