from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database

app = FastAPI(title='todo-llm API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TodoCreate(BaseModel):
    description: str   

class TodoUpdate(BaseModel):
    description: str | None = None
    done: bool | None = None

@app.post("/todos", status_code=201)
def create_todo(body: TodoCreate):
    id = database.create_todo(body.description)
    return {"id": id}

@app.get("/todos")
def list_todos():
    return database.list_todos()

@app.get("/todos/{id}")
def get_todo(id: int):
    todo = database.get_todo(id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    return todo

@app.patch("/todos/{id}")
def update_todo(id: int, body: TodoUpdate):
    todo_update = database.update_todo(id, description=body.description, done=body.done)
    if not todo_update:
        raise HTTPException(status_code=404, detail="Not found")
    return todo_update

@app.delete("/todos/{id}", status_code=204)
def delete_todo(id: int):
    todo_delete = database.delete_todo(id)
    if not todo_delete:
        raise HTTPException(status_code=404, detail="Not found")
    return todo_delete