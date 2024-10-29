from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# defines the base case
Base = declarative_base()

# To-do item SQLAlchemy model
# Defines the structure of the to-do items table
class ToDoItem(Base):
    __tablename__ = 'todo_items' # Name of the table in the database

    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    title = Column(String, index = True)
    description = Column(String, index = True, nullable = True)
    completed = Column(Boolean, default = False)

# Connection string for the SQLite database
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create an Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker instance
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Function to create database tables based on defined models.
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)