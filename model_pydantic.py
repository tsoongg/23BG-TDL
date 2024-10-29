from pydantic import BaseModel

# Base class for a to-do item
class ToDoItemBase(BaseModel):
    title: str # Required string representing the title of the to-do item
    description: str = None # Optional string for a description
    completed: bool = False # Boolean to track if the to-do item is completed

# Creation schema for to-do items
class ToDoItemCreate(ToDoItemBase):
    pass

# Read schema for to-do items
class ToDoItemRead(ToDoItemBase):
    id: int # Integer required for identifying the to-do item
    
    class Config:
        from_attributes = True # Allows ORM mode to work with databases directly