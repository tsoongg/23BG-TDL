from httpx import AsyncClient
from main import app

import pytest
import pytest_asyncio

# Function to create a to-do item that is used in other tests
@pytest_asyncio.fixture
async def create_todo_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/todos/", json={"title": "Existing Todo", "description": "Exists", "completed": False})
        return response.json()
    
# Test for creating a to-do item with a description
@pytest.mark.asyncio
async def test_create_todo_with_description():
    # HTTP client bound to FastAPI
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Post request
        response = await ac.post("/todos/", json={"title": "TylerTitle", "description": "Smiski", "completed": False})
        assert response.status_code == 200
        data = response.json()
        # Check if the returned data matches input
        assert data["title"] == "TylerTitle"
        assert data["description"] == "Smiski"
        assert data["completed"] is False

# Test for retrieving all to-do items and validating their existence
@pytest.mark.asyncio
async def test_read_all_todos():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/todos/", json={"title": "Task 1", "description": "Desc 1", "completed": False})
        await ac.post("/todos/", json={"title": "Task 2", "description": "Desc 2", "completed": True})
        # Gets the to-do items
        response = await ac.get("/todos/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2 # Makes sure at least 2 items exist
        titles = [item['title'] for item in data]
        assert "Task 1" in titles
        assert "Task 2" in titles

# Test for reading a specific to-do item using its ID
@pytest.mark.asyncio
async def test_read_todo(create_todo_item):
    todo_id = create_todo_item['id']
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()['id'] == todo_id

# Test for updating a specific to-do item and verifying the changes
@pytest.mark.asyncio
async def test_update_todo(create_todo_item):
    todo_id = create_todo_item['id']
    async with AsyncClient(app=app, base_url="http://test") as ac:
        updated_data = {
            "title": "Updated Test Todo",
            "description": create_todo_item['description'],
            "completed": create_todo_item['completed']
        }
        response = await ac.put(f"/todos/{todo_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        # Check the data was updated correctly
        assert data['title'] == "Updated Test Todo"
        assert data['description'] == create_todo_item['description']
        assert data['completed'] == create_todo_item['completed']

# Test for deletinga  specific to-do item and verifying its successfully been removed
@pytest.mark.asyncio
async def test_delete_todo(create_todo_item):
    todo_id = create_todo_item['id']
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete(f"/todos/{todo_id}") 
        assert response.status_code == 204