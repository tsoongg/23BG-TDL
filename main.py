from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
from typing import List
from models import engine
from model_pydantic import ToDoItemCreate, ToDoItemRead

# Initialize the FastAPI app
app = FastAPI()

# Event handler for starting up the app
# Creates database tables
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Endpoint to retrieve all to-do items
@app.get("/todos/", response_model=List[ToDoItemRead])
async def read_all_todos():
    async with models.AsyncSessionLocal() as session:
        result = await session.execute(select(models.ToDoItem))
        todos = result.scalars().all()
        return todos
    
# Endpoint to create a new to-do item
@app.post("/todos/", response_model=ToDoItemRead)
async def create_todo(todo: ToDoItemCreate):
    async with models.AsyncSessionLocal() as session:
        new_todo = models.ToDoItem(**todo.dict())
        session.add(new_todo)
        await session.commit()
        await session.refresh(new_todo) # Refresh to load data fro DB
        return new_todo

# Endpoint to retrieve all to-do items
@app.get("/todos/{todo_id}", response_model=ToDoItemRead)
async def read_todo(todo_id: int):
    async with models.AsyncSessionLocal() as session:
        result = await session.execute(select(models.ToDoItem).filter(models.ToDoItem.id == todo_id))
        todo = result.scalars().first()
        if todo is None:
            raise HTTPException(status_code=404, detail="To-Do item not found")
        return todo
    
# Endpoint to update specific to-do items    
@app.put("/todos/{todo_id}", response_model=ToDoItemRead)
async def update_todo(todo_id: int, todo: ToDoItemCreate):
    async with models.AsyncSessionLocal() as session:
        result = await session.execute(
            select(models.ToDoItem).filter(models.ToDoItem.id == todo_id)
        )
        existing_todo = result.scalars().first()
        if existing_todo is None:
            raise HTTPException(status_code=404, detail="To-Do item not found")
        
        # Update specific attributes of the to-do item
        for var, value in todo.dict().items():
            setattr(existing_todo, var, value) if value is not None else None
        session.add(existing_todo)
        await session.commit()
        await session.refresh(existing_todo)
        todo_data = ToDoItemRead.from_orm(existing_todo)
    return todo_data

# Endpoint to delete specific to-do items    
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    async with models.AsyncSessionLocal() as session:
        result = await session.execute(select(models.ToDoItem).filter(models.ToDoItem.id == todo_id))
        todo = result.scalars().first()
        if todo is None:
            raise HTTPException(status_code=404, detail="To-Do item not found")
        await session.delete(todo)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)