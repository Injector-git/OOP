from sqlalchemy import Boolean, Column, Integer, String, Date
import database

class Item(database.Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    is_done = Column(Boolean, index=True)
    deleted_at = Column(String, nullable=True, index=True)#Поменять str na date

class ToDoList(database.Base):
    __tablename__ = "to_do_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    deleted_at = Column(String, nullable=True, index=True)#Поменять str na date
    item_done = Column(Integer, index=True)
    item_total = Column(Integer, index=True)