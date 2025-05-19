from pydantic import BaseModel, EmailStr
from typing import Optional

# Схема для обновления (PATCH)item - все поля необязательные
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

class ItemCreate(BaseModel):
    name: str
    description: str
    is_done: bool

class Item(ItemCreate):
    id: int

    class Config:
        from_attributes = True

class CRUDItemUpdate(ItemUpdate):
    deleted_at: Optional[str] = None


# Схема для обновления (PATCH)ToDoList - все поля необязательные
class ToDoListUpdate(BaseModel):
    name: Optional[str] = None

class ToDoListCreate(BaseModel):
    name: str

class ToDoList(ToDoListCreate):
    id: int

    class Config:
        from_attributes = True

class CRUDToDoListUpdate(ToDoListUpdate):
    deleted_at: Optional[str] = None
