from sqlalchemy import select
import models, schemas

#get для всего
async def get_items(db):
    result = await db.execute(select(models.Item))
    return result.scalars().all()

#get для одного
async def get_item(db, item_id: int):
    result = await db.execute(select(models.Item).where(models.Item.id == item_id))
    return result.scalars().first()

#post item
async def post_item(db, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

#patch item
async def update_item(db, item_id: int, item_data: schemas.ItemUpdate):
    # Обновляем только переданные поля
    update_data = item_data.model_dump(exclude_unset=True)
    stmt = (
        update(models.Item)
        .where(models.Item.id == item_id)
        .values(**update_data)
    )
    await db.execute(stmt)
    await db.commit()

#delete item 
async def delete_item(db, item_id: int):
    stmt = delete(models.Item).where(models.Item.id == item_id)
    await db.execute(stmt)
    await db.commit()

