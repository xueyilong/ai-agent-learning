from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


@app.get("/")
def root():
    return {"message": "faker"}


@app.get("/name")
def hello(name: str = "同66"):
    return {"你好": name}


@app.get("/users/{user_id}")
def search_id(user_id: int):
    return {"user_id": user_id}


class UserCreat(BaseModel):
    name: str
    age: int
    email: str | None = None


@app.post("/users/creat_user")
def creat_user(user: UserCreat):
    return {
        "收到的名字": user.name,
        "收到的年龄": user.age,
        "收到的邮箱": user.email
    }
