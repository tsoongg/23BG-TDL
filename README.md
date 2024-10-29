# To-do List API

## Project Overviewis 
This project is a simple RESTful API built with FastAPI that allows users to manage a to-do list.
It supports basic CRUD operations to create, read, update, and delete to-do items.

## Technologies Used
- **FastAPI**: Used for the backend framework.
- **SQLite**: Database used for storing to-do items.
- **Pydantic**: For data validation and settings management.

## Installation
To get started with this project, clone the repository and install the required dependencies.
To run the application locally, use the following command:

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.
You can access the automatic Swagger UI documentation at http://127.0.0.1:8000/docs to interact with the API.

## API Endpoints
- GET /todos/: Retrieve a list of all to-do items.
- POST /todos/: Create a new to-do item.
- GET /todos/{todo_id}: Retrieve a specific to-do item by its ID.
- PUT /todos/{todo_id}: Update a specific to-do item.
- DELETE /todos/{todo_id}: Delete a specific to-do item.

## Database Schema
- id: Integer, Primary Key, Autoincrement.
- title: Text.
- description: Text, nullable.
- completed: Boolean.

## Testing
To run the tests run "pytest" in your terminal.

## License
This project is licensed under Apache License 2.0 - see the LICENSE file for details.
