from fastapi import APIRouter, HTTPException, status
from app.models.todo import Todo
from app.schemas.todo import GetTodos, PostTodo, PutTodo

todo_router = APIRouter(prefix='/todos', tags=['todos'])

@todo_router.get('/')
async def all_todos():
    data = Todo.all()
    return await GetTodos.from_queryset(data)

@todo_router.post('/')
async def post_todo(body: PostTodo):
    row = await Todo.create(**body.dict(exclude_unset=True))
    return await GetTodos.from_tortoise_orm(row)

@todo_router.put('/{key}')
async def put_todo(key: int, body: PutTodo):
    data = body.dict(exclude_unset=True)
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo Topilmadi')
    await Todo.filter(id=key).update(**data)
    return await GetTodos.from_queryset_single(Todo.get(id=key))

@todo_router.delete('/{key}')
async def delete_todo(key: int):
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo Topilmadi')
    await Todo.filter(id=key).delete()
    return {'detail': f'Todo with key {key} has been deleted'}


