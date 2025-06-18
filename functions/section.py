from fastapi import HTTPException
from models.section import Section
from models.user import User



def create_section(form, db, current_user: User):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Only admin can create sections.")

    section = Section(
        title=form.title.strip().capitalize(),
        order=form.order,
        course_id=form.course_id
    )
    db.add(section)
    db.commit()
    db.refresh(section)
    return {"message": "Section added to the database","section_id":section.id}




def update_section(ident, form, db, current_user: User):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Only admin can update sections.")

    section = db.query(Section).filter(Section.id == ident).first()
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    section.title = form.title.strip().capitalize()
    section.order = form.order
    db.commit()
    return {"message": "Section updated"}


def delete_section(ident, db, current_user):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Sizda ruxsat yo'q!")
    section = db.query(Section).filter(Section.id == ident).first()
    if not section:
        raise HTTPException(status_code=404, detail="Bunday bo‘lim yo‘q!")
    db.delete(section)
    db.commit()
    return {"message": "Section va unga bog‘liq darslar o‘chirildi"}

