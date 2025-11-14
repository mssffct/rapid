from typing import Union

from fastapi import FastAPI

from .routers import users

app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"Hello": "HI"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}