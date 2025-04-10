from fastapi import FastAPI, Depends, HTTPException, status
import schemas, models, crud_Item, crud_ToDoList
import database
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

app = FastAPI()

# Простейший GET-эндпоинт для корневой страницы
@app.get("/")
async def root():
    return {"greeting": "Hello world"}

@app.get("/db-check")
async def check_db_connection(db: AsyncSession = Depends(database.get_db)):
    try:
        # Простой SQL-запрос для проверки соединения
        result = await db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Database connection is working", "result": result.scalar()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=True
    )
#для запуска проги uvicorn main:app --reload

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Crud для item
@app.get("/items/", response_model=list[schemas.Item])
async def read_items(db=Depends(database.get_db)):
    items = await crud_Item.get_items(db)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db=Depends(database.get_db)):
    db_item = await crud_Item.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db=Depends(database.get_db)):
    return await crud_Item.post_item(db, item)

@app.patch("/items/{item_id}", response_model=schemas.Item)
async def update_item(
    item_id: int,
    item_data: schemas.ItemUpdate,
    db: AsyncSession = Depends(database.get_db)
):
    # Проверяем, существует ли пользователь
    db_item = await crud_Item.get_item(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    await crud_Item.update_item(db, item_id, item_data)
    return await crud_Item.get_item(db, item_id)  # Возвращаем обновленные данные

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(database.get_db)
):
    db_item = await crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    
    await crud.delete_item(db, item_id)
    return None  # 204 No Content


#Crud для ToDoList
@app.get("/ToDoLists/", response_model=list[schemas.ToDoList])
async def read_ToDoLists(db=Depends(database.get_db)):
    ToDoLists = await crud_ToDoList.get_ToDoLists(db)
    return ToDoLists

@app.get("/ToDoLists/{ToDoList_id}", response_model=schemas.ToDoList)
async def read_ToDoList(ToDoList_id: int, db=Depends(database.get_db)):
    db_ToDoList = await crud_ToDoList.get_ToDoList(db, ToDoList_id=ToDoList_id)
    if db_ToDoList is None:
        raise HTTPException(status_code=404, detail="ToDoList not found")
    return db_ToDoList

@app.post("/ToDoLists/", response_model=schemas.ToDoList)
async def create_ToDoList(ToDoList: schemas.ToDoListCreate, db=Depends(database.get_db)):
    return await crud_ToDoList.post_ToDoList(db, ToDoList)

@app.patch("/ToDoLists/{ToDoList_id}", response_model=schemas.ToDoList)
async def update_ToDoList(
    ToDoList_id: int,
    ToDoList_data: schemas.ToDoListUpdate,
    db: AsyncSession = Depends(database.get_db)
):
    # Проверяем, существует ли пользователь
    db_ToDoList = await crud_ToDoList.get_ToDoList(db, ToDoList_id)
    if not db_ToDoList:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ToDoList not found"
        )
    
    await crud_ToDoList.update_ToDoList(db, ToDoList_id, ToDoList_data)
    return await crud_ToDoList.get_ToDoList(db, ToDoList_id)  # Возвращаем обновленные данные

@app.delete("/ToDoLists/{ToDoList_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ToDoList(
    ToDoList_id: int,
    db: AsyncSession = Depends(database.get_db)
):
    db_ToDoList = await crud.get_ToDoList(db, ToDoList_id)
    if not db_ToDoList:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ToDoList not found"
        )
    
    await crud.delete_ToDoList(db, ToDoList_id)
    return None  # 204 No Content
