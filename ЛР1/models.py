from sqlalchemy import Boolean, Column, Integer, String
import database

class Item(database.Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    is_done = Column(Boolean, index=True)

class ToDoList(database.Base):
    __tablename__ = "to_do_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)