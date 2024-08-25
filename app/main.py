from fastapi import FastAPI
from app.routers.todo import todo_router
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Yoki aniq domenlar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(todo_router)
register_tortoise(
    app=app,
    db_url='sqlite://todo.db',
    add_exception_handlers=True,
    generate_schemas=True,
    modules={'models':["app.models.todo"]}
)

@app.get('/')
def index():
    return {"status":'app is runing'}