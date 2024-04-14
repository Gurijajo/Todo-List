from fastapi import FastAPI, HTTPException
from starlette import status
from tortoise.contrib.fastapi import register_tortoise
from schemas import TodoGet, TodoPost, TodoPut
from models import Todo
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@router.get('/')
async def all_todos():
    todos = await Todo.all()
    todos_dict = [todo.__dict__ for todo in todos]
    return todos_dict

@router.post('/')
async def post_todo(body: TodoPost):
    data = body.dict(exclude_unset=True)
    todo = await Todo.create(**data)
    return todo.__dict__


@router.put('/{todo_id}')
async def update_todo(todo_id: str, body: TodoPut):
    todo_exists = await Todo.filter(id=todo_id).exists()
    if not todo_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )
    data = body.dict(exclude_unset=True)
    await Todo.filter(id=todo_id).update(**data)
    return "Update successful"


@router.delete('/{todo_id}')
async def delete_todo(todo_id: str):
    todo_exists = await Todo.filter(id=todo_id).exists()
    if not todo_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )
    await Todo.filter(id=todo_id).delete()
    return "Item deleted"

app.include_router(router)

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
