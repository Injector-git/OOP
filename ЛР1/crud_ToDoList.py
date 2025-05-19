from sqlalchemy import select,update
import models, schemas

#get для всего
async def get_ToDoList(db):
    result = await db.execute(select(models.ToDoList))
    return result.scalars().all()

#get для одного
async def get_ToDoList(db, ToDoList_id: int):
    result = await db.execute(select(models.ToDoList).where(models.ToDoList.id == ToDoList_id))
    return result.scalars().first()

#post ToDoList
async def post_ToDoList(db, ToDoList: schemas.ToDoListCreate):
    db_ToDoList = models.ToDoList(**ToDoList.model_dump())
    db.add(db_ToDoList)
    await db.commit()
    await db.refresh(db_ToDoList)
    return db_ToDoList

#patch ToDoList
async def update_ToDoList(db, ToDoList_id: int, ToDoList: schemas.CRUDToDoListUpdate):
    # Обновляем только переданные поля
    update_data = ToDoList.model_dump(exclude_unset=True)
    stmt = (
        update(models.ToDoList)
        .where(models.ToDoList.id == ToDoList_id)
        .values(**update_data) 
    )
    await db.execute(stmt)
    await db.commit()

#delete ToDoList 
async def delete_ToDoList(db, ToDoList_id: int):
    stmt = db.delete(models.ToDoList).where(models.ToDoList.id == ToDoList_id)
    await db.execute(stmt)
    await db.commit()
